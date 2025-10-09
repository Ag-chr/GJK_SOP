from matrix import Matrix
import math

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

    def sæt(self, punkt):
        self.x = punkt.x
        self.y = punkt.y
        self.z = punkt.z

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

    def __mul__(self, other):
        if type(other) not in [float, int]:
            raise "Kan kun gange en skalar på"
        x = self.x * other
        y = self.y * other
        z = self.z * other
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

    def enhed_vektor(self):
        længde = self.længde()
        return Vektor(self.x/længde, self.y/længde, self.z/længde)


    def __repr__(self):
        return f"Vektor(x: {self.x}, y: {self.y}, z: {self.z})"


def vektorTripelProdukt(a: Vektor, b: Vektor, c: Vektor) -> Vektor:
    return b * (c.dot(a)) - (a * (c.dot(b)))