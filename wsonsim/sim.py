import sys
from random import expovariate, seed
from statistics import stats
from heapq import heappush, heappop
from network import Graph

class Event(object):
    def __init__(self):
        self.src = self.sim.graph.random_node()
        self.dst = self.src

        while self.dst == self.src:
            self.dst = self.sim.graph.random_node()

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, self.time)

    def __cmp__(self, other):
        return cmp(self.time, other.time)

class Departure(Event):
    def __init__(self, sim, path, pos, time=0):
        self.sim = sim
        self.path = path
        self.bitpos = pos
        self.time = time + expovariate(1 / sim.lambda_dep)

    def process(self):
        self.sim.graph.deallocate(self.bitpos, self.path)
        return False

class Arrival(Event):
    def __init__(self, sim, time=0):
        self.sim = sim
        self.time = time + expovariate(1 / sim.lambda_arr)

        Event.__init__(self)

    def process(self):
        self.sim.arrivals += 1
        self.sim.enqueue(Arrival(self.sim, self.time))

        ret = self.sim.allocate(self.src, self.dst)

        if ret:
            pos, distances, interferences, path = ret

            self.sim.distances.extend(distances)
            self.sim.interferences.extend(interferences)

            self.sim.enqueue(Departure(self.sim, path, pos, self.time))

            return False
        else:
            self.sim.blocks += 1
            return True


class Simulator(object):
    def __init__(self, graph_file, wavelengths, iterations, lambda_arr, \
                 lambda_dep, method, rndseed):

        self.arrivals = 0
        self.blocks = 0

        self.count = 0
        self.iterations = int(iterations)

        self.interferences = []
        self.distances = []
        self.method = int(method)

        self.lambda_arr = 1 / float(lambda_arr)
        self.lambda_dep = 1 / float(lambda_dep)

        self.queue = []
        self.graph = Graph(file=graph_file, wl=int(wavelengths))

        self.nointerference = False

        self.methods = ('Classic', 'FF', 'FF/LF', 'FF/LF/2', 'MinCost')

        # Initialize the random seed
        seed(rndseed)

    def allocate(self, src, dst):
        return self.graph.allocate(src, dst, self.method, self.nointerference)

    def enqueue(self, evt):
        heappush(self.queue, evt)

    def start_loop(self):
        count = self.count
        iterations = self.iterations

        while True:
            evt = heappop(self.queue)

            blocked = evt.process()

            if self.nointerference and blocked:
                self.snapshot.append((self.blocks, self.arrivals))
            #print evt, (blocked and "BLOCK" or "")

            count += 1

            if iterations == count:
                break

        self.count = count

    def simple_run(self, num_samples):
        """
        Simply returns the blocking probability from a simple run
        """
        self.nointerference = True
        self.enqueue(Arrival(self))

        count = self.count
        iterations = self.iterations
        stopafter = iterations / num_samples
        current = 0
        snapshot = []

        while True:
            evt = heappop(self.queue)

            blocked = evt.process()

            if current == stopafter:
                current = 0
                snapshot.append((self.blocks, self.arrivals))

            count += 1
            current += 1

            if iterations == count:
                break

        self.count = count
        return snapshot

    def run(self, wantpdf=False):
        self.enqueue(Arrival(self))

        self.start_loop()

        sys.stdout.write("[%8s] %4d rate, %6d blocks, %6d arrivals [%.04f]\r" % (
            self.methods[self.method],
            1.0 / self.lambda_arr, self.blocks, self.arrivals, float(self.blocks) / float(self.arrivals)
        ))

        if wantpdf:
            sys.stdout.write('\n')

        sys.stdout.flush()

        while not wantpdf:
            avg, median, std, min, max, conf = stats(self.interferences)

            if conf >= 0.05:
                self.iterations *= 2

                sys.stdout.write("Doubling iterations %d\r" % self.iterations)
                sys.stdout.flush()
                self.start_loop()
            else:
                sys.stdout.write("[%8s] %4d rate, %.6f interference, %6d blocks, %6d arrivals [%.04f]\r" % (
                    self.methods[self.method],
                    1.0 / self.lambda_arr, avg, self.blocks, self.arrivals, float(self.blocks) / float(self.arrivals)
                ))
                sys.stdout.write('\n')
                sys.stdout.flush()
                return (avg, median, std, min, max, conf)

        # If we are here we are just interested in the pdf
        # So just returns the results

        return (self.distances, self.interferences)
