import pygame

from matrix import Matrix
from position import Punkt, Vektor
from pygameHelper import til_skærm


class Figur:
    def __init__(self, punkter: [Punkt]):
        self.punkter = punkter
        self.centrum = sum(punkter, Punkt(0, 0)) / len(punkter)  # punkt som beskriver centrum af figuren

        self.punkter = list(map(lambda punkt: punkt - self.centrum, self.punkter))  # justere figuren så origo er figurens centrum
        self.transformationer = [Matrix([[1,0],[0,1]])]
        self.komposition = Matrix([[1,0],[0,1]])


    def fåPunktLængstVækIEnRetning(self, r: Vektor) -> Punkt:
        PunktLængstVæk = self.punkter[0]
        maksSkalar = 0
        for punkt in self.punkter[1::]:  # [1::] springer over første punkt
            skalarProdukt = punkt.dot(r)
            if skalarProdukt > maksSkalar:
                maksSkalar = skalarProdukt
                PunktLængstVæk = punkt

        return PunktLængstVæk

    def tilføjTransformation(self, matrix: Matrix):
        # tjekker om matrix er rigtig størrelse (et 2x2 matrix)
        if matrix.rækker() != 2 and matrix.søjler() != 2:
            return -1

        self.transformationer.append(matrix)
        self.regnKomposition()

    def fjernTransformation(self, num=-1):
        if num == 0 or len(self.transformationer) == 1:
            return
        self.transformationer.pop(num)
        self.regnKomposition()

    def regnKomposition(self):
        komposition = self.transformationer[0]
        # går baglæns og fjerner den sidste tilføjet til listen
        for transformation in self.transformationer[1::]:
            komposition = transformation * komposition
        self.komposition = komposition

    def regn_punkt_transformation(self, punkt: Punkt):
        søjle_v = punkt.til_søjlevektor()
        søjle_v = self.komposition * søjle_v
        punkt = Punkt(søjle_v[0][0], søjle_v[1][0])
        return punkt + self.centrum

    def tegn(self, canvas):
        # beregn transformation for punkter

        # tegn nye punkter på skærm
        tidligerePunkt = self.regn_punkt_transformation(self.punkter[0]).tuple()
        pygame.draw.circle(canvas, (0,0,0), til_skærm(tidligerePunkt), 5)
        for punkt in self.punkter[1::]: # [1::] springer over første punkt
            punkt = self.regn_punkt_transformation(punkt).tuple()
            pygame.draw.circle(canvas, (0, 0, 0), til_skærm(punkt), 5)
            pygame.draw.line(canvas, (0,0,0), til_skærm(tidligerePunkt), til_skærm(punkt), 2)
            tidligerePunkt = punkt
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(tidligerePunkt), til_skærm(self.regn_punkt_transformation(self.punkter[0]).tuple()), 2)


class Simplex:
    def __init__(self):
        self.punkter = []

    def tilføj(self, punkt: Punkt):
        self.punkter.insert(0, punkt)

    # få seneste tilføjet punkt
    def fåSeneste(self) -> Punkt:
        return self.punkter[0]

    # se om simplex indeholder punktet
    def indeholder(self, punkt: Punkt):
        pass


if __name__ == '__main__':


    figur = Figur([Punkt(0,0), Punkt(2,0), Punkt(2,2), Punkt(0,2)])
    shear = Matrix([
        [1, 2],
        [0, 1]
    ])
    figur.tilføjTransformation(shear)
    print(figur.komposition)
    print(figur.punkter[0])
    print(figur.regn_punkt_transformation(figur.punkter[0]))

