from Assumptions import Assumptions
from copy import deepcopy
from Worker import Worker


class Scheduler:
    def __init__(self):
        self.workers = None
        self.default_workers()

    def __str__(self):
        string = ""
        for worker in self.workers:
            string += str(worker)
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

    def default_workers(self):
        self.workers = [Worker() for i in range(Assumptions.n_workers)]
        shifts_assigned = 0
        n_workers_available = Assumptions.n_workers
        for week in range(Assumptions.n_weeks):
            for i in range(len(Assumptions.n_required_shifts)):
                j = Assumptions.n_required_shifts[i]
                while j > 0:
                    self.workers[shifts_assigned % n_workers_available].schedule[week*3*7 + i] = True
                    shifts_assigned += 1
                    j -= 1

    def get_total_cost(self) -> int:
        return sum([worker.cost for worker in self.workers if worker.is_working()])

    def swap_workers(self, w1, w2):
        self.workers[w1].schedule, self.workers[w2].schedule = self.workers[w2].schedule, self.workers[w1].schedule

    def swap_shifts(self, w1, w2, shift):
        self.workers[w1].schedule[shift], self.workers[w2].schedule[shift] = self.workers[w2].schedule[shift], self.workers[w1].schedule[shift]

    def get_neighbours(self):
        neighbours = set()
        # Swapping workers
        for i in range(len(self.workers)):
            for j in range(i+1, len(self.workers)):
                neighbour = deepcopy(self)
                neighbour.swap_workers(i, j)
                neighbours.add(neighbour)
        # Swapping shifts
        for i in range(len(self.workers)):
            for j in range(len(self.workers[i].schedule)):
                if self.workers[i].schedule[j]:
                    for k in range(len(self.workers)):
                        neighbour = deepcopy(self)
                        neighbour.swap_shifts(i, k, j)
                        neighbours.add(neighbour)
        return neighbours

    def get_sorted_neighbourhood(self):
        neighbours = list(self.get_neighbours())
        neighbours.sort(key=lambda neighbour : neighbour.get_total_cost())
        return neighbours

    def is_allowed(self):
        return sum([worker.is_allowed() for worker in self.workers]) == len(self.workers)


# scheduler = Scheduler()
# scheduler.workers.append(Worker(cost=3000))
# neighbourhood = scheduler.get_sorted_neighbourhood()
# print(neighbourhood[0].get_total_cost(), neighbourhood[-1].get_total_cost())
# print(scheduler)

