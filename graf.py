import csv
import os
import time
import timeit
import pickle
import random
from copy import deepcopy
from itertools import count
from multiprocessing import Pool

import matplotlib
matplotlib.use("TkAgg")  # eller "Qt5Agg"
import matplotlib.pyplot as plt
import numpy as np
from os import walk

from kollision import tjekKollisionGJK
from tilfældig_form import *

from position import Punkt


def beregn_spredning(liste):
    if not liste:
        return 0.0  # håndter tom liste
    n = len(liste)
    gennemsnit = sum(liste) / n
    varians = sum((x - gennemsnit) ** 2 for x in liste) / n
    spredning = math.sqrt(varians)
    return spredning


def fåFilnavne(mappePath, filter_func=lambda _: True):
    filer = []
    for (dirpath, dirnames, filenames) in walk(mappePath):
        filer.extend(filenames)
        break
    return [fil for fil in filter(filter_func, filer)]

def fåKolonne(path, key):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        kolonneværdier = [row[key] for row in reader]
    return kolonneværdier

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


def middelHastighed(func, runs=5, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)

    total_time = timeit.timeit(wrapper, number=runs)
    avg_time = total_time / runs
    return avg_time


def kør_job(args):
    datasæt, input_fil, output_fil = args
    #testDatasæt(input_fil, output_fil)

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

def lavAksetitler(plt, xAkse, yAkse):
    plt.xlabel(xAkse)
    plt.ylabel(yAkse)

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
    plt.plot(x_plot, m * x_plot + b, color="red", label=f'y = {m:.4f}·n + {b:.2f}')
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


def genererForme(maksPunkter, antalPer):
    for punktmængde in range(3,maksPunkter+1):
        forme = []
        for _ in range(antalPer):
            forme.append(tilfældig_regulær_polygon(punktmængde, 2.5))

        with open(f"forme/{punktmængde}kant.pkl", "wb") as f:
            pickle.dump(forme, f)


def testForm(form1, form2):
    positioner = []
    for x in range(-6, 6, 3):
        for y in range(-6, 6, 3):
            positioner.append(Punkt(x, y))

    resultater: list[dict] = []
    for i in range(len(positioner)):
        for j in range(len(positioner)):
            if i == j:
                continue
            form1.centrum = positioner[i]
            form2.centrum = positioner[j]

            krydser, iterationer = tjekKollisionGJK(form1, form2)
            middelTid = middelHastighed(tjekKollisionGJK, 5, form1, form2) / 5
            middelTid *= 1000  # få i millisekunder
            resultater.append({"middelTid": middelTid, "krydser": krydser, "iterationer": iterationer})

    return resultater


def testForme(former1, former2):
    resultater: list[dict] = []
    for form1 in former1:
        for form2 in former2:
            resultater.extend(testForm(form1, form2))
    return resultater


from multiprocessing import Pool, cpu_count
def worker(args):
    punktAntal1, punktAntal2 = args

    with open(f"forme/{punktAntal1}kant.pkl", "rb") as f:
        former1 = pickle.load(f)
    with open(f"forme/{punktAntal2}kant.pkl", "rb") as f:
        former2 = pickle.load(f)

    resultater = testForme(former1, former2)
    gemTilCsv(f"forme - resultater - 90 mod centrum/{punktAntal1}-{punktAntal2}kant", resultater)

    return f"færdig: {punktAntal1}-{punktAntal2}kant.csv"

def testAlleFormKombinationer():
    jobs = [
        (punktAntal1, punktAntal2)
        for punktAntal1 in range(3, 16)
        for punktAntal2 in range(punktAntal1, 16)
    ]

    with Pool(cpu_count()) as pool:
        for status in pool.imap_unordered(worker, jobs):
            print(status)


if __name__ == '__main__':
    filnavne = fåFilnavne("forme - resultater")
    x = []
    y = []
    for filnavn in filnavne:
        antal1 = int(filnavn[:filnavn.find("-")])
        antal2 = int(filnavn[filnavn.find("-") + 1:filnavn.find("k")])
        hjørne_sum = antal1 + antal2

        with open(f"forme - resultater - 90 mod centrum/{filnavn}", "r") as f:
            reader = csv.DictReader(f)
            y_values = [float(row["iterationer"]) for row in reader]
            gennemsnit = sum(y_values) / len(y_values)

            x_values = hjørne_sum

            x.append(x_values)
            y.append(gennemsnit)

    x = np.array(x)
    y = np.array(y)

    plt = genererScatterGraf(x, y)
    lavAksetitler(plt, "Antal hjørner", "Iterationer")
    LogRegression(plt, x, y)
    plt.show()


    quit()
    filnavne = fåFilnavne("forme - resultater")

    gennemsnit_tider = {}

    for filnavn in filnavne:
        antal1 = int(filnavn[:filnavn.find("-")])
        antal2 = int(filnavn[filnavn.find("-")+1:filnavn.find("k")])
        hjørne_sum = antal1 + antal2

        tider = list(map(float, fåKolonne(f"forme - resultater/{filnavn}", "middelTid")))
        gennemsnit = sum(tider) / len(tider)

        gennemsnit_tider_temp = gennemsnit_tider.get(hjørne_sum, [])
        gennemsnit_tider_temp.append(gennemsnit)
        gennemsnit_tider[hjørne_sum] = gennemsnit_tider_temp

    items = sorted(gennemsnit_tider.items(), key=lambda i: i[0])

    for (k, v) in items:
        spredning = beregn_spredning(v)
        print(f"{k} hjørner | spredning: {spredning} | gennemsnitdata i ms: {v}")
