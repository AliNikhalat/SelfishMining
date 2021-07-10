import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from matplotlib import pyplot as plt  # NOQA
from collections import OrderedDict  # NOQA

from nik_sm.nik_sm_strategy import NikSelfishMining  # NOQA
from sm1.sm1_strategy import SelfishMiningOne  # NOQA

iteration_number = 10000

tow_number = 10

reward_rate = 0.1
penalty_rate = 0.01

min_tow_block_number_1 = 4
max_tow_block_number_1 = 6

min_k = 1
max_k = 3

nik_defense_1 = NikSelfishMining(
    tow_number, min_tow_block_number_1, max_tow_block_number_1, reward_rate, penalty_rate, min_k, max_k, False)
nik_defense_1.gamma = 0.5


min_tow_block_number_2 = 8
max_tow_block_number_2 = 10

nik_defense_2 = NikSelfishMining(
    tow_number, min_tow_block_number_2, max_tow_block_number_2, reward_rate, penalty_rate, min_k, max_k, False)
nik_defense_2.gamma = 0.5

min_tow_block_number_3 = 14
max_tow_block_number_3 = 16

nik_defense_3 = NikSelfishMining(
    tow_number, min_tow_block_number_3, max_tow_block_number_3, reward_rate, penalty_rate, min_k, max_k, False)
nik_defense_3.gamma = 0.5


alpha_values = [x / 100 for x in range(25, 51) if x % 5 == 0]

nik_defense_1_revenue = []
nik_defense_1_stale_block = []

nik_defense_2_revenue = []
nik_defense_2_stale_block = []

nik_defense_3_revenue = []
nik_defense_3_stale_block = []

ideal_defense_revenue_value = []
upper_bound_value = []


for alpha in alpha_values:
    nik_defense_1.reset()

    nik_defense_1.alpha = alpha
    nik_defense_1.start_simulate(iteration_number)
    nik_defense_1.print_final_result()
    nik_defense_1_revenue.append(nik_defense_1.revenue)
    nik_defense_1_stale_block.append(nik_defense_1.stale_block)

for alpha in alpha_values:
    nik_defense_2.reset()

    nik_defense_2.alpha = alpha
    nik_defense_2.start_simulate(iteration_number)
    nik_defense_2.print_final_result()
    nik_defense_2_revenue.append(nik_defense_2.revenue)
    nik_defense_2_stale_block.append(nik_defense_2.stale_block)

for alpha in alpha_values:
    nik_defense_3.reset()

    nik_defense_3.alpha = alpha
    nik_defense_3.start_simulate(iteration_number)
    nik_defense_3.print_final_result()
    nik_defense_3_revenue.append(nik_defense_3.revenue)
    nik_defense_3_stale_block.append(nik_defense_3.stale_block)

for alpha in alpha_values:
    ideal_defense_revenue_value.append(alpha * 100)

for alpha in alpha_values:
    upper_bound_value.append(alpha / (1 - alpha) * 100)


linestyles_dict = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])


plt.plot(
    alpha_values, nik_defense_1_revenue, color='r', label='BlocksInTow=5', linestyle=linestyles_dict['densely dotted'], linewidth=1.5)
plt.plot(
    alpha_values, nik_defense_2_revenue, color='b', label='BlocksInTow=9', linestyle=linestyles_dict['densely dashdotdotted'],  linewidth=1.5)
plt.plot(
    alpha_values, nik_defense_3_revenue, color='y', label='BlocksInTow=15', linestyle=linestyles_dict['densely dashed'], linewidth=1.5)

plt.plot(alpha_values, ideal_defense_revenue_value,
         color='k', label='Ideal Defense', linestyle=linestyles_dict['densely dashed'], linewidth=1.5)
plt.plot(
    alpha_values, upper_bound_value, color='g', label='Upper Bound', linestyle=linestyles_dict['dashdotdotted'], linewidth=1.5)

plt.title('ُNik Defense Blocks in Tow Based Revenue Comparison-Ex6')
plt.xlabel('Pool size')
plt.ylabel('Relative Revenue')

plt.legend(loc="upper left")

plt.show()


plt.plot(
    alpha_values, nik_defense_1_stale_block, color='r', label='BlocksInTow=5', linestyle=linestyles_dict['densely dotted'], linewidth=1.5)
plt.plot(
    alpha_values, nik_defense_2_stale_block, color='b', label='BlocksInTow=9', linestyle=linestyles_dict['densely dashdotdotted'],  linewidth=1.5)
plt.plot(
    alpha_values, nik_defense_3_stale_block, color='y', label='BlocksInTow=15', linestyle=linestyles_dict['densely dashed'], linewidth=1.5)


plt.title('ُNik Defense Blocks in Tow Based Stale Block Comparison-Ex6')
plt.xlabel('Pool size')
plt.ylabel('ُStale Block Number')

plt.legend(loc="upper left")

plt.show()
