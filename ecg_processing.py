import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from biosppy.signals import ecg
import threading

def process_hr(sig):
    # threading.Timer(3, process_hr(sig)).start()
    out = ecg.ecg(signal=signal, sampling_rate=Fs, show=True)
    # print out['heart_rate']
    # print "Hi"


signal, mdata = storage.load_txt('nicks_heart_short_1.csv')
signal_seg = signal[0:1249]
Fs = mdata['sampling_rate']
N = len(signal_seg)
T = (N-1)/Fs
ts = np.linspace(0, T, N, endpoint=False)
process_hr(signal_seg)

# print "ts"
# print out['ts']
# print "filtered"
# print out['filtered']
# print "rpeaks"
# print out['rpeaks']
# print "templates"
# print out['templates']
# print "templates_ts"
# print out['templates_ts']
# print "heart_rate_ts"
# print out['heart_rate_ts']
# print "heart_rate"
# print out['heart_rate']



# pl.plot(ts, signal, lw=2)
# pl.grid()
# pl.show()
