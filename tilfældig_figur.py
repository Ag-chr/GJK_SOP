import random
import math

from figurer import Figur
from position import Punkt

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def convex_hull(points):
    """Andrew's monotone chain. Returns hull as CCW list without repeated endpoint."""
    pts = sorted(points)
    if len(pts) <= 1:
        return pts[:]
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    # discard last point of each list (it's the start of the other list)
    hull = lower[:-1] + upper[:-1]
    return hull

def random_convex_polygon(n, scale=1.0, max_attempts=6):
    """
    Generate a random convex polygon with exactly n vertices.
    Returns: list of (x, y) tuples in CCW order.

    Parameters:
      n           : number of vertices (int, n >= 3)
      scale       : approximate size scale (float). Points lie roughly within a box ~[-scale, scale]
      max_attempts: how many times to try sampling random points to get hull with >= n vertices
    """
    if n < 3:
        raise ValueError("n must be >= 3")

    # Try to get >= n hull vertices by sampling random points
    for attempt in range(max_attempts):
        m = max(3*n, 60) + attempt * max(0, n)  # sample more as attempts increase
        pts = [(random.uniform(-scale, scale), random.uniform(-scale, scale)) for _ in range(m)]
        hull = convex_hull(pts)
        L = len(hull)
        if L >= n:
            # pick n vertices evenly around the hull (preserves convexity)
            indices = [int(i * L / n) for i in range(n)]
            polygon = [hull[idx % L] for idx in indices]
            polygon = list(map(lambda p: Punkt(p[0], p[1]), polygon))
            return Figur(polygon)

    print("fallback")
    # Fallback: inscribe points on a rotated, scaled circle (always convex)
    angles = sorted(random.random() * 2*math.pi for _ in range(n))
    # base circle points
    base = [(math.cos(a), math.sin(a)) for a in angles]

    # apply random affine: non-uniform scale, rotation, small translation
    sx = random.uniform(0.5, 1.5) * scale
    sy = random.uniform(0.5, 1.5) * scale
    theta = random.uniform(0, 2*math.pi)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    tx = random.uniform(-0.2, 0.2) * scale
    ty = random.uniform(-0.2, 0.2) * scale

    transformed = []
    for x, y in base:
        # scale
        x *= sx
        y *= sy
        # rotate
        xr = x * cos_t - y * sin_t
        yr = x * sin_t + y * cos_t
        # translate
        transformed.append(Punkt(xr + tx, yr + ty))

    return Figur(transformed)

# Example usage:
if __name__ == "__main__":
    poly = random_convex_polygon(8, scale=10.0)
    print("Polygon with", len(poly), "vertices:")
    for p in poly:
        print(p)
