import os
import sys
from pylab import *
from matplotlib import rc
from collections import defaultdict

sys.path.insert(0, os.getcwd())
from wsonsim.statistics import stats

methods = defaultdict(lambda: defaultdict(list))
norm = defaultdict(int)

with open("pdf-all.txt") as f:
    for line in f:
        method, distance, interf = line.split(' ', 2)
        method, distance, interf = int(method), int(distance), float(interf)

        methods[method][distance].append(interf)
        norm[method] += 1

figure()

cumulative = defaultdict(int)

fmts = ('ko-', 'ro-', 'go-', 'bo-', 'mo-')
#fmts = ('k', 'r', 'g', 'b', 'm')
for idx, method in enumerate(methods):
    for distance in methods[method]:
        distances = methods[method][distance]
        methods[method][distance] = len(distances) / float(norm[method])

        cumulative[method] += methods[method][distance]

    points = methods[method].items()
    points.sort()
    x = map(lambda x: x[0], points)
    y = map(lambda x: x[1], points)

    print points
    print "Plotting", idx, fmts[idx]

    print x, y

    plot(x, y, fmts[idx])
    #bar(x, y, 0.15, color=fmts[idx])

for k,v in cumulative.iteritems():
    print "Method", k, "cumulative sum is:", v


rc('text', usetex=True)
rc('font', family='serif')
xlabel(r'\textit{Number of hops}')
ylabel(r'\textit{Probability}')

xlim([0, 10])
xticks(range(0, 14))
grid(True)

legend(("FF", "FF - Adaptive", "FF/LF - Adaptive", "FF/LF/2 - Adaptive", "MinCost - Adaptive"), loc=0)
savefig("pdf-distance.eps")

show()
