from functools import wraps

import csv
import os

import timeit
import tracemalloc
import time
import threading
import pickle

import matplotlib
matplotlib.use("TkAgg")  # or "Qt5Agg" if you prefer
import matplotlib.pyplot as plt

from kollision import tjekKollisionGJK
from tilfældig_figur import random_convex_polygon


def plot_bar_from_csv(filename, x_column, y_column, title="Bar Chart"):
    """Plot a bar chart from a CSV file using the given x and y column names."""
    x_values = []
    y_values = []

    # --- Read data from CSV ---
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x_values.append(row[x_column])
            # Convert y values to float (if numeric)
            y_values.append(float(row[y_column]))

    # --- Make bar plot ---
    plt.bar(x_values, y_values)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.xticks(rotation=45)  # rotate x labels if long
    plt.tight_layout()       # adjust layout
    plt.show()


def average_speed(func, runs=5, *args, **kwargs):
    """
    Measures average execution time of a function over multiple runs using timeit.

    :param func: function to run
    :param runs: number of times to run
    :param args: positional arguments for func
    :param kwargs: keyword arguments for func
    :return: average execution time in seconds
    """
    def wrapper():
        return func(*args, **kwargs)

    total_time = timeit.timeit(wrapper, number=runs)
    avg_time = total_time / runs
    return avg_time


def average_memory(func, runs=5, interval=0.001, *args, **kwargs):
    """
    Measures average memory usage of a function over multiple runs using tracemalloc.

    :param func: function to run
    :param runs: number of times to run
    :param interval: sampling interval in seconds
    :param args: positional arguments for func
    :param kwargs: keyword arguments for func
    :return: average memory usage in MB
    """
    avg_memories = []

    for _ in range(runs):
        memory_samples = []

        def sampler():
            while not stop_event.is_set():
                current, _ = tracemalloc.get_traced_memory()
                memory_samples.append(current)
                time.sleep(interval)

        tracemalloc.start()
        stop_event = threading.Event()
        sampling_thread = threading.Thread(target=sampler)
        sampling_thread.start()

        func(*args, **kwargs)

        stop_event.set()
        sampling_thread.join()
        tracemalloc.stop()

        avg_memories.append(sum(memory_samples)/len(memory_samples) if memory_samples else 0)

    avg_memory = sum(avg_memories)/len(avg_memories)/10**6  # convert to MB
    return avg_memory


def benchmark(iterationer, beskrivelse=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            gen_hukommelse = average_memory(func, iterationer, 0.001, *args, **kwargs)
            gen_hastighed  = average_speed(func, iterationer, *args, **kwargs)
            d = None
            if not beskrivelse:
                d = {"hastighed": gen_hastighed, "hukommelse": gen_hukommelse}
            else:
                d = {"hastighed": gen_hastighed, "hukommelse": gen_hukommelse, "beskrivelse": beskrivelse}

            return [d]
        return wrapper
    return decorator


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


import random
from position import Punkt
def genererDatasæt(kanter, mængde, savePath):
    testFigurer: list = []
    for i in range(mængde):
        figur1 = random_convex_polygon(kanter, scale=random.uniform(2.5, 5.5))
        figur1.centrum = Punkt(random.uniform(-6, 6), random.uniform(-6, 6))
        figur2 = random_convex_polygon(kanter, scale=random.uniform(2.5, 5.5))
        figur2.centrum = Punkt(random.uniform(-6, 6), random.uniform(-6, 6))
        testFigurer.append((figur1, figur2))

    with open(savePath, "wb") as f:
        pickle.dump(testFigurer, f)


def testDatasæt(dataPath, savePath):
    data = None
    with open(dataPath, "rb") as f:
        data = pickle.load(f)

    res = []
    for (i, dataPunkt) in enumerate(data):
        krydser = tjekKollisionGJK(dataPunkt[0], dataPunkt[1])
        middelTid = average_speed(tjekKollisionGJK, 1, dataPunkt[0], dataPunkt[1])
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




