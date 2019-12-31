from Assumptions import Assumptions


# __init__ with some defaults
# Defaults
default_cost = 2000
default_acceptable_shifts = (True for i in range(21))
default_schedule = [False for shift in range(Assumptions.n_weeks * 7 * 3)]


class Worker:
    # TODO below?
    # Values below will be used in generating random Worker
    # max_cost = 10000
    # min_cost = 2000
    # min_acceptable_shifts = 12

    # __init__ with some defaults
    # Defaults
    default_cost = 2000
    default_acceptable_shifts = [True for i in range(21)]

    def __init__(self, cost=default_cost, acceptable_shifts=default_acceptable_shifts):
        self.cost = cost
        self.acceptable_shifts = acceptable_shifts
        self.schedule = [False for shift in range(Assumptions.n_weeks * 7 * 3)]

    def __str__(self):
        string = ""
        for shift in self.schedule:
            string += 'X' if shift else '_'
        return string + '\n'

    def is_working(self):
        for shift in self.schedule:
            if shift:
                return True
        return False


