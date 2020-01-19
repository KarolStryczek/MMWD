s = (
        [5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3],  # 0
        [2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],  # 1
    )

n_workers = 30
default_cost = 2000
n_required_shifts = s[1]  # Whole week
n_iters = 20
tabu_size = 20
n_weeks = 4
how_often_organize = 10
how_often_sort = 20
shift_penalty = 1
week_penalty = 2
default_acceptable_shifts = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
percent_acceptable_shifts = 50
gauss_avg = 3000
gauss_sd = 500
reward_for_badness = 0.05
