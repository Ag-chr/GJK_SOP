import csv
import os
import time
import timeit
import pickle
import random
from multiprocessing import Pool

import matplotlib
matplotlib.use("TkAgg")  # eller "Qt5Agg"
import matplotlib.pyplot as plt
import numpy as np
from os import walk

from kollision import tjekKollisionGJK
from tilfældig_form import random_convex_polygon

from position import Punkt


def fåFilnavne(mappePath, filter_func=lambda _: True):
    filer = []
    for (dirpath, dirnames, filenames) in walk(mappePath):
        filer.extend(filenames)
        break
    return [fil for fil in filter(filter_func, filer)]


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


def middelHastighed(func, runs=5, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)

    total_time = timeit.timeit(wrapper, number=runs)
    avg_time = total_time / runs
    return avg_time


def testDatasæt(dataPath, savePath):
    data = None
    with open(dataPath, "rb") as f:
        data = pickle.load(f)

    res = []
    for (i, dataPunkt) in enumerate(data):
        krydser = tjekKollisionGJK(dataPunkt[0], dataPunkt[1])
        middelTid = middelHastighed(tjekKollisionGJK, 100, dataPunkt[0], dataPunkt[1])
        middelTid *= 1000 # få i millisekunder
        res.append({"num": i, "middelTid": middelTid, "krydser": krydser})

    gemTilCsv(savePath, res)


def kør_job(args):
    datasæt, input_fil, output_fil = args
    testDatasæt(input_fil, output_fil)

def testDatasætIMappe(mappePath, savePath):
    os.mkdir(f"{savePath}")
    pklFiler = fåFilnavne(mappePath, lambda navn: navn.find(".pkl") != -1)

    jobs = [(datasæt, f"{mappePath}/{datasæt}", f"{savePath}/{datasæt[:-4]}.csv") for datasæt in pklFiler]

    with Pool(processes=6) as pool:
        pool.map(kør_job, jobs)


def samlDataTilGraf(mappePath):
    csvFiler = fåFilnavne(mappePath, lambda navn: navn.find(".csv") != -1)

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
    return x, y


def genererScatterGraf(x, y):
    plt.scatter(x, y)

    return plt

def LineærRegression(plt, x, y):
    # Regression (line of best fit)
    m, b = np.polyfit(x, y, 1)  # 1 = lineær model
    plt.plot(x, m * x + b, color='red', label=f'y = {m:.2e}x + {b:.2e}')
    # Beregn R^2
    y_pred = m * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    plt.title(f'Regression med R² = {r_squared:.3f}')
    plt.legend()


def EksponentielRegression(plt, x, y):
    x = np.array(x)
    y = np.array(y)

    # Filtrér ugyldige / ikke-positive y (kan ikke log-transformere)
    mask = np.isfinite(x) & np.isfinite(y) & (y > 0)
    x = x[mask]
    y = y[mask]
    if x.size == 0:
        return  # Intet at regresse på

    # Fit på log(y)
    log_y = np.log(y)
    m, b = np.polyfit(x, log_y, 1)  # log_y ≈ m*x + b  =>  y ≈ exp(b) * exp(m*x)

    # Beregn R^2 ud fra originale x (til sammenligning)
    y_pred_orig = np.exp(b + m * x)
    ss_res = np.sum((y - y_pred_orig) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else float('nan')

    # Lav en glat, sorteret x-akse til plotting (undgår "loops" når x ikke er sorteret)
    x_plot = np.linspace(np.min(x), np.max(x), 500)
    y_plot = np.exp(b + m * x_plot)

    # Plot kun regressionskurven (ingen scatter her)
    plt.plot(x_plot, y_plot, color='red', label=f'y = {np.exp(b):.2f} * exp({m:.2f} * x)')
    plt.title(f'Eksponentiel regression med R² = {r_squared:.3f}')
    plt.legend()


def _r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot) if ss_tot != 0 else float('nan')

# O(1) - konstant model y = a
def KonstantRegression(plt, x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]; y = y[mask]
    if x.size == 0:
        return float('nan')
    a = float(np.mean(y))
    # plot horisontal linje
    x_plot = np.linspace(np.min(x), np.max(x), 200)
    plt.plot(x_plot, np.full_like(x_plot, a), color="red", label=f'y = {a:.2e}')
    r2 = _r2(y, np.full_like(y, a))
    plt.title(f'O(1) regression — R² = {r2:.3f}')
    plt.legend()
    return float(r2)

