'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways.graph import load_map_from_csv

import functools
import collections


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions' : len(roads), #dror: we assume any row in csv==junction
        'Number of links' : functools.reduce(lambda x, y: x+y, [len(roads[x].links) for x in roads]),
        'Outgoing branching factor' : Stat(max=max(len(roads[x].links) for x in roads),
                                           min=min(len(roads[x].links) for x in roads),
                                           avg=functools.reduce(lambda x, y: x+y, [len(roads[x].links) for x in roads])/len(roads)),
        'Link distance' : Stat(max=max((lnk.distance) for x in roads for lnk in roads[x].links),
                               min=min((lnk.distance) for x in roads for lnk in roads[x].links),
                               avg=functools.reduce(lambda x, y: x+y, ((lnk.distance) for road in roads for lnk in roads[road].links))
                                                                       /functools.reduce(lambda x, y: x+y, [len(roads[x].links) for x in roads])),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' :dict(collections.Counter(lnk.highway_type for x in roads for lnk in roads[x].links)),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
