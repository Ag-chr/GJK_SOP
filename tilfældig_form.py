import random
import math

from matrix import Matrix
from former import RegulærPolygon

rand_interval = lambda: random.uniform(-2, -0.5) if random.random() < 0.5 else random.uniform(0.5, 2)
def tilfældig_regulær_polygon(punkter, størrelse):
    stræk = Matrix([
        [rand_interval(), 0],
        [0, rand_interval()]
    ])
    skewx = Matrix([
        [1, rand_interval() / 2],
        [0, 1]
    ])
    skewy = Matrix([
        [1, 0],
        [rand_interval() / 2, 1]
    ])
    rand_vinkel = math.radians(random.uniform(0, 360))
    rotation = Matrix([
        [math.cos(rand_vinkel), -math.sin(rand_vinkel)],
        [math.sin(rand_vinkel), math.cos(rand_vinkel)]
    ])

    regpol = RegulærPolygon(punkter, størrelse)
    regpol.tilføjTransformation(stræk)
    regpol.tilføjTransformation(skewx)
    regpol.tilføjTransformation(skewy)
    regpol.tilføjTransformation(rotation)
    return regpol

