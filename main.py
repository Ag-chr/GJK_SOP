import pygame
import math

from konstanter import *
from pygameHelper import til_skærm
from figurer import *

pygame.init()
clock = pygame.time.Clock()
running = True

window = pygame.display.set_mode((VINDUEBREDDE, VINDUEHØJDE))
scale = VINDUEHØJDE / 100
canvas = pygame.Surface((VINDUEBREDDE, VINDUEHØJDE))

figurer = []

"""
figur = Figur([Punkt(-100, 100), Punkt(100, 100), Punkt(100, -100), Punkt(-100, -100)])
figur.centrum = Punkt(0, 0)

rotate = Matrix([
    [math.cos(math.degrees(30)), -math.sin(math.degrees(30))],
    [math.sin(math.degrees(30)), math.cos(math.degrees(30))]
])

figur.tilføjTransformation(rotate)"""

figur1 = Figur([Punkt(4,11), Punkt(9,9), Punkt(4,5)])
figur2 = Figur([Punkt(5, 7), Punkt(12, 7), Punkt(10, 2), Punkt(7, 3)])

skalere = Matrix([
    [30, 0],
    [0, 30]
])
figur1.tilføjTransformation(skalere)
figur2.tilføjTransformation(skalere)
figur1.centrum.x *= 30
figur1.centrum.y *= 30
figur2.centrum.x *= 30
figur2.centrum.y *= 30


figurer.append(figur1)
figurer.append(figur2)


if __name__ == '__main__':
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        canvas.fill((255, 255, 255))
        pygame.draw.line(canvas, (0,0,0), til_skærm(-VINDUEBREDDE/2, 0), til_skærm(VINDUEBREDDE/2, 0), 2) # vandret linje
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(0, -VINDUEHØJDE / 2), til_skærm(0, VINDUEHØJDE / 2),2)  # lodret linje

        pygame.draw.circle(canvas, (0,0,0), til_skærm(0, 0), 10)

        for figur in figurer:
            figur.tegn(canvas)

        window.set_clip(pygame.Rect((0, 0), (VINDUEBREDDE, VINDUEHØJDE)))
        window.blit(canvas, (0, 0))
        pygame.display.update()