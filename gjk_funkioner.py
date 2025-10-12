from figurer import Figur, Vektor, Punkt, Simplex


def support(figur1: Figur, figur2: Figur, r: Vektor) -> Punkt:
    p1 = figur1.fåPunktLængstVækIEnRetning(r)
    p2 = figur2.fåPunktLængstVækIEnRetning(-r)

    # minkowski difference udføres
    p3 = p1 - p2
    return p3

def minkowski(figur1: Figur, figur2: Figur, sum=True):
    minkowskiPunkter: list[Punkt] = []

    for punkt1 in figur1.punkter:
        for punkt2 in figur2.punkter:
            punkta = figur1.tilVerden(punkt1)
            punktb = figur2.tilVerden(punkt2)
            if sum:
                minkowskiPunkter.append(punkta + punktb)
            else:
                minkowskiPunkter.append(punkta - punktb)

    minkowskiFigur = Figur(minkowskiPunkter)

    ydrePunkter = []
    for punkt in minkowskiFigur.punkter:
        retning = punkt.tilStedVektor().enhedsvektor()
        ydrePunkt = minkowskiFigur.fåPunktLængstVækIEnRetning(retning)
        if ydrePunkt not in ydrePunkter:
            ydrePunkter.append(ydrePunkt)

    return Figur(ydrePunkter)





if __name__ == '__main__':
    figur1 = Figur([Punkt(4,5), Punkt(9,9), Punkt(4,11)])
    figur2 = Figur([Punkt(5, 7), Punkt(12, 7), Punkt(10, 2), Punkt(7, 3)])

    r = Vektor(1, 0)
    # print(support(figur1, figur2, r))  # skal give (4, 2)
    r = Vektor(-1, 0)
    # print(support(figur1, figur2, r)) # skal give (-8, -2)
    r = Vektor(0, 1)
    print(support(figur1, figur2, r))  # skal give (-6, 9)

