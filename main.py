import array

import pygame
import math

from konstanter import *
from pygameHelper import til_skærm
from figurer import *

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((VINDUEBREDDE, VINDUEHØJDE))
scale = VINDUEHØJDE / 100
canvas = pygame.Surface((VINDUEBREDDE, VINDUEHØJDE))

figurer = []

rotate = Matrix([
    [math.cos(math.degrees(30)), -math.sin(math.degrees(30))],
    [math.sin(math.degrees(30)), math.cos(math.degrees(30))]
])

figur1 = Figur([Punkt(4,11), Punkt(9,9), Punkt(4,5)])
figur2 = Figur([Punkt(5, 7), Punkt(12, 7), Punkt(10, 2), Punkt(7, 3)])

skalere = Matrix([
    [30, 0],
    [0, 30]
])

#TODO: lav kode som kan bruges til at teste hvor hurtig algoritmen er

figur1.tilføjTransformation(skalere)
figur2.tilføjTransformation(skalere)
figur1.centrum *= 30
figur2.centrum *= 30

figurer.append(figur1)
figurer.append(figur2)

def start():
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                print(tjekKollision(figur1, figur2))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                figur2.centrum.x -= 10
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                figur2.centrum.x += 10

        canvas.fill((255, 255, 255))
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(-VINDUEBREDDE / 2, 0), til_skærm(VINDUEBREDDE / 2, 0),
                         2)  # vandret linje
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(0, -VINDUEHØJDE / 2), til_skærm(0, VINDUEHØJDE / 2),
                         2)  # lodret linje

        pygame.draw.circle(canvas, (0, 0, 0), til_skærm(0, 0), 10)

        for figur in figurer:
            figur.tegn(canvas)

        window.set_clip(pygame.Rect((0, 0), (VINDUEBREDDE, VINDUEHØJDE)))
        window.blit(canvas, (0, 0))
        pygame.display.update()



from gjk_funkioner import support

def tjekKollision(figur1: Figur, figur2: Figur) -> bool:
    simplex = Simplex()
    # Der vælges en søge retning mod figur2 fra figur1
    r = Vektor(figur2.centrum.x - figur1.centrum.x,
               figur2.centrum.y - figur1.centrum.y).enhed_vektor()
    # Får første minkowski difference punkt
    simplex.tilføj(support(figur1,figur2, r))

    r = -r # gør den anden retning for næste punkt

    while True:
        # tilføjer nyt punkt
        simplex.tilføj(support(figur1, figur2, r))

        # sikre at det nyeste tilføjet punkt faktisk passerede origo
        if (simplex.fåSeneste().dot(r) <= 0):
            # det betyder at punktet passerede ikke origo
            # dette betyder at det er umuligt at lave en trekant som indeholder origo
            # da vi altid laver punkter på kanten af minkowski differencen
            return False
        else:
            if (simplex.indeholder(Punkt(0,0), r)):
                return True

if __name__ == '__main__':
    start()