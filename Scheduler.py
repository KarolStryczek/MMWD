from Assumptions import Assumptions
from copy import deepcopy


class Scheduler:
    def __init__(self):
        self.workers = list()
        self.schedule = self.random_schedule()
        self.neighbours = self.get_neighbours()

    def random_schedule(self):
        schedule = [[0 for i in Assumptions.n_days * 3] for j in Assumptions.n_workers]
        # TODO Generate random schedule
        return schedule

    def get_total_cost(self) -> int:
        return sum([worker.cost for worker in self.workers])

    def swap_shifts(self, col, row1, row2):
        self.schedule[row1][col], self.schedule[row2][col] = self.schedule[row2][col], self.schedule[row1][col]
        return self

    def swap_workers(self, w1, w2):
        self.schedule[w1], self.schedule[w2] = self.schedule[w2], self.schedule[w1]
        return self

    def is_same_position(self, w1, w2) -> bool:
        return self.workers[w1].current_position == self.workers[w2].current_position

    def get_neighbours(self):
        neighbours = list()
        rows = range(len(self.workers))
        cols = range(len(self.workers[0]))
        # Swapping shifts
        for worker_i in rows:
            for shift_i in cols:
                if self.schedule[worker_i][shift_i] == 1:
                    for compared_worker_i in rows:
                        if self.schedule[compared_worker_i][shift_i] == 0 and self.is_same_position(worker_i, compared_worker_i):
                            neighbour = deepcopy(self).swap_shifts(shift_i, worker_i, compared_worker_i)
                            if neighbour not in neighbours:
                                neighbours.append(neighbour)
        # Swapping workers within same position
        for worker1_i in rows:
            for worker2_i in rows:
                neighbour = deepcopy(self).swap_workers(worker1_i, worker2_i)
                if neighbour not in neighbours and self.is_same_position(worker1_i, worker2_i):
                    neighbours.append(neighbour)
        # Swapping positions

        return neighbours





