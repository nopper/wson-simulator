import networkx as nx
from operations import *
from random import choice

class FrequencyBand(object):
    """
    This class is just an abstraction for representing the available slots
    on a given link. We use a bitvect that is an integer of a given length.

    An istance of this class will be associated with each link of the network

    The length is specified in the constructor
    """

    def __init__(self, length=32):
        """
        Initialize the FrequencyBand class.
        @param length the length in bit of the bit-vector
        """
        self._bitvect = 0
        self._length = length

    def get_state(self):
        return self._bitvect

    def get_length(self):
        return self._length

    state = property(get_state)
    length = property(get_length)

    def allocate_side(self):
        """
        Perform a side allocation.
        @return the first free position in the bit-vector
        """
        pos = allocate_side(self._bitvect, self._length)

        if pos is not None:
            self.allocate_pos(pos)

        return pos

    def allocate_first(self):
        """
        Perform a first-fit allocation.
        @return the first free position in the bit-vector
        """
        pos = find_first_free(self._bitvect, 0, 1, 0, self._length)

        if pos is not None:
            interference = self.interference_at(pos)
            self.allocate_pos(pos)

        return (pos, interference)

    def allocate_center(self):
        """
        Perform a center allocation.
        @return the first free position in the bit-vector
        """
        pos = allocate_center(self._bitvect, self._length)

        if pos is not None:
            self.allocate_pos(pos)

        return pos

    def allocate_pos(self, pos):
        """
        Allocate a given slot in the bitvect.
        @param pos slot that you want to allocate. Possibly returned by one
                   of the allocate_* functions
        """
        if self._bitvect & (1 << pos) != 0:
            raise Exception("Already allocated")

        self._bitvect |= 1 << pos

    def deallocate_pos(self, pos):
        """
        Deallocate a given slot
        @param pos the slot to deallocate
        """
        self._bitvect &= ~(1 << pos)

    def interference_at(self, target):
        """
        Evaluate the inteference perceived by the target slot
        @param target the target slot
        @return a float indicating the interference level
        """
        # Evaluate on the right
        interf = 1

        for pos in xrange(self._length):
            if target == pos:
                continue

            if self._bitvect & (1 << pos) != 0:
                diff = float(abs(target - pos))
                interf *= ((diff) * 2 + 1) / ((diff - 1) * 2 + 1)

        return math.log(interf)


class Graph(object):
    """
    This class holds the information about the network topology
    """

    def __init__(self, file='graph.txt', contents=None, wl=8):
        """
        Instantiate a Graph object.
        @param file the file from which to load the network
        @param contents if the file is set to None you can load the network
                        information directly from this string.
        @param wl the number of wavelengths that each link will have
        """
        if file is not None:
            self.graph = Graph.load_graph(file, wl)
        elif contents is not None:
            self.graph = Graph.load_from_data(contents, wl)

    def random_node(self):
        """
        @return a random node
        """
        return choice(self.graph.nodes())

    def deallocate(self, bitpos, path):
        for pos in xrange(len(path) - 1):
            edge = self.graph[path[pos]][path[pos + 1]]
            edge['band'].deallocate_pos(bitpos)

    def allocate(self, src, dst, method=0, nointerference=False):
        """
        Allocate a lightpath setup request.

        @param src the source node
        @param dst the destination node
        @param method
                      0 for FF (reference scenario)
                      1 for FF - Adaptive
                      2 for FF/LF - Adaptive
                      3 for FF/LF/2 - Adaptive
                      4 for MinCost - Adaptive (theoretical lower bound)
        @param nointerference if True doesn't collect interference
                              information to speed up the simulation
        """
        bands = []
        intersection = 0
        length = 32
        kmdistance = 0

        try:
            if method != 0:
                (length, paths) = shortest_path(self.graph, src, dst)
                path = paths[dst]
            else:
                path = nx.shortest_path(self.graph, src, dst, 'distance')
        except KeyError, exc:
            return None


        # Hop by hop evaluate the intersection among all the links
        # in order to get the final bitvector.

        for pos in xrange(len(path) - 1):
            edge = self.graph[path[pos]][path[pos + 1]]
            band = edge['band']

            kmdistance += edge['kmdistance']

            intersection |= band.state
            length = min(length, band.length)

            bands.append((band, edge['distance']))

        if method == 0 or method == 1:
            pos = allocate_first(intersection, length)

        elif method == 2:
            pos = allocate_side(intersection, length)

        elif method == 3:
            pos = allocate_side_skip2(intersection, length)

        elif method == 4:
            pos = allocate_mincost(intersection, length)

        interferences = []
        distances = []

        if pos is not None:
            tdistance = 0
            tinterference = 0

            for band, distance in bands:
                tdistance += distance
                tinterference += band.interference_at(pos) * distance
                band.allocate_pos(pos)

            if not nointerference:
                interferences.append(tinterference)
                distances.append(len(bands))
        else:
            return None

        return (pos, distances, interferences, path)

    @classmethod
    def load_from_data(cls, contents, wl):
        graph = nx.Graph()
        maxdist = 0

        for line in contents.splitlines():
            src, dst, dist = line.split(' ', 2)

            src = int(src)
            dst = int(dst)
            dist = int(dist)

            maxdist = max(dist, maxdist)

            graph.add_edge(int(src), int(dst), {
                'kmdistance': dist,
                'band': FrequencyBand(wl),
            })

        for src, dst in graph.edges():
            graph[src][dst]['distance'] = float(graph[src][dst]['kmdistance']) / maxdist

        return graph

    @classmethod
    def load_graph(cls, file, wl):
        """
        Load a graph from a file normalizing the distances of each edge.
        """
        with open(file, 'r') as f:
            graph = nx.Graph()

            # Skip the first line
            f.readline()

            maxdist = 0

            for line in f:
                src, dst, dist = line.split(' ', 2)

                src = int(src)
                dst = int(dst)
                dist = int(dist)

                maxdist = max(dist, maxdist)

                graph.add_edge(src, dst, {
                    'kmdistance': dist,
                    'band': FrequencyBand(wl),
                })

            for src, dst in graph.edges():
                graph[src][dst]['distance'] = float(graph[src][dst]['kmdistance']) / maxdist

            return graph

    @classmethod
    def random(cls, number):
        #return nx.random_geometric_graph(number, 0.125)
        #return nx.petersen_graph()
        return nx.tetrahedral_graph()

    def draw(self):
        import matplotlib.pyplot as plt

        nx.draw(self.graph)
        plt.savefig("graph.png")


if __name__ == "__main__":
    Graph().draw()
