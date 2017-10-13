import numpy as np
from lib import run, group_size_ev, save_gsize
from plot import pop, markov
import brian2 as br2
import matplotlib.pyplot as plt

def fig2():
    spikes = run(ext_w=0.36, inh_w=0.16, linear=True)
    hist_glob, hist_g = pop(spikes)
    return np.max(hist_glob[:1000]), hist_g, spikes

def fig3(repet_n=50, fname="dat.hdf"):
    # Must do two separate runs because of Brian2
    group_ev = []
    for i in range(1, 180, 5):
        group_ev.append(group_size_ev(i, repet_n))
        print(i/180.)
        save_gsize(group_ev, fname, linear=True)

    group_ev = []
    for i in range(1, 180, 5):
        group_ev.append(group_size_ev(i, repet_n, linear=False))
        print(i/180.)
        save_gsize(group_ev, fname, linear=False)

print(fig2())
