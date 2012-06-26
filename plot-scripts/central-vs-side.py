import math

def interf(target, bv):
    interf = 0
    for pos in xrange(32):
        if target == pos:
            continue
        if bv & (1 << pos) != 0:
            diff = float(abs(target - pos))
            interf += math.log(((diff) * 2 + 1) / ((diff - 1) * 2 + 1))

    return interf

# Evaluate side graph
side = []
bv = 1
for i in xrange(31):
    print "BV: %32s" % bin(bv)[2:]
    side.append(interf(31, bv))
    bv = bv << 1
    bv += 1

print "Side", len(side), "points"

# Evaluate right graph
center = []
bv = 1
ls = 1

for i in xrange(31):
    print "BV: %32s" % bin(bv)[2:]
    center.append(interf(16, bv))

    if i % 2 == 0:
        bv |= 1 << (31 - i // 2)
    else:
        ls = ls << 1
        ls += 1
        bv |= ls

print "Center", len(center), "points"


print "Side", side
print "Center", center
from pylab import *

from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')

figure()
plot(range(1, 32), side, 'b', ls='-')
plot(range(1, 32), center, 'r', ls='-')
grid(True)
xticks(range(1, 32, 2))

legend(('Side allocation', 'Center allocation'), loc=4)
ylabel(r'\textit{Interference level}')
xlabel(r'\textit{Number of slots occupied}')

savefig('generic.eps')
show()
