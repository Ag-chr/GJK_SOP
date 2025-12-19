import array
import random

import pygame
import math
import pickle

from konstanter import *
from pygameHelper import til_skærm
from former import *
from gjk_funkioner import minkowski
from kollision import tjekKollisionGJK, tjekKollisionAABB
from tilfældig_form import *

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((VINDUEBREDDE, VINDUEHØJDE))
scale = VINDUEHØJDE / 100
canvas = pygame.Surface((VINDUEBREDDE, VINDUEHØJDE))
font = pygame.font.Font(None, 36)

former: list[Form] = []

stræk = Matrix([
    [1, 0],
    [0, 2]
])

polygon1 = Form([Punkt(4, 11), Punkt(9, 9), Punkt(4, 5)])
polygon2 = Form([Punkt(7, 11), Punkt(12, 6), Punkt(14, 11), Punkt(9, 7)])
minkowskiForm = minkowski(polygon1, polygon2, False)
cirkel = Cirkel(3, Punkt(0,5))
#polygon2.tilføjTransformation(stræk)

former.append(polygon2)
former.append(polygon1)
#former.append(minkowskiForm)


def start():
    global former
    holdtForm = None

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:

                former.append(tilfældig_regulær_polygon(7, 2.5))


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                import timeit
                tjekKollisionGJK(polygon1, polygon2)
                print(timeit.timeit(lambda: tjekKollisionGJK(polygon1, polygon2), number=10000))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                former.pop()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                print("form1", round(former[-1].centrum.x, 1), round(former[-1].centrum.y, 1))
                print("form2", round(former[-2].centrum.x, 1), round(former[-2].centrum.y, 1))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                with open(f"forme/3kant.pkl", "rb") as f:
                    former = pickle.load(f)


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = list(event.pos)
                mouse_pos[0] -= (VINDUEBREDDE // 2)
                mouse_pos[0] /= ZOOM
                mouse_pos[1] = -(mouse_pos[1] - VINDUEHØJDE // 2)
                mouse_pos[1] /= ZOOM
                cirkel = Cirkel(1, Punkt(mouse_pos[0], mouse_pos[1]))

                for form in former:
                    tjekKollisionGJK(cirkel, form)
                    if tjekKollisionGJK(Cirkel(1, Punkt(mouse_pos[0], mouse_pos[1])), form):
                        holdtForm = form
                        break

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                holdtForm = None

            elif event.type == pygame.MOUSEMOTION and holdtForm is not None:
                bevægelse = event.rel
                holdtForm.centrum.x += bevægelse[0] / ZOOM
                holdtForm.centrum.y -= bevægelse[1] / ZOOM

        canvas.fill((255, 255, 255))
        pygame.draw.line(canvas, (100, 100, 100), (0, VINDUEHØJDE / 2), (VINDUEBREDDE, VINDUEHØJDE / 2),
                         2)  # x akse
        pygame.draw.line(canvas, (100, 100, 100), (VINDUEBREDDE / 2, 0), (VINDUEBREDDE / 2, VINDUEHØJDE),
                         2)  # y akse

        for form in former:
            form.tegn(canvas)

        kollision = False
        for i in range(len(former)):
            for j in range(i+1, len(former)):
                form1 = former[i]
                form2 = former[j]

                if tjekKollisionGJK(form1, form2):
                    kollision = True
                    form1.tegn(canvas, (255, 0, 0))
                    form2.tegn(canvas, (255, 0, 0))

        polygon2.tegn(canvas, (221, 82, 204))
        polygon1.tegn(canvas, (32, 189, 255))


        text_kollision = font.render(f"Kollision: {kollision}", True, (0, 0, 0))
        text_rect_kollision = text_kollision.get_rect(topleft=(10, 10))

        canvas.blit(text_kollision, text_rect_kollision)
        window.set_clip(pygame.Rect((0, 0), (VINDUEBREDDE, VINDUEHØJDE)))
        window.blit(canvas, (0, 0))
        pygame.display.update()






if __name__ == '__main__':
    start()