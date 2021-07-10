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
min_tow_block_number = 4
max_tow_block_number = 6

reward_rate = 0.1
penalty_rate = 0.01

min_k = 1
max_k = 3

nik_defense = NikSelfishMining(
    tow_number, min_tow_block_number, max_tow_block_number, reward_rate, penalty_rate, min_k, max_k, False)
nik_defense.gamma = 0.5

selfish_mining_one = SelfishMiningOne(False)
selfish_mining_one.gamma = 1

tie_breaking_defense = SelfishMiningOne(False)
tie_breaking_defense.gamma = 0.5

alpha_values = [x / 100 for x in range(25, 51) if x % 5 == 0]
nik_defense_revenue = []
one_selfish_revenue = []
tie_breaking_defense_revenue = []
upper_bound_value = []
ideal_defense_revenue_value = []

nik_defense_stale_block = []
one_selfish_stale_block = []
tie_breaking_stale_block = []


for alpha in alpha_values:
    nik_defense.reset()

    nik_defense.alpha = alpha
    nik_defense.start_simulate(iteration_number)
    nik_defense.print_final_result()
    nik_defense_revenue.append(nik_defense.revenue)
    nik_defense_stale_block.append(nik_defense.stale_block)


for alpha in alpha_values:
    tie_breaking_defense.reset()

    tie_breaking_defense.alpha = alpha
    tie_breaking_defense.start_simulate(iteration_number)
    tie_breaking_defense.print_final_result()
    tie_breaking_defense_revenue.append(tie_breaking_defense.revenue)
    tie_breaking_stale_block.append(tie_breaking_defense.stale_block)


for alpha in alpha_values:
    selfish_mining_one.reset()

    selfish_mining_one.alpha = alpha
    selfish_mining_one.start_simulate(iteration_number)
    selfish_mining_one.print_final_result()
    one_selfish_revenue.append(selfish_mining_one.revenue)
    one_selfish_stale_block.append(selfish_mining_one.stale_block)

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
    alpha_values, nik_defense_revenue, color='r', label='Nik Defense', linestyle=linestyles_dict['densely dotted'], linewidth=2)
plt.plot(
    alpha_values, tie_breaking_defense_revenue, color='b', label='Tie Breaking', linestyle=linestyles_dict['densely dashdotdotted'],  linewidth=1.5)
plt.plot(
    alpha_values, one_selfish_revenue, color='y', label='No Defense', linewidth=1.5)

plt.plot(alpha_values, ideal_defense_revenue_value,
         color='k', label='Ideal Defense', linestyle=linestyles_dict['densely dashed'], linewidth=1.5)
plt.plot(
    alpha_values, upper_bound_value, color='g', label='Upper Bound', linestyle=linestyles_dict['dashdotdotted'], linewidth=1.5)


plt.title('ُNik Defense Relative Revenue Comparison-Ex4.1.5')
plt.xlabel('Pool size')
plt.ylabel('Relative Revenue')

plt.legend(loc="upper left")

plt.show()


alpha_values[-1] = 0.48

nik_defense.alpha = alpha
nik_defense.reset()
nik_defense.start_simulate(iteration_number)
nik_defense_stale_block[-1] = nik_defense.stale_block

tie_breaking_defense.alpha = alpha
tie_breaking_defense.reset()
tie_breaking_defense.start_simulate(iteration_number)
tie_breaking_stale_block[-1] = tie_breaking_defense.stale_block

selfish_mining_one.alpha = alpha
selfish_mining_one.reset()
selfish_mining_one.start_simulate(iteration_number)
one_selfish_stale_block[-1] = selfish_mining_one.stale_block


plt.title('ُNik Defense Stale Block Comparison-Ex4.3.5')
plt.xlabel('Pool size')
plt.ylabel('ُStale Block Number')

plt.plot(
    alpha_values, nik_defense_stale_block, color='r', label='Nik Defense', linestyle=linestyles_dict['densely dotted'], linewidth=2)
plt.plot(
    alpha_values, tie_breaking_stale_block, color='b', label='Tie Breaking', linestyle=linestyles_dict['densely dashdotdotted'],  linewidth=1.5)
plt.plot(
    alpha_values, one_selfish_stale_block, color='y', label='No Defense', linewidth=1.5)

plt.legend(loc="upper left")

plt.show()
