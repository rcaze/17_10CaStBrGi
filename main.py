import numpy as np
from lib import run, group_size_ev, save_gsize, coloring
from plot import pop, markov, grid
import brian2 as br2
import matplotlib.pyplot as plt
from itertools import product

def fig2():
    spikes = run(ext_w=0.26, inh_w=0.26, linear=True)
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


def fig1():
    """Generate the first figure of the plos article"""
    par_range = np.linspace(0.16, 0.4, 5, endpoint=True)
    colors = np.zeros((len(par_range), len(par_range), 3))
    linear = False
    for i, j in product(range(len(par_range)), range(len(par_range))):
        c = coloring(par_range[i], par_range[j] , linear)
        colors[j][i] = np.array(c)
    grid(par_range * 150, colors, save="grid_nl.png")

    colors = np.zeros((len(par_range), len(par_range), 3))
    linear = True
    for i, j in product(range(len(par_range)), range(len(par_range))):
        c = coloring(par_range[i], par_range[j] , linear)
        colors[j][i] = np.array(c)
    grid(par_range * 150, colors, save="grid_l.png")

fig1()
