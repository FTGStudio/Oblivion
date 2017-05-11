from biosppy import storage
from heart import heart

# Import the data from a csv file
signal, mdata = storage.load_txt('nicks_heart_short_1.csv')
# Set the signal to be the first 5 seconds of data
signal_seg = signal[0:1249]

# Create class for heart process
h = heart(mdata['sampling_rate'])
# Set the signal to be processed
h.set_signal(signal_seg)
# Process signal and show the result in the GUI
h.process_show()
