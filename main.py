import numpy as np
from lib import run, group_size_ev, save_gsize, coloring, grid_search
from plot import pop, markov, grid
from itertools import product


def fig1(linear=True, short=True):
    """Generate the grid search and the associated figure"""
    if short:
        par_range = np.linspace(0.16, 0.4, 5, endpoint=True)
        name = "grid_short"
    else:
        par_range = np.linspace(0.16, 0.4, 100, endpoint=True)
        name = "grid"

    fname = name + ".hdf"
    figname = name + ".png"
    #Generate the data
    grid_search(par_range)
    grid_search(par_range, linear=False)
    #Plot
    colors = np.zeros((len(par_range), len(par_range), 3))
    for i, j in product(range(len(par_range)), range(len(par_range))):
        c = coloring(par_range[i], par_range[j] , linear, fname)
        colors[j][i] = np.array(c)
    grid(par_range * 150, colors, save=figname)


def fig2():
    """Generate th raster plot"""
    spikes = run(ext_w=0.2, inh_w=0.2, linear=True)
    spikes_nl = run(ext_w=0.2, inh_w=0.2, linear=False)
    pop(spikes, save="spikes_l.png")
    pop(spikes_nl, save="spikes_nl.png")


def fig3(repet_n=50, fname="dat.hdf"):
    """Generate the last figure of the article"""
    # Generate the data
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

    #Plot the data
    gsize = load_gsize()
    gsize_nl = load_gsize(linear=False)
    markov(gsize, linear=True, save="markov.png")
    markov(gsize_nl, linear=False, save="markov_nl.png")


def all_figs(short=True):
    fig1(short=short)
    fig2()
    if short:
        fig3(2)
    else;
        fig3(50)
