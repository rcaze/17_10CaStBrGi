import numpy as np
import os
import h5py
import brian2 as br2
from brian2 import mV, ms
from itertools import product
from plot import pop

def set_neuron():
    """Set the neuron model"""
    pass

def save_gsize(gsize, fname="dat.hdf", linear=True):
    """Save the Brian object into an h5 file"""
    with h5py.File(fname, "a") as hdf:
        if linear:
            hdf.create_dataset(name="linear", data=gsize)
        else:
            hdf.create_dataset(name="nonlinear", data=gsize)
    pass

def save_grid(hists, exc_w, inh_w, fname="grid.hdf", linear=True):
    """Save the Brian object into an h5 file"""
    with h5py.File(fname, "a") as hdf:
        if linear:
            hdf.create_dataset(name="e_%s_i_%s_l" % (exc_w, inh_w), data=hists)
        else:
            hdf.create_dataset(name="e_%s_i_%s_nl" % (exc_w, inh_w), data=hists)
    pass


def load_gsize(fname="dat.hdf", linear=True):
    """Save the Brian object into an h5 file"""
    with h5py.File(fname, "r") as hdf:
        if linear:
            return np.array(hdf["linear"])
        else:
            return np.array(hdf["nonlinear"])
    pass

def group_size_ev(group_size, repet_n=1, linear=True):
    """Return the evolution of the group size"""
    group_ev = []
    for i in range(repet_n):
        spikes = run(56, group_size=group_size, g_time=50, linear=linear)
        dt = br2.defaultclock.dt/(2 * ms)
        g_size = np.sum(np.abs(spikes.t/ms - 55) < dt)
        group_ev.append(g_size)
    return group_ev

def grid_search(weights=np.arange(0.16, 0.4, 0.375/150.),
                n_rep=1,
                linear=True):
    """Perform a parameter sweep and record the result in an hdf5 file"""
    for ext, inh in product(weights, weights):
        hists = []
        for i in range(n_rep):
            spikes = run(ext_w=ext, inh_w=inh, linear=linear)
            hist_glob, hist_g = pop(spikes)
            c_hist = [np.max(hist_glob[:1000])] + hist_g.tolist()
            hists.append(c_hist)
        save_grid(np.array(hists), ext, inh, linear=linear)

def run(TSTOP=250, group_size=100, g_time=150, neuron_n=1000, linear=True
        ,ext_w=0.2 ,inh_w=0.2):
    """Run a simulation and return the resulting spiketrain"""
    # Basic equation of the model
    eq = """dv/dt = -gamma*v + I0 : volt
    Ie : volt
    Ii : volt
    """

    thetaU = 16 * mV
    tauM = 8 * ms
    gamma = 1 / tauM
    I0 = 17.6 * mV / tauM

    #Build the group of neuron to use
    G = br2.NeuronGroup(neuron_n, threshold="v>thetaU", reset="v=0*mV",
                        method='euler',
                        model=eq)

    #Record the spikes from this group
    spikes = br2.SpikeMonitor(G)

    #Build stimulation
    stim = br2.SpikeGeneratorGroup(1, [0], [g_time]*ms - br2.defaultclock.dt)
    stim_syn = br2.Synapses(stim, G, on_pre="v += 2*thetaU")
    stim_syn.connect(i=0, j=np.arange(group_size))
    br2.magic_network.schedule = ['start', 'groups', 'synapses', 'thresholds', 'resets', 'end']
    connections = np.random.rand(1000, 1000) < 0.3
    exc_or_inh  = np.random.rand(1000, 1000) < 0.5
    exc_i, exc_j = (connections & exc_or_inh).nonzero()
    inh_i, inh_j = (connections & ~exc_or_inh).nonzero()

    if linear:
        G.run_regularly('''
                        v += Ie + Ii
                        Ie = 0*mV
                        Ii = 0*mV
                        ''', when='after_synapses')
    else:
        G.run_regularly('''
                        v += clip(Ie, 0*mV, 2*mV) + clip(2*(Ie-2*mV), 0*mV, 4*mV) + Ii
                        Ie = 0*mV
                        Ii = 0*mV
                        ''', when='after_synapses')

    dt = br2.defaultclock.dt
    exc_syn = br2.Synapses(G, G, on_pre='Ie += %s*mV' % (ext_w), delay=5*ms-dt)
    inh_syn = br2.Synapses(G, G, on_pre='Ii -= %s*mV' % (inh_w), delay=5*ms-dt)
    exc_syn.connect(i=exc_i, j=exc_j)
    inh_syn.connect(i=inh_i, j=inh_j)

    #Set random initial conditions
    G.v = np.random.rand(neuron_n) * 16 * mV

    br2.run(TSTOP * ms)

    return spikes

def coloring(ext_w, inh_w, linear, fname="grid.hdf"):
    """Color the points given from the data"""
    if linear:
        data_name = "e_%s_i_%s_l" % (ext_w, inh_w)
    else:
        data_name = "e_%s_i_%s_nl" % (ext_w, inh_w)

    with h5py.File(fname, "r") as hdf:
        data = np.array(hdf[data_name][0])
        if data[0] >= 100:
            if np.min(data[1:]) > data[0]:
                return (1, 1, 0)
            else:
                return (1, 0, 0)
        else:
            if np.min(data[1:]) > data[0]:
                return (0, 0, 1)
            else:
                return (0, 1, 0)


if __name__ == "__main__":
    #os.remove("grid.hdf")
    # This range requires ~10 min computation time on a laptop
    par_range = np.linspace(0.16, 0.4, 5, endpoint=True)
    grid_search(par_range)
    grid_search(par_range, linear=False)
