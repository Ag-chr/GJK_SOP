import random
from position import Punkt
from figurer import Figur

def convex_hull(points):
    """Return points on the convex hull in counter-clockwise order."""
    # Sort by x, then y
    points = sorted(points)

    # Cross product helper
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate (omit duplicate endpoints)
    return lower[:-1] + upper[:-1]

def random_convex_polygon(num_points, spread=6):
    """
    Generate a convex polygon with approximately num_points vertices.
    Returns the hull (list of (x, y) tuples).
    """
    # Generate more points than needed—hull will pick only outer ones
    raw_points = [
        (random.uniform(-spread, spread), random.uniform(-spread, spread))
        for _ in range(num_points)
    ]

    points = list(map(lambda p: Punkt(p[0], p[1]), convex_hull(raw_points)))

    return Figur(points)