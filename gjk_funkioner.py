from figurer import *

def support(figur1: Figur, figur2: Figur, r: Vektor) -> Punkt:
    p1 = figur1.fåPunktLængstVækIEnRetning(r)
    p2 = figur2.fåPunktLængstVækIEnRetning(-r)

    # minkowski difference udføres
    p3 = p1 - p2
    return p3


# får retning mod origo
def fåRetning(simplex: Simplex):
    pass

def vektorTripelProdukt(a: Vektor, b: Vektor, c: Vektor) -> Vektor:
    return b * (c.dot(a)) - (a * (c.dot(b)))

if __name__ == '__main__':
    figur1 = Figur([Punkt(4,5), Punkt(9,9), Punkt(4,11)])
    figur2 = Figur([Punkt(5, 7), Punkt(12, 7), Punkt(10, 2), Punkt(7, 3)])

    r = Vektor(1, 0)
    # print(support(figur1, figur2, r))  # skal give (4, 2)
    r = Vektor(-1, 0)
    # print(support(figur1, figur2, r)) # skal give (-8, -2)
    r = Vektor(0, 1)
    print(support(figur1, figur2, r))  # skal give (-6, 9)

