from biosppy import storage
from heart import heart
from time import sleep
import numpy as np

#one file to fakes serial port
data = open('rawNoHead.txt')

# Import the data from a csv file
signal, mdata = storage.load_txt('nicks_heart_1.csv')
# Set the signal to be the first 5 seconds of data
signal_seg = signal[0:1249]

# Create class for heart process
h = heart(mdata['sampling_rate'])

print signal

winCh1 = np.array([])
winCh2 = np.array([])
winCh3 = np.array([])

while True:
    #simulate serial message at 250 Hz
    sleep(0.004)
    dataline = data.readline();

    datalist = dataline.split(", ")

    winCh1 = np.append(winCh1, float(datalist[1]));
    winCh2 = np.append(winCh2, float(datalist[2]));
    winCh3 = np.append(winCh3, float(datalist[3]));

    if len(winCh1) == 1250:
        #this is window of 5 seconds - process it yo.

        # Set the signal to be processed
        print winCh1
        h.set_signal(winCh1)
        h.process()
        winCh1 = winCh1[-750:]
        winCh2 = winCh2[-750:]
        winCh3 = winCh3[-750:]

