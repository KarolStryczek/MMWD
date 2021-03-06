from typing import List
from Worker import Worker
import Assumptions
from random import seed, gauss, randrange


def get_workers(mode: str) -> List[Worker]:
    if mode == "gauss":
        workers = []
        # seed random number generator
        seed(1)
        for i in range(Assumptions.n_workers):
            # generate random Gaussian value
            cost = round(gauss(Assumptions.gauss_avg, Assumptions.gauss_sd))
            acceptable_shifts = []
            for j in range(len(Assumptions.n_required_shifts)):
                acceptable_shifts.append(int(true_for_random_percentage(Assumptions.percent_acceptable_shifts)))
            workers.append(Worker(cost, acceptable_shifts))
        return workers
    elif mode == "equal":
        workers = []
        # seed random number generator
        for i in range(Assumptions.n_workers):
            # generate random Gaussian value
            cost = Assumptions.default_cost
            acceptable_shifts = []
            for j in range(len(Assumptions.n_required_shifts)):
                acceptable_shifts.append(int(true_for_random_percentage(Assumptions.percent_acceptable_shifts)))
            workers.append(Worker(cost, acceptable_shifts))
        return workers
    else:
        raise NotImplementedError


def true_for_random_percentage(percent=50):
    return randrange(100) < percent
