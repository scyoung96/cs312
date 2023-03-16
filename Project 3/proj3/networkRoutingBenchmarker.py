"""networkRoutingBenchmarker.py: Benchmarking the network routing algorithms."""

import time
import random
import math

from PyQt6.QtCore import QPointF

import NetworkRoutingSolver as networkRoutingSolver
from CS312Graph import CS312Graph


nValuesToTestArray = [100, 1000, 10000, 100000]
nValuesToTestHeap = [100, 1000, 10000, 100000, 1000000]


def newPoints(numPoints):
    """Generate a list of random points in the range specified by the user."""
    seed = 0
    random.seed(seed)
    ptList = []
    xr = [-2.0, 2.0]
    yr = [-1.0, 1.0]
    while len(ptList) < numPoints:
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        if True:
            xVal = xr[0] + (xr[1] - xr[0]) * x
            yVal = yr[0] + (yr[1] - yr[0]) * y
            ptList.append(QPointF(xVal, yVal))
    return ptList


def generateNetwork(numPoints):
    """Generate a random network with numPoints nodes."""
    nodes = newPoints(numPoints)
    OUT_DEGREE = 3
    size = len(nodes)
    edgeList = {}
    for u in range(size):
        edgeList[u] = []
        pt_u = nodes[u]
        chosen = []
        for i in range(OUT_DEGREE):
            v = random.randint(0, size - 1)
            while v in chosen or v == u:
                v = random.randint(0, size - 1)
            chosen.append(v)
            pt_v = nodes[v]
            uv_len = math.sqrt((pt_v.x() - pt_u.x()) ** 2 +
                               (pt_v.y() - pt_u.y()) ** 2)
            edgeList[u].append((v, 100.0 * uv_len))
        edgeList[u] = sorted(edgeList[u], key=lambda n: n[0])
    graph = CS312Graph(nodes, edgeList)
    return graph


if __name__ == "__main__":
    testResultsArray = {nValue: [] for nValue in nValuesToTestArray}
    testResultsHeap = {nValue: [] for nValue in nValuesToTestHeap}

    print("Testing with array implementation")
    for nValue in nValuesToTestArray:
        print(f"\nTesting with n = {nValue}")
        for i in range(5):
            print(f"Generating network with {nValue} nodes...")
            graph = generateNetwork(nValue)
            solver = networkRoutingSolver.NetworkRoutingSolver()
            solver.initializeNetwork(graph)
            print(f" Test {i + 1}")
            t1 = time.time()
            solver.computeShortestPaths(0, use_heap=False)
            t2 = time.time()

            elapsedTime = t2 - t1
            print(f"  Elapsed time: {elapsedTime:3.3f} seconds")
            testResultsArray[nValue].append(elapsedTime)

    print("\n\nTesting with heap implementation")
    for nValue in nValuesToTestHeap:
        print(f"\nTesting with n = {nValue}")
        for i in range(5):
            print(f"Generating network with {nValue} nodes...")
            graph = generateNetwork(nValue)
            solver = networkRoutingSolver.NetworkRoutingSolver()
            solver.initializeNetwork(graph)
            print(f" Test {i + 1}")
            t1 = time.time()
            solver.computeShortestPaths(0, use_heap=True)
            t2 = time.time()

            elapsedTime = t2 - t1
            print(f"  Elapsed time: {elapsedTime:3.3f} seconds")
            testResultsHeap[nValue].append(elapsedTime)

    finalResults = {}
    for nValue, results in testResultsArray.items():
        finalResults[nValue] = sum(results) / len(results)

    finalResultsHeap = {}
    for nValue, results in testResultsHeap.items():
        finalResultsHeap[nValue] = sum(results) / len(results)

    # Write test results to a file
    with open("network_routing_benchmark_results.txt", "w") as f:
        f.write("Array implementation\n")
        for nValue, results in testResultsArray.items():
            f.write(f"{nValue}\n")
            for result in results:
                f.write(f"{result:3.3f}\n")
            f.write("\n")

        f.write("\nAverages (seconds)\n")
        for nValue in nValuesToTestArray:
            f.write(f"{nValue} {finalResults[nValue]:3.3f} seconds\n")

        f.write("\n\nHeap implementation\n")
        for nValue, results in testResultsHeap.items():
            f.write(f"{nValue}\n")
            for result in results:
                f.write(f"{result:3.3f}\n")
            f.write("\n")

        f.write("\nAverages (seconds)\n")
        for nValue in nValuesToTestHeap:
            f.write(f"{nValue} {finalResultsHeap[nValue]:3.3f} seconds\n")