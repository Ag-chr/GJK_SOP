import math

import pygame

from matrix import Matrix
from position import Punkt, Vektor, vektorTripelProdukt
from pygameHelper import til_skærm

class Figur:
    def __init__(self, punkter: [Punkt]):
        self.punkter = punkter
        self.centrum = sum(punkter, Punkt(0, 0)) / len(punkter)  # punkt som beskriver centrum af figuren

        self.punkter = list(map(lambda punkt: punkt - self.centrum, self.punkter))  # justere figuren så origo er figurens centrum
        self.transformationer = [Matrix([[1,0],[0,1]])]
        self.komposition = Matrix([[1,0],[0,1]])

    def fåPunkt(self, index):
        return self.regn_punkt_transformation(self.punkter[index]) + self.centrum

    def tilVerden(self, punkt: Punkt):
        return self.regn_punkt_transformation(punkt) + self.centrum

    def fåPunktLængstVækIEnRetning(self, r: Vektor) -> Punkt:
        PunktLængstVæk = self.punkter[0]
        maksSkalar = 0
        for punkt in self.punkter:
            skalarProdukt = punkt.dot(r)
            if skalarProdukt > maksSkalar:
                maksSkalar = skalarProdukt
                PunktLængstVæk = punkt

        return self.tilVerden(PunktLængstVæk)

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
        return punkt

    def tegn(self, canvas):
        # beregn transformation for punkter

        # tegn nye punkter på skærm
        tidligerePunkt = self.fåPunkt(0).tuple()
        pygame.draw.circle(canvas, (0,0,0), til_skærm(tidligerePunkt), 3)
        for punkt in self.punkter:  # springer over første punkt
            punkt = self.tilVerden(punkt).tuple()

            pygame.draw.circle(canvas, (0, 0, 0), til_skærm(punkt), 3)
            pygame.draw.line(canvas, (0,0,0), til_skærm(tidligerePunkt), til_skærm(punkt), 2)

            tidligerePunkt = punkt
        pygame.draw.line(canvas, (0, 0, 0), til_skærm(tidligerePunkt), til_skærm(self.fåPunkt(0).tuple()), 2)


class Simplex:
    def __init__(self):
        self.punkter = []

    def tilføj(self, punkt: Punkt):
        self.punkter.insert(0, punkt)

    def fjern(self, punkt: Punkt):
        self.punkter.remove(punkt)

    # få seneste tilføjet punkt
    def fåSeneste(self) -> Punkt:
        return self.punkter[0]

    def fåB(self) -> Punkt:
        return self.punkter[1]

    def fåC(self) -> Punkt:
        return self.punkter[2]

    # se om simplex indeholder punktet
    def indeholder(self, punkt: Punkt, r: Vektor):
        a = self.fåSeneste()

        ao = Punkt(0,0) - a
        if (len(self.punkter) == 3):
            b = self.fåB()
            c = self.fåC()

            ab = b - a
            ac = c - a

            abVinkelret = vektorTripelProdukt(ac, ab, ab)
            acVinkelret = vektorTripelProdukt(ab, ac, ac)

            if abVinkelret.dot(ao) > 0:
                self.fjern(c)
                r.sæt(abVinkelret)
            else:
                if acVinkelret.dot(ao) > 0:
                    self.fjern(b)
                    r.sæt(acVinkelret)
                else:
                    return True

        else: # betyder at det er et linje segment
            b = self.fåB()

            ab = b - a
            abVinkelret = vektorTripelProdukt(ab, ao, ab)

            r.sæt(abVinkelret)
        return False

    def __repr__(self):
        return f"Punkter: {self.punkter}"


class Cirkel(Figur):
    def __init__(self, radius, pos: Punkt):
        super().__init__([Punkt(0, 0)])
        self.centrum = pos
        self.radius = radius


    def tegn(self, canvas):
        pygame.draw.circle(canvas, (0, 0, 0), til_skærm(self.centrum.tuple()), self.radius, 2)

    def fåPunktLængstVækIEnRetning(self, r: Vektor) -> Punkt:
        _, vinkel = r.polær_vektor()
        x = self.radius * math.cos(vinkel)
        y = self.radius * math.sin(vinkel)

        return Punkt(x, y) + self.centrum


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

    a = Vektor(3, 2)
    b = Vektor(5, 3)
    c = Vektor(2, 6)

    print(f"kryds: {a.kryds(b).kryds(c)}")
    print(f"anden formel: {b*(c.dot(a)) - (a*(c.dot(b)))}")


