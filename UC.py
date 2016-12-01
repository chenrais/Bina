from ways.graph import Link
from ways.graph import Junction
from ways.graph import Roads
import heapq
from ways.graph import load_map_from_csv



# def retrack_path(src_id, end_state):
#     l = []
#     l.

# def UC(src, roads, dest_list, number_of_wanted_results = 1):
#     '''
#     :type src: Junction
#     :type dest_list: List[Junction]
#     :type roads: Roads
#     :type number_of_wanted_results: int
#     '''
#     dest_set= set(dest_list)
#     results = []
#     close = {}  # dictionary: key is nodes index, value is (junction, [path_by_id])
#     open = [[0, src, [src.index]]]  # cost , node, path: by id list
#     #todo maybe it would be faster to also save a dict named opened_dict, key is id and value is cost and so we save the list search in line 37 for most of the iterations
#     while open:
#         next_node= heapq.heappop(open)
#         close[next_node[1].index] = next_node
#         if (next_node[1].index in dest_set) and (next_node[1].index != src.index):
#             results.append(next_node)
#             if len(results) == number_of_wanted_results:
#                 return results
#         for link in next_node[1].links:
#             if not link.target in close:
#                 new_cost = link[2] + next_node[0]
#                 new_path = next_node[2] + [link.target]
#                 old_node = next((x for x in open if x[1].index == link.target),None)
#                 if old_node:  # note that this is depending on positive costs
#                     if old_node[0] > new_cost:
#                         old_node = next((x for x in open if x[1].index == link.target), None)  # new improvement
#                         open = [x for x in open if x[1].index != old_node[1].index]  # we remove the old node from the list
#                         old_node[0] = new_cost
#                         old_node[2] = new_path
#                         heapq.heapify(open) # maybe this isn't needed.. i don't know what happened when i've extracted
#                         #  an item from the queue forcefully
#                         heapq.heappush(open, old_node)
#                 else:
#                     new = [new_cost, roads[link.target], new_path]
#                     heapq.heappush(open, new)
#     return results
# ## returns a list of [cost, junction, [path]

def UC_faster(src, roads, dest_list, number_of_wanted_results = 1, re_execute = 0):
    '''
    :type src: Junction
    :type dest_list: List[Junction]
    :type roads: Roads
    :type number_of_wanted_results: int
    '''
    dest_set= set(dest_list)
    results = []
    close = {}  # dictionary: key is nodes index, value is (junction, [path_by_id])
    open = [[0, src, [src.index]]]  # cost , node, path: by id list
    #todo maybe it would be faster to also save a dict named opened_dict, key is id and value is cost and so we save the list search in line 37 for most of the iterations
    opened_dict = {src.index: 0}
    while open:
        next_node= heapq.heappop(open)
        opened_dict.pop(next_node[1].index)
        close[next_node[1].index] = next_node
        if (next_node[1].index in dest_set) and (next_node[1].index != src.index):
            results.append(next_node)
            if len(results) == number_of_wanted_results:
                 return results, len(close)
            else:
                continue
        for link in next_node[1].links:
            if link.target not in close:
                new_cost = link[2] + next_node[0]
                new_path = next_node[2] + [link.target]
                # old_node = next((x for x in open if x[1].index == link.target),None)   new improvement
                if link.target in opened_dict:  # note that this is depending on positive costs
                    if opened_dict[link.target] > new_cost:
                        old_node = next((x for x in open if x[1].index == link.target), None)  # new improvement
                        open = [x for x in open if x[1].index != old_node[1].index]  # we remove the old node from the list
                        old_node[0] = new_cost
                        old_node[2] = new_path
                        open.append(old_node)
                        heapq.heapify(open) # maybe this isn't needed.. i don't know what happened when i've extracted
                        #  an item from the queue forcefully
                        opened_dict[link.target] = new_cost
                else:
                    new = [new_cost, roads[link.target], new_path]
                    heapq.heappush(open, new)
                    opened_dict[link.target] = new_cost
    return results, len(close)


def UC_original_graph(src, dest_list, number_of_wanted_results = 1,re_execute = 0):
    roads = load_map_from_csv()
    return UC_faster(src, roads, dest_list, re_execute=re_execute)



if __name__ == '__main__':
    print(' ')
