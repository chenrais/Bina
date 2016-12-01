import collections
from numpy import random
from ways.graph import load_map_from_csv


def gen_random_route(roads):  #dror: we should call this function the same way we called load_map_from_csv
    rand = random.randint(len(roads))
    l = [rand]
    while random.random() < .99: # dror: is this the way to toss a coin with p=0.99?
        # neighbours = [x.target for x in roads[rand].links]
        # if neighbours:
        #     rand = random.choice(neighbours)
        if roads[rand].links:
            rand = random.choice([x.target for x in roads[rand].links])
            l.append(rand)
        else:
            break
    return l

def generate_centers(roads): # N == len(roads)
    full_list = []
    for i in range (500000):  #TODO change this to 500000
        full_list += gen_random_route(roads)
        print(i)
    centers = collections.Counter(full_list).most_common()
    # print(centers)
    #centers.sort(lambda x: x[1], centers)
    write_to_centrality_csv(centers)
    return [x[0] for x in centers]  # we return a list of id's and occurrences count


def write_to_centrality_csv(centers_list):
    f = open('centrality.csv', 'w')
    for i in centers_list:
        f.write(str(i[0])+','+str(i[1])+'\n')





if __name__ == '__main__':
    centers = generate_centers(load_map_from_csv())
    # print(centers)