# O(log n) - model y ≈ m * log(x) + b
def LogRegression(plt, x, y):
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return float('nan')
    feat = np.log(x)
    m, b = np.polyfit(feat, y, 1)
    y_pred = m * feat + b
    # glat plot
    x_plot = np.linspace(np.min(x), np.max(x), 300)
    y_plot = m * np.log(x_plot) + b
    plt.plot(x_plot, y_plot, color="red", label=f'y = {m:.2e}·log(n) + {b:.2e}')
    r2 = _r2(y, y_pred)
    plt.title(f'O(log n) regression — R² = {r2:.3f}')
    plt.legend()
    return float(r2)

# O(n) - lineær i n : y ≈ m*n + b
def NRegression(plt, x, y):
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return float('nan')
    m, b = np.polyfit(x, y, 1)
    y_pred = m * x + b
    x_plot = np.linspace(np.min(x), np.max(x), 300)
    plt.plot(x_plot, m * x_plot + b, color="red", label=f'y = {m:.2e}·n + {b:.2e}')
    r2 = _r2(y, y_pred)
    plt.title(f'O(n) regression — R² = {r2:.3f}')
    plt.legend()
    return float(r2)

# O(n log n) - fit y ≈ m*(n log n) + b
def NLogNRegression(plt, x, y):
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return float('nan')
    feat = x * np.log(x)
    m, b = np.polyfit(feat, y, 1)
    y_pred = m * feat + b
    x_plot = np.linspace(np.min(x), np.max(x), 300)
    y_plot = m * (x_plot * np.log(x_plot)) + b
    plt.plot(x_plot, y_plot, color="red", label=f'y = {m:.2e}·n·log(n) + {b:.2e}')
    r2 = _r2(y, y_pred)
    plt.title(f'O(n log n) regression — R² = {r2:.3f}')
    plt.legend()
    return float(r2)

# O(n^2) - fit y ≈ m*n^2 + b
def N2Regression(plt, x, y):
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return float('nan')
    feat = x ** 2
    m, b = np.polyfit(feat, y, 1)
    y_pred = m * feat + b
    x_plot = np.linspace(np.min(x), np.max(x), 300)
    y_plot = m * x_plot**2 + b
    plt.plot(x_plot, y_plot, color="red", label=f'y = {m:.2e}·n^2 + {b:.2e}')
    r2 = _r2(y, y_pred)
    plt.title(f'O(n^2) regression — R² = {r2:.3f}')
    plt.legend()
    return float(r2)

# O(n^k) - power-law via log-log: y ≈ c * n^k
def PowerLawRegression(plt, x, y):
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return float('nan')
    logx = np.log(x)
    logy = np.log(y)
    k, logc = np.polyfit(logx, logy, 1)  # log(y) = k*log(x) + logc
    c = float(np.exp(logc))
    y_pred = c * (x ** k)
    x_plot = np.linspace(np.min(x), np.max(x), 400)
    y_plot = c * (x_plot ** k)
    plt.plot(x_plot, y_plot, color="red", label=f'y = {c:.2e}·n^{k:.3f}')
    r2 = _r2(y, y_pred)
    plt.title(f'O(n^k) power-law regression — k = {k:.3f}, R² = {r2:.3f}')
    plt.legend()
    return float(r2)

# Eksponentiel model y = a * b^n  (log(y) = n*log(b) + log(a))
def EksponentielRegression(plt, x, y):
    mask = np.isfinite(x) & np.isfinite(y) & (y > 0)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return float('nan')
    logy = np.log(y)
    m, b = np.polyfit(x, logy, 1)  # log(y) = m*x + b
    a = float(np.exp(b))
    base = float(np.exp(m))
    y_pred = a * (base ** x)
    x_plot = np.linspace(np.min(x), np.max(x), 400)
    y_plot = a * (base ** x_plot)
    plt.plot(x_plot, y_plot, color="red", label=f'y = {a:.2e}·{base:.3f}^n')
    r2 = _r2(y, y_pred)
    plt.title(f'Eksponentiel regression — R² = {r2:.3f}')
    plt.legend()
    return float(r2)



# få maks ved hvert datasæt
# få de 10 øverste ved hvert datasæt

if __name__ == '__main__':

    #for kanter in range(53, 101):
     #   print("i gang med at generer", kanter, "kanter")
      #  genererDatasæt(kanter, 1000, f"data/{kanter}kant.pkl")

    #print("tester data...")
    #testDatasætIMappe("testData", "resultattest")
    #print("færdig :)")

    x, y = samlDataTilGraf("data - resultat")
    plt = genererScatterGraf(x,y)
    #LineærRegression(plt, x, y)
    NRegression(plt, x, y)
    #EksponentielRegression(plt, x, y)



    plt.show()


    #with open("test.csv", "r") as f:
     #   reader = csv.DictReader(f)
      #  column_values = [row["middelTid"] for row in reader]
       # print(column_values)

    #genererDatasæt(3, 1000, "test/3kant.pkl")
    #testDatasæt("testData/3kant.pkl", "test.csv")




