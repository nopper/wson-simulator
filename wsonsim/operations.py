import math
import heapq

def freebits(x, length=32):
    """
    Generator returning position of free slots (bit position set to 0)
    @param x a bit-vector
    @param length the length in bit of the bit-vector
    """
    for pos in xrange(length):
        if x & (1 << pos) == 0:
            yield pos

def interference(target, bitvect, length=32):
    """
    Evaluate the interference perceived by slot target
    @param target the target slot position
    @param bitvect the bit-vector
    @param the length in bit of the bit-vector
    @return a float representing the interference level
    """
    interf = 0
    for pos in xrange(length):
        if target == pos:
            continue
        if bitvect & (1 << pos) != 0:
            diff = float(abs(target - pos))
            interf += math.log(((diff * 2) + 1) / ((diff - 1) * 2 + 1))
    return interf

def allocate_mincost(bitvect, bitlength):
    positions = []
    for bitpos in freebits(bitvect, bitlength):
        positions.append((interference(bitpos, bitvect, bitlength), bitpos))

    if not positions:
        return None

    return min(positions)[1]

def allocate_side(bitvect, bitlength):
    limit = bitlength // 2

    fst_l = find_first_free(bitvect, 0, 1, 0, limit)
    fst_r = find_first_free(bitvect, bitlength - 1, -1, limit, bitlength)

    if fst_r is None and fst_l is None:
        return None

    if fst_r is None and fst_l is not None:
        return fst_l
    if fst_l is None and fst_r is not None:
        return fst_r

    diff_r = bitlength - 1 - fst_r
    diff_l = fst_l

    if diff_r < diff_l:
        return fst_r
    else:
        return fst_l

def allocate_side_skip2(bitvect, bitlength):
    limit = bitlength // 2

    fst_l = find_first_free(bitvect, 0, 1, 0, limit)
    fst_r = find_first_free(bitvect, bitlength - 1, -1, limit, bitlength)

    if fst_r is None and fst_l is None:
        return None

    if fst_r is None and fst_l is not None:
        return fst_l
    if fst_l is None and fst_r is not None:
        return fst_r

    if fst_l == 1:
        new_l = find_first_free(bitvect, 2, 1, 0, limit)
        if new_l is not None:
            fst_l = new_l

    if fst_r == bitlength - 2:
        new_r = find_first_free(bitvect, bitlength - 3, -1, limit, bitlength)
        if new_r is not None:
            fst_r = new_r

    diff_r = bitlength - 1 - fst_r
    diff_l = fst_l

    if diff_r < diff_l:
        return fst_r
    else:
        return fst_l

def allocate_center(bitvect, bitlength):
    tgt = bitlength // 2

    if bitvect & (1 << tgt) == 0:
        return tgt

    fst_r = find_first_free(bitvect, tgt + 1, 1, 0, bitlength)
    fst_l = find_first_free(bitvect, tgt - 1, -1, 0, bitlength)

    if fst_r is None and fst_l is None:
        return None

    if fst_r is None and fst_l is not None:
        return fst_l
    if fst_l is None and fst_r is not None:
        return fst_r

    diff_r = fst_r - tgt
    diff_l = tgt - fst_l

    if diff_r < diff_l:
        return fst_r
    else:
        return fst_l

def find_first_free(bitvect, start, add, lower, upper):
    while start >= lower and start < upper:
        if bitvect & (1 << start) == 0:
            return start
        start += add

def allocate_first(bitvect, bitlength):
    return find_first_free(bitvect, 0, 1, 0, bitlength)

def shortest_path(G, source, target):
    """
    Dijsktra adaptive algorithm. This is a readaption version of the networkx's
    Dijsktra's shortest path algorithm implementation.

    @param G the a nx.Graph object
    @param source the source node
    @param target the destination node
    @return a tuple (dict_dist, dict_paths)
    """
    dist = {}  # dictionary of final distances
    paths = {source: [source]}  # dictionary of paths
    seen = {source: 0}
    fringe=[] # use heapq with (distance,label) tuples

    if source == target:
        return (0, paths)

    heapq.heappush(fringe, (0, 32 - 32, source, 0, 32))

    while fringe:
        d, _, v, band, length = heapq.heappop(fringe)

        # already searched this node.
        if v in dist:
            continue

        dist[v] = d

        if v == target:
            break

        edata = iter(G[v].items())

        for w, edgedata in edata:
            vw_dist = dist[v] + edgedata.get('distance', 1)

            vw_band = edgedata['band']
            curr_band = vw_band.state | band
            curr_length = min(vw_band.length, length)

            free = False
            empty = 32

            for pos in xrange(curr_length):
                if curr_band & (1 << pos) == 0:
                    free = True
                else:
                    empty -= 1

            if not free:
                # Intersection gave no free slot
                continue

            if w in dist:
                if vw_dist < dist[w]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif w not in seen or vw_dist < seen[w]:
                seen[w] = vw_dist
                heapq.heappush(fringe, (vw_dist, empty, w, curr_band, curr_length))
                paths[w] = paths[v] + [w]

    return (dist, paths)
