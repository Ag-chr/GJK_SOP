from figurer import *
from gjk_funkioner import support
import pygame

def tjekKollisionGJK(figur1: Figur, figur2: Figur) -> bool:
    simplex = Simplex()
    # Der vælges en søge retning mod figur2 fra figur1
    r = Vektor(figur2.centrum.x - figur1.centrum.x,
               figur2.centrum.y - figur1.centrum.y).enhedsvektor()
    # Får første minkowski difference punkt
    simplex.tilføj(support(figur1,figur2, r))

    r = -r # går den modsatte retning for næste punkt

    while True:
        # tilføjer nyt punkt
        simplex.tilføj(support(figur1, figur2, r))

        # sikre at det nyeste tilføjet punkt faktisk passerede origo
        if simplex.fåSeneste().dot(r) <= 0:
            # det betyder at punktet passerede ikke origo
            # dette betyder at det er umuligt at lave en trekant som indeholder origo
            # da vi altid laver punkter på kanten af minkowski differencen
            return False
        else:
            if simplex.indeholder(Punkt(0,0), r):
                return True

def tjekKollisionAABB(figur1: Figur, figur2: Figur) -> bool:
    min1, max1 = figur1.få_min_max()
    min2, max2 = figur2.få_min_max()

    d1x = min2.x - max1.x
    d1y = min2.y - max1.y
    d2x = min1.x - max2.x
    d2y = min1.y - max2.y

    if d1x > 0 or d1y > 0:
        return False
    if d2x > 0 or d2y > 0:
        return False

    return True