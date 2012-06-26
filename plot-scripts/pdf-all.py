import os
import sys
from pylab import *
from matplotlib import rc
from collections import defaultdict

sys.path.insert(0, os.getcwd())
from wsonsim.statistics import stats

methods = defaultdict(lambda: defaultdict(list))
norm = defaultdict(lambda: defaultdict(int))

with open("pdf-all.txt") as f:
    for line in f:
        method, distance, interf = line.split(' ', 2)
        method, distance, interf = int(method), int(distance), float(interf)

        methods[method][distance].append(interf)
        norm[method][distance] += 1

figure()

fmts = ('ko-', 'ro-', 'go-', 'bo-', 'mo-')
#fmts = ('k', 'r', 'g', 'b', 'm')
for idx, method in enumerate(methods):
    for distance in methods[method]:
        distances = methods[method][distance]

        normalizer = max([norm[k][distance] for k in norm])

        print "Method", idx, "at Hop", distance, "has", len(distances), "samples"

        methods[method][distance] = sum(distances) / float(normalizer)

    points = methods[method].items()
    points.sort()

    x = map(lambda x: x[0], points)
    y = map(lambda x: x[1], points)

    stats(y)

    print points
    print "Plotting", idx, fmts[idx]

    print x, y

    plot(x, y, fmts[idx])
    #bar(x, y, 0.15, color=fmts[idx])

rc('text', usetex=True)
rc('font', family='serif')

xlabel(r'\textit{Number of hops}')
ylabel(r'\textit{Average interference level}')

xlim([0, 10])
xticks(range(0, 14))
grid(True)

legend(("FF", "FF - Adaptive", "FF/LF - Adaptive", "FF/LF/2 - Adaptive", "MinCost - Adaptive"), loc=0)
savefig("pdf.eps")
show()
