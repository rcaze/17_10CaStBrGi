import brian2 as br2
import numpy as np
from brian2 import mV, ms

eq = """dv/dt = -gamma*v + I0 : volt
        Ie : volt
        Ii : volt
"""

thetaU = 16 * mV
tauM = 8 * ms
gamma = 1 / tauM
I0 = 17.6 * mV / tauM
neuron_n = 1000

G = br2.NeuronGroup(neuron_n, threshold="v>thetaU", reset="v=0*mV", model=eq)

mon = br2.StateMonitor(G, "v", record = 0)
spikes = br2.SpikeMonitor(G)

connections = np.random.rand(1000, 1000) < 0.3
exc_or_inh  = np.random.rand(1000, 1000) < 0.5
exc_i, exc_j = (connections & exc_or_inh).nonzero()
inh_i, inh_j = (connections & ~exc_or_inh).nonzero()
G.run_regularly('''
               v += Ie + Ii
               Ie = 0*mV
               Ii = 0*mV
               ''', when='after_synapses')

exc_syn = br2.Synapses(G, G, on_pre='Ie += 0.2*mV', delay=5*ms)
inh_syn = br2.Synapses(G, G, on_pre='Ii -= 0.2*mV', delay=5*ms)

exc_syn.connect(i=exc_i, j=exc_j)
inh_syn.connect(i=inh_i, j=inh_j)

br2.run(250 * ms, report='text')

import matplotlib.pyplot as plt
# plt.plot(mon.t/ms, mon.v[0]/mV)
plt.plot(spikes.t/ms, spikes.i, '.')
plt.show()
