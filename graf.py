import csv
import os
import timeit
import pickle
import random

import matplotlib
matplotlib.use("TkAgg")  # eller "Qt5Agg"
import matplotlib.pyplot as plt

from kollision import tjekKollisionGJK
from tilfældig_form import random_convex_polygon

from position import Punkt

def middelHastighed(func, runs=5, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)

    total_time = timeit.timeit(wrapper, number=runs)
    avg_time = total_time / runs
    return avg_time


def gemTilCsv(path, data: list[dict]):
    fieldnames = data[0].keys()

    skrivHeader = False
    if not os.path.exists(path):
        skrivHeader = True

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if skrivHeader:
            writer.writeheader()
        writer.writerows(data)


def genererDatasæt(kanter, mængde, savePath):
    testFormer: list = []
    for i in range(mængde):
        Form1 = random_convex_polygon(kanter, scale=random.uniform(2.5, 5.5))
        Form1.centrum = Punkt(random.uniform(-6, 6), random.uniform(-6, 6))
        Form2 = random_convex_polygon(kanter, scale=random.uniform(2.5, 5.5))
        Form2.centrum = Punkt(random.uniform(-6, 6), random.uniform(-6, 6))
        testFormer.append((Form1, Form2))

    with open(savePath, "wb") as f:
        pickle.dump(testFormer, f)


def testDatasæt(dataPath, savePath):
    data = None
    with open(dataPath, "rb") as f:
        data = pickle.load(f)

    res = []
    for (i, dataPunkt) in enumerate(data):
        krydser = tjekKollisionGJK(dataPunkt[0], dataPunkt[1])
        middelTid = middelHastighed(tjekKollisionGJK, 1, dataPunkt[0], dataPunkt[1])
        res.append({"num": i, "middelTid": middelTid, "krydser": krydser})

    gemTilCsv(savePath, res)


def fåFilnavne(mappePath, filter_func=lambda _: True):
    filer = []
    for (dirpath, dirnames, filenames) in walk(mappePath):
        filer.extend(filenames)
        break
    return [fil for fil in filter(filter_func, filer)]

from os import walk
def testDatasætIMappe(mappePath):

    os.mkdir(f"{mappePath} - resultat")
    pklFiler = fåFilnavne(mappePath, lambda navn: navn.find(".pkl") != -1)
    for datasæt in pklFiler:
        testDatasæt(f"{mappePath}/{datasæt}", f"{mappePath} - resultat/{datasæt[:-4]}.csv")


import numpy as np

def genererGraf(mappePath, savePath):
    csvFiler = fåFilnavne(mappePath, lambda navn: navn.find(".csv") != -1)
    print(csvFiler)

    x = []
    y = []

    for csvFil in csvFiler:
        with open(f"{mappePath}/{csvFil}", "r") as f:
            reader = csv.DictReader(f)
            y_values = [float(row["middelTid"]) for row in reader]
            x_values = [int(csvFil[:-8]) for _ in y_values]

            x.extend(x_values)
            y.extend(y_values)

    x = np.array(x)
    y = np.array(y)

    # Scatter plot
    plt.scatter(x, y)

    # Regression (line of best fit)
    m, b = np.polyfit(x, y, 1)  # 1 = lineær model
    plt.plot(x, m*x + b, color='red', label=f'y = {m:.2e}x + {b:.2e}')

    # Beregn R^2
    y_pred = m * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    plt.title(f'Regression med R² = {r_squared:.3f}')

    plt.legend()
    plt.show()


if __name__ == '__main__':

    #for kanter in range(53, 101):
     #   print("i gang med at generer", kanter, "kanter")
      #  genererDatasæt(kanter, 1000, f"data/{kanter}kant.pkl")

    #print("tester data...")
    #testDatasætIMappe("testData")
    #print("færdig :)")

    genererGraf("data - resultat", "a")

    with open("test.csv", "r") as f:
        reader = csv.DictReader(f)
        column_values = [row["middelTid"] for row in reader]
        print(column_values)



    #genererDatasæt(3, 1000, "test/3kant.pkl")
    #testDatasæt("testData/3kant.pkl", "test.csv")




