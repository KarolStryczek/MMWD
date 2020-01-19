import Assumptions
import random
import string


class Worker:
    def __init__(self, cost, acceptable_shifts):
        self.name = "".join(random.choices(string.ascii_uppercase, k=3))
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
        return string + " " + str(self.get_cost()) + " " + str(self.how_bad_am_i()) + " " + self.name + '\n'

    def __hash__(self):
        return hash(tuple(self.schedule))

    def get_cost(self):
        return round(self.cost*(1+self.how_bad_am_i()*Assumptions.reward_for_badness))

    def how_bad_am_i(self):
        badness = 0
        for i in range(len(self.schedule)):
            if self.schedule[i] and not self.acceptable_shifts[i % 21]:
                badness += Assumptions.shift_penalty
        for i in range(Assumptions.n_weeks):
            if sum(self.schedule[i*21: i*21+20]) > 5:
                badness += Assumptions.week_penalty
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

