from Assumptions import Assumptions


class Worker:
    def __init__(self, cost, acceptable_shifts):
        self.cost = cost
        self.acceptable_shifts = acceptable_shifts
        self.schedule = [False for shift in range(Assumptions.n_weeks * 7 * 3)]

    def __str__(self):
        string = ""
        for i in range(len(self.schedule)):
            if i % 21 == 0:
                string += '|'
            if self.schedule[i]:
                string += 'V' if self.acceptable_shifts[i % 21] else 'X'
            else:
                string += '_' if self.acceptable_shifts[i % 21] else ' '
        return string + " " + str(self.get_cost()) + " " + str(self.how_bad_am_i()) + '\n'

    def __hash__(self):
        return hash(tuple(self.schedule))

    def get_cost(self):
        return self.cost

    def how_bad_am_i(self):
        badness = 0
        for i in range(len(self.schedule)):
            if self.schedule[i] and not self.acceptable_shifts[i % 21]:
                badness += 1
            if sum(self.schedule[max(i-21, 0):i]) > 3:
                badness += 5
        return badness

    def is_working(self):
        for shift in self.schedule:
            if shift:
                return True
        return False

    def is_allowed(self):
        for i in range(len(self.schedule)-2):
            if self.schedule[i]:
                if self.schedule[i+1] or self.schedule[i+2]:
                    return False
        if self.schedule[-1] and self.schedule[-2]:
            return False
        return True

    def count_unaccepted_shifts(self):
        unaccepted_shifts = 0
        for i in range(len(self.schedule)):
            if self.schedule[i] and not self.acceptable_shifts[i % 21]:
                unaccepted_shifts += 1
        return unaccepted_shifts

    def is_acceptable(self):
        return self.count_unaccepted_shifts() == 0

    def is_pretending_to_be_acceptable(self):
        return self.count_unaccepted_shifts() < Assumptions.max_unaccepted_shifts


# acc = (1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0)
# sch = (1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0)
# w1 = Worker(2000, acc)
# w1.schedule = sch
# print(w1.how_bad_am_i())
