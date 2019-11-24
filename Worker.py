class Worker:
    # Values below will be used in generating random Worker
    max_cost = 10000
    min_cost = 2000
    min_acceptable_shifts = 12

    def __init__(self, cost, skills, acceptable_shifts):
        self.cost = cost
        self.skills = skills
        self.acceptable_shifts = acceptable_shifts
        self.current_position = None

    def __init__(self):
        # TODO Generate some random values and call init above
        raise NotImplementedError
