from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer


class ex_proc:
    def __init__(self):
        self.i=0

    def getData(self,h_obj,signal):
        # Set the signal to be the previous 5 seconds of data
        signal_seg = signal[(self.i*250):(self.i*250)+1249]
        # Set the signal to be processed
        h_obj.set_signal(signal_seg)
        # Process signal and show the result in the GUI
        h_obj.process()
        # Print the calculated heart rates
        # h_obj.print_heart_rate()
        # Print the calculated average heart rate
        print h_obj.calc_avg_heart_rate()
        # Set the time to increase by 3 seconds
        self.i += 3

# Import the data from a csv file
signal, mdata = storage.load_txt('nicks_heart_1.csv')
# Create class for heart process
h = heart(mdata['sampling_rate'])
# Create an object for the example class
a = ex_proc()
# Set the function to run every x seconds
RepeatedTimer(3,a.getData,h,signal)
