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

    def print_heart_rate(self):
        print self.result['heart_rate']

    def process(self):
        self.result = ecg.ecg(signal=self.sig, sampling_rate=self.Fs, show=False)

    def process_show(self):
        self.result = ecg.ecg(signal=self.sig, sampling_rate=self.Fs, show=True)

    def calc_avg_heart_rate(self):
        self.avg_hr = np.mean(self.result['heart_rate'])
        return self.avg_hr
