import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from biosppy.signals import ecg

signal, mdata = storage.load_txt('nicks_heart_short_1.csv')
Fs = mdata['sampling_rate']
N = len(signal)
T = (N-1)/Fs
ts = np.linspace(0, T, N, endpoint=False)
out = ecg.ecg(signal=signal, sampling_rate=Fs, show=False)


pl.plot(ts, signal, lw=2)
pl.grid()
#pl.show()
print(out[6][-1])
