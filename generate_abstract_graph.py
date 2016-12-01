
import time
import ways.graph
from ways.graph import AbstractLink, Junction
from ways.graph import load_map_from_csv
import UC
import UC
from centers_generation import generate_centers
import functools
import pickle

def get_path_by_junctions(path_by_id, roads):
    return [roads[x] for x in path_by_id]



def get_path_by_links(path_by_id, roads):
    '''
    :type path_by_junctions: List[Junction]
    :param path_by_junctions:
    :return:
    '''
    path_by_junctions = get_path_by_junctions(path_by_id, roads)
    path_by_links = []
    for i in range (len(path_by_junctions) -1):
        path_by_links += [link for link in path_by_junctions[i].links if link.target == path_by_junctions[i+1].index]
    return path_by_links

# def create_abstract_map(roads, list_of_centers_id, m):
#     '''
#
#     :type roads: Roads
#     :param roads:
#     :param list_of_centers_id:
#     :param m:
#     :return:
#     '''
#     centers = [roads[c_id] for c_id in list_of_centers_id]
#     abstract_map = {}
#     i = 0  # debug print
#     for center in centers:
#         neighbours = UC.UC(center, roads, list_of_centers_id, int(m * len(centers)))  # a_list of tuples (neighbour_id, path)
#         links = [AbstractLink(neighbour[2],neighbour[1].index, neighbour[0], -1) for neighbour in neighbours]
#         i += 1  # debug print
#         # print(str(i)+'/'+str(len(centers)))  # debug print
#         abstract_map[center.index] = Junction(center.index, center.lat, center.lon, links)
#     return abstract_map


def create_abstract_map_faster(roads, list_of_centers_id, m):
    '''

    :type roads: Roads
    :param roads:
    :param list_of_centers_id:
    :param m:
    :return:
    '''
    centers = [roads[c_id] for c_id in list_of_centers_id]
    abstract_map = {}
    i = 0  # debug print
    for center in centers:
        neighbours = UC.UC_faster(center, roads, list_of_centers_id, int(m * len(centers)))  # a_list of tuples (neighbour_id, path)
        links = [AbstractLink(neighbour[2],neighbour[1].index, neighbour[0], -1) for neighbour in neighbours]
        i += 1  # debug print
        print(str(i)+'/'+str(len(centers)))  # debug print
        abstract_map[center.index] = Junction(center.index, center.lat, center.lon, links)
    return abstract_map

def get_centers_from_centrality_file(file_path):
    f = open(file_path, 'r')
    centers_id_list = []
    for line in f:
        s = line.split(',')
        centers_id_list.append(int(s[0]))
    f.close()
    return centers_id_list


if __name__ == '__main__':
    roads = load_map_from_csv()
    centers_id = get_centers_from_centrality_file('centrality.csv')
    for k in [0.0025, 0.005, 0.01, 0.05]:
        kN = int(k * len(centers_id))
        kcenters_id = centers_id[:kN]
        start_time = time.time()
        print(kcenters_id)
        abs_map = create_abstract_map_faster(roads, kcenters_id, 0.1)
        print('the length of 0.005 is: ' + str(len(abs_map)))
        print("---"+str(k)+" abs graph generation --- %s min ---" % str((time.time() - start_time) / 60))
        pickle.dump(abs_map, open("abstract"+str(k)+".pkl", "wb"))
