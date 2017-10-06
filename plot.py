import matplotlib.pyplot as plt
from matplotlib import gridspec
from brian2 import ms
import brian2 as br2
import numpy as np

def pop(spikes, gridmax=170, save=None):
    """Draw and/or save the figure"""
    plt.figure()
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 3])
    # Draw the raster plot
    ax0 = plt.subplot(gs[2])
    ax0.set_xlim(110, 220)

    for i in range(150, gridmax, 5):
        ax0.vlines(i, 0, 200, color="gray", linestyle='dashed')
    ax0.plot(spikes.t/ms, spikes.i, '|', color="black", mew=3, markersize=10)
    red_spikes = ((spikes.t >= 150*ms) & ((spikes.t % (5*ms) < br2.defaultclock.dt/2)|
                                          (spikes.t % (5*ms) > (5*ms - br2.defaultclock.dt/2))))

    ax0.plot(spikes.t[red_spikes]/ms, spikes.i[red_spikes], 'r|', mew=3, markersize=10)

    ax0.set_ylim(0, 200)
    ax0.set_ylabel("Neuron")
    ax0.set_xlabel("Time (ms)")

    # Draw the population rate
    ax1 = plt.subplot(gs[1])
    ax1.hist(spikes.t/ms, range(250), color="black")
    #ax1.plot(mon_rat.t/ms, mon_rat.smooth_rate(width=1*ms)/Hz, color="black")
    ax1.set_ylim(0, 250)
    ax1.set_ylabel("Rate")
    ax1.set_xlim(110, 220)
    ax1.set_xlim(110, 220)

    # Draw the group size
    ax2 = plt.subplot(gs[0])
    selected = np.array(spikes.t[red_spikes]/ms)
    selected[selected > 170] = 250
    print(selected)
    ax2.hist(selected, range(250), color="red")
    #ax1.plot(mon_rat.t/ms, mon_rat.smooth_rate(width=1*ms)/Hz, color="black")
    ax2.set_ylim(0, 250)
    ax2.set_ylabel("g'")
    ax2.set_xlim(110, 220)
    ax2.set_xlim(110, 220)

    if save:
        plt.savefig(save + ".png")
    else:
        plt.show()
