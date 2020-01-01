# https://medium.com/@ms.kaleia/tabu-search-gentle-introduction-46c479eb6525

"""
This implementation for tabu search is modified from:
https://www.techconductor.com/algorithms/python/Search/Tabu_Search.php

Reference:
https://www.researchgate.net/publication/242527226_Tabu_Search_A_Tutorial
"""
import copy
import math

from Scheduler import Scheduler
from Worker import Worker


def distance(point1, point2):
    raise NotImplementedError
    # return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def generate_neighbours(points):
    raise NotImplementedError
    """This function generates a 2D distance matrix between all points

    Parameters
    ----------
    points : type
        Description of parameter `points`.

    Returns
    -------
    type
        Description of returned object.

    """
    dict_of_neighbours = {}

    # for i in range(len(points)):
    #     for j in range(i + 1, len(points)):
    #         if i not in dict_of_neighbours:
    #             dict_of_neighbours[i] = {}
    #             dict_of_neighbours[i][j] = distance(points[i], points[j])
    #         else:
    #             dict_of_neighbours[i][j] = distance(points[i], points[j])
    #             # dict_of_neighbours[i] = sorted(dict_of_neighbours[i].items(), key=lambda kv: kv[1])
    #         if j not in dict_of_neighbours:
    #             dict_of_neighbours[j] = {}
    #             dict_of_neighbours[j][i] = distance(points[j], points[i])
    #         else:
    #             dict_of_neighbours[j][i] = distance(points[j], points[i])
    #             # dict_of_neighbours[i] = sorted(dict_of_neighbours[i].items(), key=lambda kv: kv[1])
    #
    # return dict_of_neighbours


def generate_first_solution(nodes, dict_of_neighbours):
    raise NotImplementedError
    # start_node = nodes[0]
    # end_node = start_node
    #
    # first_solution = []
    # distance = 0
    # visiting = start_node
    # pre_node = None
    # while visiting not in first_solution:
    #     _tmp = copy.deepcopy(dict_of_neighbours[visiting])
    #     _tmp.pop(pre_node, None)
    #     next_node = min(_tmp.items(), key=lambda x: x[1])[0]
    #     distance += dict_of_neighbours[visiting][next_node]
    #     first_solution.append(visiting)
    #     pre_node = visiting
    #     visiting = next_node
    #
    # first_solution.append(nodes[0])
    # distance += dict_of_neighbours[pre_node][end_node]
    # return first_solution, distance


def get_neighborhood(solution, dict_of_neighbours, n_opt=1):
    neighborhood_of_solution = []
    for n in solution[1:-n_opt]:
        idx1 = []
        n_index = solution.index(n)
        for i in range(n_opt):
            idx1.append(n_index + i)

        for kn in solution[1:-n_opt]:
            idx2 = []
            kn_index = solution.index(kn)
            for i in range(n_opt):
                idx2.append(kn_index + i)
            if bool(
                    set(solution[idx1[0]:(idx1[-1] + 1)]) &
                    set(solution[idx2[0]:(idx2[-1] + 1)])):
                continue

            _tmp = copy.deepcopy(solution)
            for i in range(n_opt):
                _tmp[idx1[i]] = solution[idx2[i]]
                _tmp[idx2[i]] = solution[idx1[i]]

            distance = 0
            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                distance = distance + dict_of_neighbours[k][next_node]

            _tmp.append(distance)
            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    index_of_last_item_in_the_list = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[index_of_last_item_in_the_list])
    return neighborhood_of_solution


def tabu_search(first_solution, cost_of_first_solution, dict_of_neighbours, iters, size, n_opt=1):
    count = 1
    best_solution_ever = first_solution
    solution = first_solution
    best_cost = cost_of_first_solution
    tabu_list = list()
    while count <= iters:
        # neighborhood = get_neighborhood(solution, dict_of_neighbours, n_opt=n_opt)
        neighborhood = solution.get_neighbours()
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1
        found = False
        while found is False:
            i = 0
            first_exchange_node, second_exchange_node = [], []
            n_opt_counter = 0
            while i < len(best_solution):
                if best_solution[i] != solution[i]:
                    first_exchange_node.append(best_solution[i])
                    second_exchange_node.append(solution[i])
                    n_opt_counter += 1
                    if n_opt_counter == n_opt:
                        break
                i = i + 1

            exchange = first_exchange_node + second_exchange_node
            if first_exchange_node + second_exchange_node not in tabu_list and second_exchange_node + first_exchange_node not in tabu_list:
                tabu_list.append(exchange)
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            elif index_of_best_solution < len(neighborhood):
                best_solution = neighborhood[index_of_best_solution]
                index_of_best_solution = index_of_best_solution + 1

        while len(tabu_list) > size:
            tabu_list.pop(0)

        count = count + 1
    best_solution_ever.pop(-1)
    return best_solution_ever, best_cost


def my_tabu_search(first_solution, iters, tabu_list_size=30):
    best = first_solution
    best_candidate = first_solution
    tabu_list = list()
    tabu_list.append(first_solution)
    for i in range(iters):
        print("{0}/{1} best cost: {2}".format(i, iters, best.get_total_cost()))
        neighbours = best_candidate.get_neighbours()
        for neighbour in neighbours:
            if neighbour not in tabu_list and neighbour.is_allowed() and neighbour.get_total_cost() <= best_candidate.get_total_cost():
                best_candidate = neighbour
        if best_candidate.get_total_cost() <= best.get_total_cost():
            best = best_candidate
        tabu_list.append(best_candidate)
        if len(tabu_list) > tabu_list_size:
            del tabu_list[0]
    return best


if __name__ == '__main__':
    # tabu_search(generate_first_solution( , generate_neighbours()), , generate_neighbours(), , )
    first_solution = Scheduler()
    best = my_tabu_search(first_solution, 30, 100)
    print(first_solution.get_total_cost(), best.get_total_cost())
    print(best)

