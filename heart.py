import numpy as np
from biosppy.signals import ecg

class heart:
    def __init__(self, sampleRate):
        self.sig = []
        self.Fs = sampleRate
        self.heartRate = []
        self.i = 0

    def add_heart_rate(self, heart_rate):
        self.heartRate.append(heart_rate)

    def ready_to_send(self):
        return len(self.heartRate)

    def get_avg_heart_rate(self):
        temp = 0.0
        if len(self.heartRate) is not 0:
            temp = sum(self.heartRate) / float(len(self.heartRate))
            self.heartRate = []
        return temp

    def getData(self, signal):
        if (self.i*250)+1249 >= len(signal):
            self.i = 0
            print "Reset CSV"
        # Set the signal to be the previous 5 seconds of data
        signal_seg = signal[(self.i*250):(self.i*250)+1249]
        # Set the signal to be processed
        self.set_signal(signal_seg)
        # Process signal and show the result in the GUI
        self.process()
        # Print the calculated heart rates
        # self.print_heart_rate()
        # Print the calculated average heart rate
        self.hr = self.calc_avg_heart_rate()
        # print int(self.hr)
        self.add_heart_rate(self.hr)
        # Set the time to increase by 3 seconds
        self.i += 3

    def set_signal(self, signal):
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
