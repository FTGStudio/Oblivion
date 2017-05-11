import numpy as np
from biosppy.signals import ecg

class heart:
    def __init__(self, sampleRate):
        self.sig = []
        self.Fs = sampleRate

    def set_signal(self,signal):
        self.sig = signal
        self.N = len(self.sig)
        self.T = (self.N-1)/self.Fs
        self.ts = np.linspace(0, self.T, self.N, endpoint=False)

    def print_signal(self):
        print "Signal:"
        print self.sig

    def process(self):
        result = ecg.ecg(signal=self.sig, sampling_rate=self.Fs, show=False)

    def process_show(self):
        result = ecg.ecg(signal=self.sig, sampling_rate=self.Fs, show=True)
