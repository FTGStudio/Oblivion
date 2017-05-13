from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer

def getData(h_obj,signal):
    # Set the signal to be the first 5 seconds of data
    signal_seg = signal[0:1249]
    # Set the signal to be processed
    h_obj.set_signal(signal_seg)
    # Process signal and show the result in the GUI
    h_obj.process()
    # Print the calculated heart rates
    h_obj.print_heart_rate()
    # Print the calculated average heart rate
    print h_obj.calc_avg_heart_rate()


# Import the data from a csv file
signal, mdata = storage.load_txt('nicks_heart_short_1.csv')
# Create class for heart process
h = heart(mdata['sampling_rate'])
# Set the function to run every x seconds
RepeatedTimer(5,getData,h,signal)
