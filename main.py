import array

import pygame
import math

from konstanter import *
from pygameHelper import til_skærm
from figurer import *
from gjk_funkioner import minkowski
from kollision import tjekKollisionGJK, tjekKollisionAABB

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((VINDUEBREDDE, VINDUEHØJDE))
scale = VINDUEHØJDE / 100
canvas = pygame.Surface((VINDUEBREDDE, VINDUEHØJDE))
font = pygame.font.Font(None, 36)

text = font.render(f"Kollision: {False}", True, (0, 0, 0))
text_rect = text.get_rect(topleft=(10, 10))

figurer = []

rotate = Matrix([
    [math.cos(math.degrees(30)), -math.sin(math.degrees(30))],
    [math.sin(math.degrees(30)), math.cos(math.degrees(30))]
])

figur1 = Figur([Punkt(4,11), Punkt(9,9), Punkt(4,5)])
figur2 = Figur([Punkt(5, 7), Punkt(10, 2), Punkt(12, 7), Punkt(7, 3)])
cirkel = Cirkel(30, Punkt(0,100))



skalere = Matrix([
    [30, 0],
    [0, 30]
])

figur1.tilføjTransformation(skalere)
figur2.tilføjTransformation(skalere)

figur1.centrum *= 30
figur2.centrum *= 30

minkowskiFigur = minkowski(figur1, figur2, False)


figurer.append(figur1)
figurer.append(figur2)
#figurer.append(cirkel)
#figurer.append(minkowskiFigur)


def start():
    holderFigur = False
    holdtFigur = None

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = list(event.pos)
                pos[0] -= VINDUEBREDDE // 2
                pos[1] = -(pos[1] - VINDUEHØJDE // 2)
                cirkel = Cirkel(5, Punkt(pos[0], pos[1]))

                for figur in figurer:
                    tjekKollisionGJK(cirkel, figur)
                    if tjekKollisionGJK(Cirkel(1, Punkt(pos[0], pos[1])), figur):
                        holderFigur = True
                        holdtFigur = figur
                        break

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                holderFigur = False
                holdtFigur = None

            elif event.type == pygame.MOUSEMOTION and holderFigur:
                bevægelse = event.rel
                holdtFigur.centrum.x += bevægelse[0]
                holdtFigur.centrum.y -= bevægelse[1]

        canvas.fill((255, 255, 255))
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(-VINDUEBREDDE / 2, 0), til_skærm(VINDUEBREDDE / 2, 0),
                         2)  # x akse
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(0, -VINDUEHØJDE / 2), til_skærm(0, VINDUEHØJDE / 2),
                         2)  # y akse
        #pygame.draw.circle(canvas, (0, 0, 0), til_skærm(0, 0), 10)  # origo

        for figur in figurer:
            figur.tegn(canvas)

        kollision = False
        for i in range(len(figurer)):
            for j in range(i+1, len(figurer)):
                figur1 = figurer[i]
                figur2 = figurer[j]

                if tjekKollisionAABB(figur1, figur2):
                    kollision = True
                    figur1.tegn(canvas, (255, 0, 0))
                    figur2.tegn(canvas, (255, 0, 0))

        text = font.render(f"Kollision: {kollision}", True, (0, 0, 0))

        canvas.blit(text, text_rect)
        window.set_clip(pygame.Rect((0, 0), (VINDUEBREDDE, VINDUEHØJDE)))
        window.blit(canvas, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    start()