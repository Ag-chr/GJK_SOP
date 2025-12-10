import array
import random

import pygame
import math
import pickle

from konstanter import *
from pygameHelper import til_skærm
from figurer import *
from gjk_funkioner import minkowski
from kollision import tjekKollisionGJK, tjekKollisionAABB
from tilfældig_figur import random_convex_polygon

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((VINDUEBREDDE, VINDUEHØJDE))
scale = VINDUEHØJDE / 100
canvas = pygame.Surface((VINDUEBREDDE, VINDUEHØJDE))
font = pygame.font.Font(None, 36)

text_kollision = font.render(f"Kollision: {False}", True, (0, 0, 0))
text_rect_kollision = text_kollision.get_rect(topleft=(10, 10))

figurer = []

rotate = Matrix([
    [math.cos(math.degrees(360)), -math.sin(360)],
    [math.sin(math.degrees(360)), math.cos(math.degrees(360))]
])

figur1 = Figur([Punkt(4,11), Punkt(9,9), Punkt(4,5)])
figur2 = Figur([Punkt(5, 7), Punkt(10, 2), Punkt(12, 7), Punkt(7, 3)])
cirkel = Cirkel(30, Punkt(0,5))


figur1.tilføjTransformation(rotate)

figurer.append(figur1)
figurer.append(figur2)
figurer.append(cirkel)

minkowskiFigur = minkowski(figur1, figur2, False)
#figurer.append(minkowskiFigur)

testFigurer: list[(Figur, Figur)] = []

filnavn = "10kant.pkl"

def start():
    global testFigurer
    holdtFigur = None

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    fig = random_convex_polygon(5, scale=random.uniform(2.5, 5.5), max_attempts=20)
                    fig.centrum = Punkt(random.uniform(-6, 6), random.uniform(-6, 6))
                    figurer.append(fig)

                elif event.key == pygame.K_p:
                    figurer.pop()
                elif event.key == pygame.K_o:
                    testFigurer.append((figurer.pop(), figurer.pop()))
                elif event.key == pygame.K_s:
                    print("save")
                    with open(filnavn, "wb") as f:
                        pickle.dump(testFigurer, f)
                elif event.key == pygame.K_l:
                    with open(filnavn, "rb") as f:
                        data = pickle.load(f)
                        print(len(data))
                        print(len(data[0]))
                elif event.key == pygame.K_h:
                    with open(filnavn, "rb") as f:
                        testFigurer = pickle.load(f)



            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = list(event.pos)
                mouse_pos[0] -= (VINDUEBREDDE // 2)
                mouse_pos[0] /= ZOOM
                mouse_pos[1] = -(mouse_pos[1] - VINDUEHØJDE // 2)
                mouse_pos[1] /= ZOOM
                cirkel = Cirkel(1, Punkt(mouse_pos[0], mouse_pos[1]))

                for figur in figurer:
                    tjekKollisionGJK(cirkel, figur)
                    if tjekKollisionGJK(Cirkel(1, Punkt(mouse_pos[0], mouse_pos[1])), figur):
                        holdtFigur = figur
                        break

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                holdtFigur = None

            elif event.type == pygame.MOUSEMOTION and holdtFigur is not None:
                bevægelse = event.rel
                holdtFigur.centrum.x += bevægelse[0] / ZOOM
                holdtFigur.centrum.y -= bevægelse[1] / ZOOM

        canvas.fill((255, 255, 255))
        pygame.draw.line(canvas, (100, 100, 100), (0, VINDUEHØJDE / 2), (VINDUEBREDDE, VINDUEHØJDE / 2),
                         2)  # x akse
        pygame.draw.line(canvas, (100, 100, 100), (VINDUEBREDDE / 2, 0), (VINDUEBREDDE / 2, VINDUEHØJDE),
                         2)  # y akse
        #pygame.draw.circle(canvas, (0, 0, 0), (VINDUEBREDDE / 2, VINDUEHØJDE / 2), 10)  # origo

        for figur in figurer:
            figur.tegn(canvas)

        kollision = False
        for i in range(len(figurer)):
            for j in range(i+1, len(figurer)):
                figur1 = figurer[i]
                figur2 = figurer[j]

                if tjekKollisionGJK(figur1, figur2):
                    kollision = True
                    figur1.tegn(canvas, (255, 0, 0))
                    figur2.tegn(canvas, (255, 0, 0))

        text_kollision = font.render(f"Kollision: {kollision}", True, (0, 0, 0))

        text = font.render(f"størrelse: {len(testFigurer)}", True, (0, 0, 0))
        text_rect = text.get_rect(topleft=(10, 40))
        canvas.blit(text, text_rect)

        text = font.render(f"filnavn: {filnavn}", True, (0, 0, 0))
        text_rect = text.get_rect(topleft=(10, 70))
        canvas.blit(text, text_rect)

        canvas.blit(text_kollision, text_rect_kollision)
        window.set_clip(pygame.Rect((0, 0), (VINDUEBREDDE, VINDUEHØJDE)))
        window.blit(canvas, (0, 0))
        pygame.display.update()






if __name__ == '__main__':
    start()