from functools import wraps

import csv
import os

import timeit
import tracemalloc
import time
import threading

import matplotlib
matplotlib.use("TkAgg")  # or "Qt5Agg" if you prefer
import matplotlib.pyplot as plt

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



def gemTilCsv(path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            fieldnames = data[0].keys()

            skrivHeader = False
            if not os.path.exists(path):
                skrivHeader = True

            with open(path, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if skrivHeader:
                    writer.writeheader()
                writer.writerows(data)
            return data

        return wrapper
    return decorator



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


if __name__ == '__main__':
    testdata = [
        {"x": 1, "y": 2, "a": 1},
        {"x": 2, "y": 3, "a": 2},
        {"x": 3, "y": 4, "a": 2}
    ]

    @gemTilCsv("output.csv")
    def testCsv(data):
        return data

    @gemTilCsv("outputTest.csv")
    @benchmark(1, )
    def testBenchmark():
        a = [i for i in range(1000000)]
        time.sleep(0.5)  # simulate work
        return sum(a)

    #print("Csv: ", testCsv(testdata))
    #print("benchmark:", testBenchmark())

    plot_bar_from_csv("output.csv", "x", "y")

