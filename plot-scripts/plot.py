import os
import sys
import random
from collections import defaultdict

sys.path.insert(0, os.getcwd())
from wsonsim.statistics import stats
from wsonsim.sim import Simulator


def capture(topology, wavelengths, iterations, arrivals, departures, reference):
    # Use a fixed seed if you want to see the real difference
    sim = Simulator(topology, wavelengths, iterations, arrivals, departures, reference, None)

    # snapshot = sim.simple_run(3000)
    # samples = random.sample(snapshot, min(3000, len(snapshot)))

    samples = sim.simple_run(3000)

    if len(samples) > 10:
        statistics = stats(map(lambda x: float(x[0]) / float(x[1]), samples))

        average, confidence = statistics[0], statistics[-1]

        print statistics
        print "Collected:", average, confidence

        return average, confidence
    else:
        return 0, 0


def blocking():
    topology = 'topos/eon.simpltopo.txt'
    wavelengths = 16
    iterations = 100000
    departures = 1

    curves = (
        ("FF", []),
        ("FF - Adaptive", []),
        ("FF/LF - Adaptive", []),
        ("FF/LF/2 - Adaptive", []),
        ("MinCost - Adaptive", [])
    )

    x = []

    #for i in xrange(64, 151):
    for i in xrange(30, 151, 10):
        x.append(i)

        for method, (label, points) in enumerate(curves):
            avg, ci = capture(topology, wavelengths, iterations, i, departures, method)
            points.append((avg, ci))

    f = open('graph-block.py', 'w+')
    f.write("from pylab import *\nfrom matplotlib import rc\n")
    f.write("rc('text', usetex=True)\nrc('font', family='serif')\nfigure()\n")
    f.write("x = " + repr(x) + "\n")

    colors = ('k', 'r', 'g', 'b', 'm')
    labels = map(lambda x: x[0], curves)

    for idx, (label, points) in enumerate(curves):
        y = map(lambda x: x[0], points)
        e = map(lambda x: x[1], points)
        f.write(("y%d = " % idx) + repr(y) + "\n")
        f.write(("e%d = " % idx) + repr(e) + "\n")
        f.write("errorbar(x, y%d, yerr=e%d, ls='-', fmt='%s.')\n" % (idx, idx, colors[idx]))

    f.write("grid(True)\n")
    f.write("xlabel(r'\\textit{Traffic load (Erlang)}')\n")
    f.write("ylabel(r'\\textit{Blocking probability}')\n")
    f.write("legend(" + repr(labels) + ", loc=4)\n")
    f.write("yscale('log')\nsavefig('graph-block.eps')\n")
    f.write("show()\n")
    f.close()


def interference():
    topology = 'topos/eon.simpltopo.txt'
    wavelengths = 16
    iterations = 200000
    departures = 1

    curves = (
        ("FF", []),
        ("FF - Adaptive", []),
        ("FF/LF - Adaptive", []),
        ("FF/LF/2 - Adaptive", []),
        ("MinCost - Adaptive", [])
    )

    x = []

    #for i in xrange(64, 151):
    for i in xrange(80, 151, 10):
        x.append(i)

        for method, (label, points) in enumerate(curves):
            sim = Simulator(topology, wavelengths, iterations, i, departures, method, 0)
            stats = sim.run()

            points.append((stats[0], stats[-1]))

    f = open('graph.py', 'w+')
    f.write("from pylab import *\nfrom matplotlib import rc\n")
    f.write("rc('text', usetex=True)\nrc('font', family='serif')\nfigure()\n")
    f.write("x = " + repr(x) + "\n")

    colors = ('k', 'r', 'g', 'b', 'm')
    labels = map(lambda x: x[0], curves)

    for idx, (label, points) in enumerate(curves):
        y = map(lambda x: x[0], points)
        e = map(lambda x: x[1], points)
        f.write(("y%d = " % idx) + repr(y) + "\n")
        f.write(("e%d = " % idx) + repr(e) + "\n")
        f.write("errorbar(x, y%d, yerr=e%d, ls='-', fmt='%s.')\n" % (idx, idx, colors[idx]))

    f.write("grid(True)\n")
    f.write("xlabel(r'\\textit{Traffic load (Erlang)}')\n")
    f.write("ylabel(r'\\textit{Average interference level}')\n")
    f.write("legend(" + repr(labels) + ", loc=4)\n")
    f.write("savefig('graph.eps')\n")
    f.write("show()\n")
    f.close()


def pdf_points():
    topology = 'topos/eon.simpltopo.txt'
    wavelengths = 16
    iterations = 100000
    departures = 1

    curves = (
        ("FF", {}),
        ("FF - Adaptive", {}),
        ("FF/LF - Adaptive", {}),
        ("FF/LF/2 - Adaptive", {}),
        ("MinCost - Adaptive", {})
    )

    # Sulle x la distance
    # Sulle y interference

    x = []
    with open("pdf-all.txt", "w+") as f:
        for load in xrange(80, 151, 10):
            for idx, method in enumerate(curves):
                sim = Simulator(topology, wavelengths, iterations, load, departures, idx, None)
                distances, interferences = sim.run(wantpdf=True)

                for d, i in zip(distances, interferences):
                    f.write("%d %d %.20f\n" % (idx, d, i))


if __name__ == "__main__":
    try:
        if sys.argv[1] == 'blocking':
            blocking()
        elif sys.argv[1] == 'interference':
            interference()
        elif sys.argv[1] == 'pdf':
            pdf_points()
        else:
            raise
    except:
        print "Usage: %s <blocking|interference|pdf>" % sys.argv[0]
        sys.exit(-1)
