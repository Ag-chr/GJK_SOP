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

    r = -r # gør den anden retning for næste punkt

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


def tjekKollisionAABB(figur1: Figur, figur2: Figur, canvas) -> bool:
    rect1 = figur1.get_rect()
    x1, y1, bredde1, højde1 = rect1
    pygame.draw.rect(canvas, (0, 0, 255), rect1, 2)


    rect2 = figur2.get_rect()
    x2, y2, bredde2, højde2 = rect2
    pygame.draw.rect(canvas, (0,0,255), rect2, 2)

    if (x1 < x2 + bredde2 and
        x1 + bredde1 > x2 and
        y1 < y2 + højde2 and
        y1 + højde1 > y2):
        return True
    else:
        return False
