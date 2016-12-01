
from ways.graph import load_map_from_csv
import random
import heapq

def UCDataSet(src, roads):
    '''
    :type src: Junction
    :type dest_list: List[Junction]
    :type roads: Roads
    :type number_of_wanted_results: int
    '''
    results = []
    close = {}  # dictionary: key is nodes index, value is (junction, [path_by_id])
    open = [[0, src, [src.index]]]  # cost , node, path: by id list
    while open:
        next_node= heapq.heappop(open)
        close[next_node[1].index] = next_node
        # if ncloseext[1].index in centers_id_list:

        if next_node[0]>200:
            results.append(next_node[1].index)
            if len(results) == 1:
                return results
        for link in next_node[1].links:
            if not link.target in close:
                new_cost = 1 + next_node[0]
                new_path = next_node[2] + [link.target]
                old_node = next((x for x in open if x[1].index == link.target),None)
                if old_node:
                    if old_node[0] > new_cost:
                        open = [x for x in open if x[1].index != old_node[1].index]  # we remove the old node from the list
                        old_node[0] = new_cost
                        old_node[2] = new_path
                        heapq.heapify(open) # maybe this isn't needed.. i don't know what happened when i've extracted
                        #  an item from the queue forcefully
                        heapq.heappush(open, old_node)
                else:
                    new = [new_cost, roads[link.target], new_path]
                    heapq.heappush(open, new)
    return results
## returns a list of [cost, junction, [path]

if __name__ == '__main__':
    roads=load_map_from_csv()
    f = open('dataSet.csv', 'w')
    counter=0
    while (counter<20):
        x=random.randint(0,len(roads))
        ucResult=UCDataSet(roads[x], load_map_from_csv())
        for y in ucResult:
            f.write(str(x) + ',' + str(y) + '\n')
            counter=counter+1
    f.close()


