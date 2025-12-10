from former import *
from gjk_funkioner import support
import pygame

def tjekKollisionGJK(form1: Form, form2: Form) -> bool:
    simplex = Simplex()
    # Der vælges en søge retning mod form2 fra form1
    r = Vektor(form2.centrum.x - form1.centrum.x,
               form2.centrum.y - form1.centrum.y).enhedsvektor()
    # Får første minkowski difference punkt
    simplex.tilføj(support(form1,form2, r))

    r = -r # går den modsatte retning for næste punkt

    while True:
        # tilføjer nyt punkt
        simplex.tilføj(support(form1, form2, r))

        # sikre at det nyeste tilføjet punkt faktisk passerede origo
        if simplex.fåSeneste().dot(r) <= 0:
            # det betyder at punktet passerede ikke origo
            # dette betyder at det er umuligt at lave en trekant som indeholder origo
            # da vi altid laver punkter på kanten af minkowski differencen
            return False
        else:
            if simplex.indeholder(Punkt(0,0), r):
                return True

def tjekKollisionAABB(form1: Form, form2: Form) -> bool:
    min1, max1 = form1.få_min_max()
    min2, max2 = form2.få_min_max()

    d1x = min2.x - max1.x
    d1y = min2.y - max1.y
    d2x = min1.x - max2.x
    d2y = min1.y - max2.y

    if d1x > 0 or d1y > 0:
        return False
    if d2x > 0 or d2y > 0:
        return False

    return True