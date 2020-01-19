from Scheduler import Scheduler
import WorkersFactory
import Assumptions
from matplotlib import pyplot as plt
import time


def my_tabu_search(first_solution, iters, tabu_list_size=30):
    best = first_solution
    best_good = first_solution
    best_candidate = first_solution
    tabu_list = list()
    tabu_list.append(first_solution)
    stats = [list(), list(), list()]  # [i, cost, badness]
    for i in range(iters):
        if i % 10 == 0:
            print(best)
        if i % Assumptions.how_often_organize == 0:
            best.set_working_first(should_i_sort=(i % Assumptions.how_often_sort == 0))
        print("{0}/{1} best cost: {2}, badness: {3}".format(i, iters, best.get_total_cost(), best.how_bad_am_i()))
        neighbours = best_candidate.get_neighbours(i)
        for neighbour in neighbours:
            if neighbour not in tabu_list and neighbour.is_allowed() and neighbour.is_better(best_candidate):
                best_candidate = neighbour
        if best_candidate.is_better(best):
            if best != best_candidate:
                best = best_candidate
                if best.how_bad_am_i() == 0:
                    best_good = best
            else:
                print("randomizing...")
                best.randomize_me()
        tabu_list.append(best_candidate)
        if len(tabu_list) > tabu_list_size:
            del tabu_list[0]
        stats[0].append(i)
        stats[1].append(best.get_total_cost())
        stats[2].append(best.how_bad_am_i())
    return best, best_good, stats


if __name__ == '__main__':
    # Algorithm
    first_solution = Scheduler(WorkersFactory.get_workers("equal"))
    start = time.time()
    best_solution, best_good, statistics = my_tabu_search(first_solution, Assumptions.n_iters, Assumptions.tabu_size)
    end = time.time()
    time_elapsed = end - start

    print(time_elapsed)

    # Display
    print(first_solution.get_total_cost(), best_solution.get_total_cost())
    print(best_solution)
    plt.plot(statistics[0], statistics[1])
    plt.xlabel("Liczba iteracji")
    plt.ylabel("Koszt")
    plt.title("Funkcja celu [czas: {}s]".format(round(time_elapsed, 2)))
    plt.show()
    plt.plot(statistics[0], statistics[2])
    plt.xlabel("Liczba iteracji")
    plt.ylabel("Liczba niedozwolonych elementów")
    plt.title('"Niedozwoloność" rozwiązania')
    plt.show()
