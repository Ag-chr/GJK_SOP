from konstanter import *
def til_skærm(x, y=0): # til skærm koordinater
    if type(x) == tuple:
        return (VINDUEBREDDE // 2 + x[0], VINDUEHØJDE // 2 - x[1])

    return (VINDUEBREDDE // 2 + x, VINDUEHØJDE // 2 - y)