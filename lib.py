import numpy as np
import h5py
import brian2 as br2
from brian2 import mV, ms


def set_neuron():
    """Set the neuron model"""
    pass

def save_gsize(gsize, fname="data.hdf", linear=True):
    """Save the Brian object into an h5 file"""
    with h5py.File(fname, "a") as hdf:
        if linear:
            hdf.create_dataset(name="linear", data=gsize)
        else:
            hdf.create_dataset(name="nonlinear", data=gsize)
    pass

def load_gsize(fname="data.hdf", linear=True):
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


def run(TSTOP=250, group_size=100, g_time=150, neuron_n=1000, linear=True):
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
    exc_syn = br2.Synapses(G, G, on_pre='Ie += 0.2*mV', delay=5*ms-dt)
    inh_syn = br2.Synapses(G, G, on_pre='Ii -= 0.2*mV', delay=5*ms-dt)
    exc_syn.connect(i=exc_i, j=exc_j)
    inh_syn.connect(i=inh_i, j=inh_j)

    #Set random initial conditions
    G.v = np.random.rand(neuron_n) * 16 * mV

    br2.run(TSTOP * ms)

    return spikes
