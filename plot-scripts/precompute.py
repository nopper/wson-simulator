import math


def freebits(x, length=32):
    for pos in xrange(length):
        if x & (1 << pos) == 0:
            yield pos


def interference(target, bitvect, length=32):
    interf = 0
    for pos in xrange(length):
        if target == pos:
            continue
        if bitvect & (1 << pos) != 0:
            diff = float(abs(target - pos))
            interf += math.log(((diff * 2) + 1) / ((diff - 1) * 2 + 1))
    return interf

from collections import defaultdict
mincost = {}
stats = defaultdict(int)

width = 20

for i in xrange(2 ** width):
    bitpos = [(interference(bit, i, width), bit) for bit in freebits(i, width)]
    if bitpos:
        mincost[i] = min(bitpos)[1]
        stats[min(bitpos)[1]] += 1

#print stats
#print mincost

points = stats.items()
points.sort()


x = map(lambda x: x[0] + 1, points)
y = map(lambda x: x[1], points)

from pylab import *
from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')
figure()
xticks(range(1, width + 1))
bar(x, y, color='green', align='center', log=True)
ylabel(r"\textit{Number of allocations}")
xlabel(r"\textit{Slot number}")
grid(True)
savefig("precompute.eps")
show()
