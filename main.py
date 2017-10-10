from lib import run, group_size_ev, save_gsize
from plot import pop, markov


# Must do two separate runs because of Brian2
"""
group_ev = []
for i in range(1, 180, 5):
    group_ev.append(group_size_ev(i, 50))
    print(i/180.)
save_gsize(group_ev, linear=True)
"""

group_ev = []
for i in range(1, 180, 5):
    group_ev.append(group_size_ev(i, 50, linear=False))
    print(i/180.)
save_gsize(group_ev, linear=False)
