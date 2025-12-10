import math

import pygame

from matrix import Matrix
from position import Punkt, Vektor, vektorTripelProdukt
from pygameHelper import til_skærm
from konstanter import ZOOM

class Figur:
    def __init__(self, punkter: list[Punkt]):
        self.punkter = punkter
        self.centrum = sum(punkter, Punkt(0, 0)) / len(punkter)  # punkt som beskriver centrum af figuren

        # justere figuren så origo er figurens centrum i dens koordinatsystem
        self.punkter = list(map(lambda punkt: punkt - self.centrum, self.punkter))
        self.punkter: list[Punkt] = self.sorterePunkterMedUret() # så den kan tegnes
        self.transformationer = [Matrix.IDENTITET_2D()]
        self.komposition = Matrix.IDENTITET_2D()

    def fåPunkt(self, index):
        return self.tilVerden(self.punkter[index])

    def tilVerden(self, punkt: Punkt):
        return self.regnPunktTransformation(punkt) + self.centrum

    def fåPunktLængstVækIEnRetning(self, r: Vektor) -> Punkt:
        PunktLængstVæk = self.punkter[0]
        maksSkalar = 0
        for punkt in self.punkter:
            punkt_trans = self.regnPunktTransformation(punkt)
            skalarProdukt = punkt_trans.dot(r)
            if skalarProdukt > maksSkalar:
                maksSkalar = skalarProdukt
                PunktLængstVæk = punkt

        return self.tilVerden(PunktLængstVæk)

    def tilføjTransformation(self, matrix: Matrix):
        # tjekker om matrix er rigtig størrelse (et 2x2 matrix)
        if matrix.rækker() != 2 and matrix.søjler() != 2:
            return -1

        self.transformationer.append(matrix)
        self.regnKompositionMatrix()

    def fjernTransformation(self, num=-1):
        if num == 0 or len(self.transformationer) == 1:
            return
        self.transformationer.pop(num)
        self.regnKompositionMatrix()

    def regnKompositionMatrix(self):
        komposition = self.transformationer[0]
        # går baglæns og fjerner den sidste tilføjet til listen
        for transformation in self.transformationer[1::]:
            komposition = transformation * komposition
        self.komposition = komposition

    def regnPunktTransformation(self, punkt: Punkt):
        søjle_v = punkt.til_søjlevektor()
        søjle_v = self.komposition * søjle_v
        punkt = Punkt(søjle_v[0][0], søjle_v[1][0])
        return punkt

    def tegn(self, canvas, farve=(0,0,0)):
        # beregn transformation for punkter

        # tegn nye punkter på skærm
        tidligerePunkt = (self.fåPunkt(0) * ZOOM).tuple()
        pygame.draw.circle(canvas, farve, til_skærm(tidligerePunkt), 3)
        for punkt in self.punkter[1::]:  # springer over første punkt
            punkt = (self.tilVerden(punkt) * ZOOM).tuple()


            pygame.draw.circle(canvas, farve, til_skærm(punkt), 3)
            pygame.draw.line(canvas, farve, til_skærm(tidligerePunkt), til_skærm(punkt), 2)

            tidligerePunkt = punkt
        pygame.draw.line(canvas, farve, til_skærm(tidligerePunkt), til_skærm((self.fåPunkt(0) * ZOOM).tuple()), 2)

    def sorterePunkterMedUret(self):
        vinkel_fra_midten = lambda p: math.atan2(p.y, p.x)

        sorteretPunkter = sorted(self.punkter, key=vinkel_fra_midten, reverse=True)
        return sorteretPunkter

    def få_min_max(self):
        x_max = 0
        x_min = math.inf
        y_max = 0
        y_min = math.inf
        for punkt in self.punkter:
            x, y = til_skærm(self.tilVerden(punkt).tuple())
            if x > x_max: x_max = x
            if x < x_min: x_min = x
            if y > y_max: y_max = y
            if y < y_min: y_min = y

        return Punkt(x_min, y_min), Punkt(x_max, y_max)


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

        ao = punkt - a
        if (len(self.punkter) == 3):
            b = self.fåB()
            c = self.fåC()

            ab = b - a
            ac = c - a

            abVinkelret = vektorTripelProdukt(ac, ab, ab)
            acVinkelret = vektorTripelProdukt(ab, ac, ac)

            # hvis origo er ud mod linje ab så fjernes c og der gås videre i denne retning
            if abVinkelret.dot(ao) > 0:
                self.fjern(c)
                r.sæt(abVinkelret)
            else:
                # hvis origo er ud mod linje ac så fjernes b og der gås videre i denne retning
                if acVinkelret.dot(ao) > 0:
                    self.fjern(b)
                    r.sæt(acVinkelret)
                # hvis der nås hertil betyder det at origo er inde i trekant og dermed krydser figurerne
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


    def tegn(self, canvas, farve=(0,0,0)):
        x_tidligere = self.radius * math.cos(0)
        y_tidligere = self.radius * math.sin(0)
        for vinkel in range(5, 360, 5):
            x = self.radius * math.cos(vinkel)
            y = self.radius * math.sin(vinkel)
            pygame.draw.line(canvas, farve, (x_tidligere, y_tidligere), (x, y))
            x_tidligere = x
            y_tidligere = y

        pygame.draw.circle(canvas, farve, til_skærm(self.centrum.tuple()*ZOOM), self.radius, 2)

    def fåPunktLængstVækIEnRetning(self, r: Vektor) -> Punkt:
        _, vinkel = r.polær_vektor()
        x = self.radius * math.cos(vinkel)
        y = self.radius * math.sin(vinkel)

        return self.tilVerden(Punkt(x, y))




class RegulærPolygon(Figur):
    def __init__(self, antal_punkter, størrelse):
        grader_mellem_punkter = math.radians(360) / antal_punkter
        punkter = []
        for i in range(antal_punkter):
            x = math.cos(i*grader_mellem_punkter +grader_mellem_punkter/2 - math.radians(90)) * størrelse
            y = math.sin(i*grader_mellem_punkter +grader_mellem_punkter/2 - math.radians(90)) * størrelse

            punkter.append(Punkt(x,y))

        super().__init__(punkter)


if __name__ == '__main__':
    figur = Figur([Punkt(0,0), Punkt(2,0), Punkt(2,2), Punkt(0,2)])
    shear = Matrix([
        [1, 2],
        [0, 1]
    ])
    figur.tilføjTransformation(shear)
    print(figur.komposition)
    print(figur.punkter[0])
    print(figur.regnPunktTransformation(figur.punkter[0]))

    a = Vektor(3, 2)
    b = Vektor(5, 3)
    c = Vektor(2, 6)

    print(f"kryds: {a.kryds(b).kryds(c)}")
    print(f"anden formel: {b*(c.dot(a)) - (a*(c.dot(b)))}")


