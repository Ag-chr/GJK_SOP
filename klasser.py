import math
from copy import deepcopy


class Matrix:
    def __init__(self, matrix: [[float]]):
        if type(matrix) != list and type(matrix[0]) != list and type(matrix[0][0]) not in [float, int]:
            raise "matrix er ikke en nested list af floats"
        self.matrix = matrix

    def transponere(self):
        pass

    def rækker(self):
        return len(self.matrix)

    def søjler(self):
        return len(self.matrix[0])

    def få_søjler(self):
        for i in range(self.søjler()):
            søjle = []
            for j in range(self.rækker()):
                søjle.append(self.matrix[j][i])
            yield søjle


    def __repr__(self):
        s = "Matrix(\n"
        for række in self.matrix:
            s = s + f"  {række}\n"
        s = s + ")"
        return s

    def __add__(self, other):
        matrix = deepcopy(self.matrix)

        # tjekker om det er et tal
        if type(other) in [float, int]:
            for række in range(self.rækker()):
                for søjle in range(self.søjler()):
                    matrix[række][søjle] = matrix[række][søjle] + other
            return Matrix(matrix)

        if type(other) != __class__:
            raise "Kan kun lægge matrix sammen med et andet matrix eller et float eller int"

        # tjekkes om det er et matrix
        if other.rækker() != self.rækker() and other.søjler() != self.søjler():
            raise "Matricer er ikke af samme type"

        for række in range(self.rækker()):
            for søjle in range(self.søjler()):
                matrix[række][søjle] = matrix[række][søjle] + other.matrix[række][søjle]
        return Matrix(matrix)

    def __mul__(self, other):
        # tjekker om det er en skalar
        if type(other) in [float, int]:
            matrix = deepcopy(self.matrix)
            for m in range(self.rækker()):
                for n in range(self.søjler()):
                    matrix[m][n] = matrix[m][n] * other
            return matrix

        if self.søjler() != other.rækker():
            raise "kan ikke ganges sammen"


        matrix = []
        for _ in range(self.rækker()):
            matrix.append([])

        for p, vektor_søjle in enumerate(other.få_søjler()): # laver andet matrix til vektor søjler og iterer igennem dem
            # hver række element ganges med henholdsvis hver vektor_søjle element
            for (m, række) in enumerate(self.matrix):
                matrix[m].append(0)
                for n, element in enumerate(række):
                    matrix[m][p] += vektor_søjle[n] * self.matrix[m][n]

        return Matrix(matrix)

    def __getitem__(self, index):
        return self.matrix[index]

class Position:
    def __init__(self, x: float, y: float, z: float=0):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def tuple(self):
        return self.x, self.y

    def til_søjlevektor(self, til_3d=False):
        if til_3d:
            return Matrix([
                [self.x],
                [self.y],
                [self.z]
            ])
        else:
            return Matrix([
                [self.x],
                [self.y]
            ])

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return self.__class__(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return self.__class__(x, y, z)

    def __truediv__(self, other):
        if type(other) in [int, float]:
            x = self.x / other
            y = self.y / other
            z = self.z / other
        else:
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        return self.__class__(x, y, z)

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    def __ne__(self, other):
        if not (self.x == other.x and self.y == other.y and self.z == other.z):
            return True
        else:
            return False

    def __repr__(self):
        return f"(x: {self.x}, y: {self.y}, z: {self.z})"


class Punkt(Position):
    def tilStedVektor(self):
        return Vektor(self.x, self.y, self.z)


class Vektor(Position):
    def kryds(self, vektor):
        x = self.y * vektor.z - self.z * vektor.y
        y = -(self.x * vektor.z - self.z * vektor.x)
        z = self.x * vektor.y - self.y * vektor.x
        return Vektor(x, y, z)

    def længde(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normaliserer(self):
        længde = self.længde()
        return Vektor(self.x/længde, self.y/længde, self.z/længde)

    def __repr__(self):
        return f"Vektor(x: {self.x}, y: {self.y}, z: {self.z})"


import pygame
from helper1 import til_skærm

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

