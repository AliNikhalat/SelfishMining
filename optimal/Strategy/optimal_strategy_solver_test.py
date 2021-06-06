from optimal_strategy_solver import OptimalSolver

alpha = 0.35
gamma = 0
max_fork_len = 8
show_log = True

optimal_solver = OptimalSolver(alpha, gamma, max_fork_len, show_log)
optimal_solver.start_solving()
