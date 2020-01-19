s = (
        [13, 7, 3, 13, 7, 3, 13, 7, 3, 13, 7, 3, 13, 7, 3, 10, 5, 2, 6, 2, 0],  # 0
        [2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],  # 1
        [5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3],  # 2
    )

workers_type = "equal"
n_workers = 100
default_cost = 2000
gauss_avg = 3000
gauss_sd = 500
n_required_shifts = s[2]  # Whole week
n_iters = 400
tabu_size = 30
n_weeks = 1
percent_acceptable_shifts = 50


how_often_organize = 10
how_often_sort = 20
shift_penalty = 1
week_penalty = 5
reward_for_badness = 0.05
