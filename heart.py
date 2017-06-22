import numpy as np
import math
from biosppy.signals import ecg

class heart:
    def __init__(self, sampleRate):
        self.sig = []
        self.Fs = sampleRate
        self.heartRate = []
        self.i = 0

    def add_heart_rate(self, heart_rate):
        if not math.isnan(heart_rate):
            self.heartRate.append(heart_rate)

    def ready_to_send(self):
        return len(self.heartRate)

    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    def __is_outlier(self, points, thresh=3.5):
        if len(points.shape) == 1:
            points = points[:,None]
            median = np.median(points, axis=0)
            diff = np.sum((points - median)**2, axis=-1)
            diff = np.sqrt(diff)
            med_abs_deviation = np.median(diff)

        modified_z_score = 0.6745 * diff / med_abs_deviation

        return modified_z_score > thresh


    def get_avg_heart_rate(self):
        temp = 0.0
        numData = 0
        if len(self.heartRate) is not 0:
            outlier = self.__is_outlier(np.array(self.heartRate))
            for isOut, beat in zip(outlier, self.heartRate):
                if not isOut:
                    temp += beat
                    numData += 1
                else:
                    print beat, " is an outlier"
            self.heartRate = []
        return temp / numData

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
