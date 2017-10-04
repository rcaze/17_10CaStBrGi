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
G = br2.NeuronGroup(1, threshold="v>thetaU", reset="v=0*mV", model=eq)
G.run_regularly('''
               v += clip(Ie, 0*mV, 0.5*mV)
               Ie = 0*mV
               ''', when='after_synapses')
mon = br2.StateMonitor(G, "v", record = True)

ext_in = br2.SpikeGeneratorGroup(3, [0, 1, 2], np.array([1, 5, 5])*ms)
exc_syn = br2.Synapses(ext_in, G, on_pre='Ie += 0.5*mV', delay=5*ms)
exc_syn.connect()
br2.run(25 * ms)

import matplotlib.pyplot as plt
plt.plot(mon.t/ms, mon.v[0]/mV)
plt.show()
