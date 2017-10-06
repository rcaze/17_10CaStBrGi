import brian2 as br2
import numpy as np
from brian2 import mV, ms, Hz


def run(TSTOP = 250, neuron_n=1000):
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
    G = br2.NeuronGroup(neuron_n, threshold="v>thetaU", reset="v=0*mV", model=eq)

    #Record the spikes from this group
    spikes = br2.SpikeMonitor(G)

    #Build stimulation
    stim = br2.SpikeGeneratorGroup(1, [0], [150]*ms - br2.defaultclock.dt)
    stim_syn = br2.Synapses(stim, G, on_pre="v += 2*thetaU")
    stim_syn.connect(i=0, j=np.arange(100))
    br2.magic_network.schedule = ['start', 'groups', 'synapses', 'thresholds', 'resets', 'end']
    connections = np.random.rand(1000, 1000) < 0.3
    exc_or_inh  = np.random.rand(1000, 1000) < 0.5
    exc_i, exc_j = (connections & exc_or_inh).nonzero()
    inh_i, inh_j = (connections & ~exc_or_inh).nonzero()
    G.run_regularly('''
                    v += clip(Ie, 0*mV, 5* mV) + Ii
                    Ie = 0*mV
                    Ii = 0*mV
                    ''', when='after_synapses')
    exc_syn = br2.Synapses(G, G, on_pre='Ie += 0.2*mV', delay=5*ms)
    inh_syn = br2.Synapses(G, G, on_pre='Ii -= 0.2*mV', delay=5*ms)
    exc_syn.connect(i=exc_i, j=exc_j)
    inh_syn.connect(i=inh_i, j=inh_j)

    #Set initial conditions
    G.v = np.random.rand(neuron_n) * 16 * mV

    br2.run(TSTOP * ms, report='text')

    return spikes
