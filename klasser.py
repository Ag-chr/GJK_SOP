import math


class Position:
    def __init__(self, x: float, y: float, z: float=0):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z + other.z

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


class Punkt(Position):
    pass


class Vektor(Position):
    def kryds(self, v):
        return Vektor

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
        self.punkter.append(punkt)

    # få seneste tilføjet punkt
    def fåSeneste(self) -> Punkt:
        pass

    # se om simplex indeholder punktet
    def indeholder(self, punkt: Punkt):
        pass


if __name__ == '__main__':
    punkt1 = Punkt(3,3, 3)
    punkt2 = Punkt(1,2, 2)

    punkt = punkt1 - punkt2
    print(punkt.x, punkt.y, punkt.z)
