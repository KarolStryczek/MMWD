from Assumptions import Assumptions
from copy import deepcopy
from Worker import Worker
from typing import List
import random


class Scheduler:
    def __init__(self, workers: List[Worker] = None):
        self.workers = None
        if workers is None:
            self.default_workers()
        else:
            self.custom_workers(workers)

    def __str__(self):
        string = ""
        for worker in self.workers:
            string += str(worker) if worker.is_working() else ''
        return string

    def __eq__(self, other):
        if len(self.workers) == len(other.workers):
            for i in range(len(self.workers)):
                for j in range(len(self.workers[i].schedule)):
                    if self.workers[i].schedule[j] != other.workers[i].schedule[j]:
                        return False
            return True
        else:
            return False

    def __hash__(self):
        return hash(tuple(self.workers))

    def how_bad_am_i(self):
        return sum([worker.how_bad_am_i() for worker in self.workers])

    def is_better(self, other):
        diff = self.get_total_cost() - other.get_total_cost()
        if diff < 0:
            return True
        elif diff > 0:
            return False
        else:
            not_worse = self.how_bad_am_i() <= other.how_bad_am_i()
            return True if not_worse or (sum(self.workers[0].schedule) < sum(other.workers[0].schedule) and not_worse) else False

    def default_workers(self):
        acceptable_shifts = Assumptions.default_acceptable_shifts
        self.workers = [Worker(Assumptions.starting_cost + i*Assumptions.cost_increase, acceptable_shifts) for i in range(Assumptions.n_workers)]
        shifts_assigned = 0
        n_workers_available = Assumptions.n_workers
        for week in range(Assumptions.n_weeks):
            for i in range(len(Assumptions.n_required_shifts)):
                j = Assumptions.n_required_shifts[i]
                while j > 0:
                    self.workers[shifts_assigned % n_workers_available].schedule[week*3*7 + i] = True
                    shifts_assigned += 1
                    j -= 1

    def custom_workers(self, workers: List[Worker]):
        self.workers = workers
        shifts_assigned = 0
        n_workers_available = len(self.workers)
        for week in range(Assumptions.n_weeks):
            for i in range(len(Assumptions.n_required_shifts)):
                j = Assumptions.n_required_shifts[i]
                while j > 0:
                    self.workers[shifts_assigned % n_workers_available].schedule[week*3*7 + i] = True
                    shifts_assigned += 1
                    j -= 1

    def get_total_cost(self) -> int:
        return sum([worker.get_cost() for worker in self.workers if worker.is_working()])

    def swap_workers(self, w1, w2):
        self.workers[w1].schedule, self.workers[w2].schedule = self.workers[w2].schedule, self.workers[w1].schedule

    def swap_shifts(self, w1, w2, shift):
        self.workers[w1].schedule[shift], self.workers[w2].schedule[shift] = self.workers[w2].schedule[shift], self.workers[w1].schedule[shift]

    def collapse_workers(self, w1: Worker, w2: Worker):
        collapsed_shifts = []
        can_collapse = True
        for s1, s2 in zip(self.workers[w1].schedule, self.workers[w2].schedule):
            if s1 == s2 == 1:
                can_collapse = False
                break
            collapsed_shifts.append(s1 or s2)
        if self.workers[w1].get_cost() < self.workers[w2].get_cost() and can_collapse:
            self.workers[w1].schedule, self.workers[w2].schedule = \
                collapsed_shifts, [0] * len(collapsed_shifts)
        elif can_collapse:
            self.workers[w2].schedule, self.workers[w1].schedule = \
                collapsed_shifts, [0] * len(collapsed_shifts)

    # def get_neighbours(self):
    #     neighbours = set()
    #     # Swapping workers
    #     for i in range(len(self.workers)):
    #         for j in range(i+1, len(self.workers)):
    #             neighbour = deepcopy(self)
    #             neighbour.swap_workers(i, j)
    #             neighbours.add(neighbour)
    #     # Swapping shifts
    #     for i in range(len(self.workers)):
    #         for j in range(len(self.workers[i].schedule)):
    #             if self.workers[i].schedule[j]:
    #                 for k in range(len(self.workers)):
    #                     neighbour = deepcopy(self)
    #                     neighbour.swap_shifts(i, k, j)
    #                     neighbours.add(neighbour)
    #     # Collapsing shifts
    #     for i in range(len(self.workers)):
    #         for k in range(len(self.workers)):
    #             neighbour = deepcopy(self)
    #             neighbour.collapse_workers(i, k)
    #             neighbours.add(neighbour)
    #     return neighbours

    # def get_neighbours(self):
    #     neighbours = set()
    #     # Swapping workers
    #     i = 0
    #     for j in range(i+1, len(self.workers)):
    #         neighbour = deepcopy(self)
    #         neighbour.swap_workers(i, j)
    #         neighbours.add(neighbour)
    #     # Swapping shifts
    #     for j in range(len(self.workers[i].schedule)):
    #         if self.workers[i].schedule[j]:
    #             for k in range(len(self.workers)):
    #                 neighbour = deepcopy(self)
    #                 neighbour.swap_shifts(i, k, j)
    #                 neighbours.add(neighbour)
    #     # Collapsing shifts
    #     for k in range(len(self.workers)):
    #         neighbour = deepcopy(self)
    #         neighbour.collapse_workers(i, k)
    #         neighbours.add(neighbour)
    #     return neighbours

    def get_neighbours(self, i: int):
        neighbours = set()
        i = 0
        if i % 20 == 0:
            # Swapping workers
            for j in range(i+1, len(self.workers)):
                neighbour = deepcopy(self)
                neighbour.swap_workers(i, j)
                neighbours.add(neighbour)
        # Swapping shifts
        for j in range(0, len(self.workers[0].schedule)):
            if self.workers[i].schedule[j]:
                for k in range(len(self.workers)):
                    neighbour = deepcopy(self)
                    neighbour.swap_shifts(i, k, j)
                    neighbours.add(neighbour)
        return neighbours

    def get_sorted_neighbourhood(self):
        neighbours = list(self.get_neighbours())
        neighbours.sort(key=lambda neighbour: neighbour.get_total_cost())
        return neighbours

    def is_allowed(self):
        return sum([worker.is_allowed() for worker in self.workers]) == len(self.workers)

    def set_working_first(self, should_i_sort: bool):
        if should_i_sort:
            self.workers.sort(key=lambda w: w.get_cost() if w.is_working() and w.how_bad_am_i() == 0 else (1000000 if w.how_bad_am_i() > 0 else -1), reverse=True)
        i = 1
        while not self.workers[0].is_working():
            self.workers[0], self.workers[i] = self.workers[i], self.workers[0]
            i += 1

    def randomize_me(self):
        self.workers.sort(key=lambda w: random.randint(0, 10000) % 132 + random.randint(0, 10000) % 32 - 15)

# scheduler = Scheduler()
# scheduler.workers.append(Worker(3000, Assumptions.default_acceptable_shifts))
# for worker in scheduler.workers:
#     print(worker.cost)
