from Worker import Worker
from Assumptions import Assumptions
from random import seed, gauss, randrange


def randomized_workers():
    workers = []
    # seed random number generator
    seed(1)
    for i in range(Assumptions.n_workers):
        # generate random Gaussian value
        cost = round(gauss(3000, 500), 2)
        acceptable_shifts = []
        for i in range(len(Assumptions.n_required_shifts)):
            acceptable_shifts.append(int(true_for_random_percentage(90)))
        workers.append(Worker(cost, acceptable_shifts))
    return workers


def true_for_random_percentage(percent=50):
    return randrange(100) < percent
