from Scheduler import Scheduler
import CustomeWorkers


def my_tabu_search(first_solution, iters, tabu_list_size=30):
    best = first_solution
    best_candidate = first_solution
    tabu_list = list()
    tabu_list.append(first_solution)
    for i in range(iters):
        if i % 10 == 0:
            print(best)
        best.set_working_first()
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
    first_solution = Scheduler(CustomeWorkers.randomized_workers())
    best_solution = my_tabu_search(first_solution, 1000, 100)
    print(first_solution.get_total_cost(), best_solution.get_total_cost())
    print(best_solution)
