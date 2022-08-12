from sm1_strategy import SelfishMiningOne

iteration_number = 10000

selfish_mining_one = SelfishMiningOne(False)
selfish_mining_one.alpha = 0.5
selfish_mining_one.gamma = 1
selfish_mining_one.print_input_statistic()

selfish_mining_one.start_simulate(iteration_number)
selfish_mining_one.print_final_result()

# selfish_mining_one.visualize_data(iteration_number)
