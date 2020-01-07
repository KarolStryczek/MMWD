from Assumptions import Assumptions


class Worker:
    def __init__(self, cost, acceptable_shifts):
        self.cost = cost
        self.acceptable_shifts = acceptable_shifts
        self.schedule = [False for shift in range(Assumptions.n_weeks * 7 * 3)]

    def __str__(self):
        string = ""
        for shift in self.schedule:
            string += 'X' if shift else '_'
        return string + " " + str(self.cost) + '\n'

    def __hash__(self):
        return hash(tuple(self.schedule))

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
