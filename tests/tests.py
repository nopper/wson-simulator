import os
import sys
import math
import unittest

sys.path.insert(0, os.getcwd())
from wsonsim.network import FrequencyBand, Graph, shortest_path

GRAPH = """1 2 80
2 3 80
3 4 80
4 1 80
"""

GRAPH_ALGO = """1 2 80
1 3 80
2 4 80
3 4 80
4 5 80
"""

class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        self.wavelengths = 4
        self.graph = Graph(file=None, contents=GRAPH_ALGO, wl=self.wavelengths)

    def test_first_fit_saturation(self):
        """
        This test try to allocate all the wavelengths on the link 4, 5
        and then check if that an extra allocation result in a block
        """

        for i in xrange(self.wavelengths):
            self.graph.allocate(1, 5)

        self.assertTrue(self.graph.allocate(4, 5) is None)


class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(file=None, contents=GRAPH)

    def test_simple(self):
        for i in range(32):
            self.graph.allocate(1, 3)


class TestFreqBand(unittest.TestCase):
    def setUp(self):
        self.band = FrequencyBand()

    def test_deallocation(self):
        self.band.allocate_pos(0)
        self.assertTrue(self.band.state == 1)
        self.band.deallocate_pos(0)
        self.assertTrue(self.band.state == 0)

        self.band.allocate_pos(0)
        self.band.allocate_pos(1)
        self.assertTrue(self.band.state == 3)
        self.band.deallocate_pos(1)
        self.assertTrue(self.band.state == 1)

    def test_interference(self):
        """
        Check that the interference evaluation is correct by using
        the example provided.
        """
        for pos in (0, 1, 4, 6):
            self.band.allocate_pos(pos)

        interference = 1

        for x, y in ((3, 1), (7, 5), (7, 5), (5, 3)):
            interference *= float(x) / float(y)

        interference = math.log(interference)

        self.assertTrue(self.band.interference_at(3) == interference)

    def test_saturate(self):
        ret = [self.band.allocate_center() for i in range(32)]
        ret.sort()

        self.assertTrue(ret == range(32))

    def test_center(self):
        delta = 0

        for _ in range(16):
            self.assertTrue(self.band.allocate_center() == 16 + delta)
            delta += 1
            self.assertTrue(self.band.allocate_center() == 16 - delta)

        self.assertTrue(self.band.allocate_center() is None)

    def test_side(self):
        left, right = 0, 31

        for _ in range(16):
            self.assertTrue(self.band.allocate_side() == left)
            self.assertTrue(self.band.allocate_side() == right)

            left += 1
            right -= 1

    def test_complete(self):
        for _ in range(16):
            self.assertTrue(self.band.allocate_center() is not None)
            self.assertTrue(self.band.allocate_side() is not None)

        self.assertTrue(self.band.allocate_side() is None)
        self.assertTrue(self.band.allocate_center() is None)

if __name__ == '__main__':
    unittest.main()
