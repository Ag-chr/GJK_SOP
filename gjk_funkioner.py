from former import Form, Vektor, Punkt, Simpleks


def støtte(form1: Form, form2: Form, r: Vektor) -> Punkt:
    p1 = form1.støttefunktion(r)
    p2 = form2.støttefunktion(-r)

    # minkowski difference udføres
    p3 = p1 - p2
    return p3


def minkowski(form1: Form, form2: Form, sum=True):
    minkowskiPunkter: list[Punkt] = []

    for punkt1 in form1.punkter:
        for punkt2 in form2.punkter:
            punkta = form1.tilVerden(punkt1)
            punktb = form2.tilVerden(punkt2)
            if sum:
                minkowskiPunkter.append(punkta + punktb)
            else:
                minkowskiPunkter.append(punkta - punktb)

    minkowskiForm = Form(minkowskiPunkter)

    ydrePunkter = []
    for punkt in minkowskiForm.punkter:
        retning = punkt.tilStedVektor().enhedsvektor()
        ydrePunkt = minkowskiForm.støttefunktion(retning)
        if ydrePunkt not in ydrePunkter:
            ydrePunkter.append(ydrePunkt)

    return Form(ydrePunkter)


if __name__ == '__main__':
    form1 = Form([Punkt(4, 5), Punkt(9, 9), Punkt(4, 11)])
    form2 = Form([Punkt(5, 7), Punkt(12, 7), Punkt(10, 2), Punkt(7, 3)])

    r = Vektor(1, 0)
    # print(support(form1, form2, r))  # skal give (4, 2)
    r = Vektor(-1, 0)
    # print(support(form1, form2, r)) # skal give (-8, -2)
    r = Vektor(0, 1)
    print(støtte(form1, form2, r))  # skal give (-6, 9)

