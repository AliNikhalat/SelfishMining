import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from matplotlib import pyplot as plt  # NOQA

from nik_sm.nik_sm_strategy import NikSelfishMining  # NOQA

iteration_number = 10000

tow_number = 10
min_tow_block_number = 4
max_tow_block_number = 6

reward_rate = 0
penalty_rate = 0

min_k = 1
max_k = 3


selfish_mining_nik = NikSelfishMining(
    tow_number, min_tow_block_number, max_tow_block_number, reward_rate, penalty_rate, min_k, max_k, False)
selfish_mining_nik.alpha = 0.45
selfish_mining_nik.gamma = 0
# selfish_mining_nik.print_input_statistic()

# selfish_mining_nik.start_simulate(iteration_number)
# selfish_mining_nik.print_final_result()

alpha_values = [x / 100 for x in range(51) if x % 5 == 0]
selfish_revenue_value_0 = []
selfish_revenue_value_0_5 = []
selfish_revenue_value_1 = []
upper_bound_value = []
honest_revenue_value = []

for alpha in alpha_values:
    selfish_mining_nik.reset()

    selfish_mining_nik.alpha = alpha
    selfish_mining_nik.start_simulate(iteration_number)
    selfish_mining_nik.print_final_result()
    selfish_revenue_value_0.append(selfish_mining_nik.revenue)

selfish_mining_nik.gamma = 0.5

for alpha in alpha_values:
    selfish_mining_nik.reset()

    selfish_mining_nik.alpha = alpha
    selfish_mining_nik.start_simulate(iteration_number)
    selfish_mining_nik.print_final_result()
    selfish_revenue_value_0_5.append(selfish_mining_nik.revenue)

selfish_mining_nik.gamma = 1

for alpha in alpha_values:
    selfish_mining_nik.reset()

    selfish_mining_nik.alpha = alpha
    selfish_mining_nik.start_simulate(iteration_number)
    selfish_mining_nik.print_final_result()
    selfish_revenue_value_1.append(selfish_mining_nik.revenue)

for alpha in alpha_values:
    honest_revenue_value.append(alpha * 100)

for alpha in alpha_values:
    upper_bound_value.append(alpha / (1 - alpha) * 100)


plt.plot(
    alpha_values, selfish_revenue_value_0, color='r', label='Nik SM(Gamma = 0)')
plt.plot(
    alpha_values, selfish_revenue_value_0_5, color='b', label='Nik SM(Gamma = 0.5)')
plt.plot(
    alpha_values, selfish_revenue_value_1, color='y', label='Nik SM(Gamma = 1)')

plt.plot(alpha_values, honest_revenue_value,
         color='k', label='honest mining', linestyle='dashdot')
plt.plot(
    alpha_values, upper_bound_value, color='g', label='Upper Bound', linestyle='dashed')

# plt.plot(alpha_values, honest_revenue_value,
#          color='k', label='honest mining')

plt.title('Nik Selfish Mining-Ex3')
plt.xlabel('Pool size')
plt.ylabel('Relative Revenue')

plt.legend(loc="upper left")

plt.show()
