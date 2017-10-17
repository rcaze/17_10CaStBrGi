import matplotlib.pyplot as plt
from matplotlib import gridspec
from brian2 import ms
import brian2 as br2
import numpy as np


def s(save=None, fig=None):
    """Code snippet to use at the end of making a figure"""
    if save:
        plt.tight_layout()
        plt.savefig(save, dpi=800)
        plt.close(fig)
    else:
        plt.show()


def pop(spikes, ymax1=250, gridmax=220, save=None):
    """Draw and/or save the figure"""
    plt.figure()
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 3])
    # Draw the raster plot
    ax0 = plt.subplot(gs[2])
    ax0.set_xlim(110, 220)

    for i in range(150, gridmax, 5):
        ax0.vlines(i, 0, 200, color="gray", linestyle='dashed')
    ax0.plot(spikes.t/ms, spikes.i, '|', color="black", mew=3, markersize=10)
    red_spikes = ((spikes.t >= 150*ms) &
                  ((spikes.t % (5*ms) < br2.defaultclock.dt / 2) |
                   (spikes.t % (5*ms) > (5*ms - br2.defaultclock.dt / 2))))

    ax0.plot(spikes.t[red_spikes]/ms, spikes.i[red_spikes], 'r|', mew=3,
             markersize=10)

    ax0.set_ylim(0, 200)
    ax0.set_ylabel("Neuron")
    ax0.set_xlabel("Time (ms)")

    # Draw the population rate
    ax1 = plt.subplot(gs[1])
    if save is not None:
        ax1.hist(spikes.t/ms, range(250), color="black")
    else:
        h_glob, b, p = ax1.hist(spikes.t/ms, np.arange(0.05, 250, 0.1),
                                color="black")
    ax1.set_ylim(0, ymax1)
    ax1.set_ylabel("Rate")
    ax1.set_xlim(110, 220)
    ax1.set_xlim(110, 220)
    ax1.set_xticklabels("")

    # Draw the group size
    ax2 = plt.subplot(gs[0])
    selected = np.array(spikes.t[red_spikes]/ms)
    selected[selected > gridmax] = 250

    if save is not None:
        ax2.hist(selected, range(250), color="red")
    else:
        h_g, b, p = ax2.hist(selected, np.arange(0.05, 250, 0.1), color="red")
        # Extract only the
        h_g = h_g[range(1499, 1999, 50)]
    ax2.set_ylim(0, 250)
    ax2.set_ylabel("g'")
    ax2.set_xlim(110, 220)
    ax2.set_xlim(110, 220)
    ax2.set_xticklabels("")

    if save:
        plt.savefig(save + ".png")
    elif save is None:
        # Save data to see what is the color of the pixel
        plt.close('all')
        return h_glob, h_g
    else:
        plt.show()


def markov(group_ev, max_size=180, save=None, linear=True):
    """Plot the most probable evolution of a group size at time t+1 given the
    size at time t"""
    fig, ax = plt.subplots(dpi=200, figsize=(5, 5))
    ax.plot(np.arange(1, max_size+1, 5), np.array(group_ev), marker='_',
            ms=7,
            mew=1,
            color="black",
            linestyle='', alpha=0.3)
    ax.plot(np.arange(1, max_size+1, 5),
            np.mean(np.array(group_ev), axis=1),
            marker='s', color="lime", ms=3,
            linestyle='')
    ax.plot(np.arange(0, max_size), np.arange(0, max_size), color="black")
    ax.tick_params(direction='in', pad=5)
    ax.set_aspect('equal')
    ax.set_xticks([1] + range(25, max_size+1, 25))
    ax.set_yticks([1] + range(25, max_size+1, 25))
    ax.set_xlim(0, max_size)
    plt.ylim(0, max_size)
    plt.xlabel("# of synchronized neurons g'0")
    plt.ylabel("# of synchronized neurons g'1")

    # Making an inset
    plt.axes([0.17, 0.65, .2, .2])
    if linear:
        plt.plot(range(11), range(11), color='black')
    else:
        plt.plot(range(11), range(11), color='gray')
        plt.plot(range(11),
                 range(3) + [4, 6] + [6 for i in range(6)], color='black')
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xticks([])
    plt.yticks([])

    s(save, fig=fig)


def grid(par_range, colors, save=None):
    """Draw the result of a parameter search"""
    fig, ax = plt.subplots(dpi=200, figsize=(5, 5))
    ax.imshow(colors, extent=[min(par_range),
                              max(par_range),
                              max(par_range),
                              min(par_range)])
    ax.set_xlabel("Total ext weight")
    ax.set_ylabel("Total Inh weight")
    s(save, fig=fig)


if __name__ == "__main__":
    """
    from lib import load_gsize
    gsize = load_gsize()
    gsize_nl = load_gsize(linear=False)
    markov(gsize, linear=True, save="markov.png")
    markov(gsize_nl, linear=False, save="markov_nl.png")
    """
    par_range = np.linspace(0, 5, 2)
    im = grid(par_range, np.zeros((2, 2)))
