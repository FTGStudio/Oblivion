import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage

signal, mdata = storage.load_txt('Nicks_ECG_single_channel.csv')
Fs = mdata['sampling_rate']
N = len(signal)
T = (N-1)/Fs
ts = np.linspace(0, T, N, endpoint=False)
pl.plot(ts, signal, lw=2)
pl.grid()
pl.show()
