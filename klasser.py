import math
from copy import deepcopy

class Matrix:
    def __init__(self, matrix: [[float]]):
        if type(matrix) == list and type(matrix[0]) == list and type(matrix[0][0]) == float:
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

class Position:
    def __init__(self, x: float, y: float, z: float=0):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

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
        return f"Vektor(x: {self.x}, y: {self.y}, z: {self.z})"


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


class Figur:
    def __init__(self, punkter: [Punkt]):
        self.punkter = punkter

    def fåPunktLængstVækIEnRetning(self, r) -> Punkt:
        pass


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
    punkt1 = Punkt(3,3, 3)
    punkt2 = Punkt(1,2, 2)

    punkt = punkt1 - punkt2
    print(punkt.x, punkt.y, punkt.z)

    vektor1 = Vektor(3, 8, 2)
    vektor2 = Vektor(6, 1, 7)
    kryds = vektor1.kryds(vektor2)

    print(kryds.dot(vektor2))

    matrix1 = Matrix([
        [1, 1],
        [1, 1]
    ])

    matrix2 = Matrix([
        [2],
        [3]
    ])

    matrix3 = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    matrix4 = Matrix([
        [1, 2],
        [3, 4],
        [5, 6]
    ])


    print(matrix3 * matrix4)

    #for søjle in matrix3.få_søjler():
    #    print(søjle)

