from nik_sm import NikSelfishMining

iteration_number = 10000

tow_number = 10
min_tow_block_number = 4
max_tow_block_number = 6

selfish_mining_nik = NikSelfishMining(
    tow_number, min_tow_block_number, max_tow_block_number, False)
selfish_mining_nik.alpha = 0.48
selfish_mining_nik.gamma = 0.5
# selfish_mining_nik.print_input_statistic()

selfish_mining_nik.start_simulate(iteration_number)
selfish_mining_nik.print_final_result()

selfish_mining_nik.visualize_data(iteration_number)
