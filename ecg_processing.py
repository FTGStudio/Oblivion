import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer
from ecg_lora import lora
from coms import get_com
import time

def send_packet_over_lora():
    mote.send_data(5,a.get_hr_int())

class ex_proc:

    def __init__(self):
        self.i=0
        self.hr = 4

    def get_hr_int(self):
        return int(self.hr)

    def getData(self,h_obj,signal):
        if ((self.i*250)+1249 >= len(signal)):
            self.i = 0
            print "Reset CSV"
        # Set the signal to be the previous 5 seconds of data
        signal_seg = signal[(self.i*250):(self.i*250)+1249]
        # Set the signal to be processed
        h_obj.set_signal(signal_seg)
        # Process signal and show the result in the GUI
        h_obj.process()
        # Print the calculated heart rates
        # h_obj.print_heart_rate()
        # Print the calculated average heart rate
        self.hr = h_obj.calc_avg_heart_rate()
        # print int(self.hr)
        # Set the time to increase by 3 seconds
        self.i += 3
        zzz = int(self.hr)

# Set up LoRa mote
# Get LoRa COM port
print "Get LoRa COM Port...",
lora_com = get_com()
print lora_com
# Set up LoRa object
mote = lora(lora_com)
# Join server
mote.connect()

# Import the data from a csv file
print "Importing data from CSV..."
signal, mdata = storage.load_txt('nicks_heart_1.csv')
# Create class for heart process
h = heart(mdata['sampling_rate'])
# Create an object for the example class
a = ex_proc()
# Set the function to run every x seconds
print "Set timer to process data repeatedly..."
pros_timer = RepeatedTimer(3,a.getData,h,signal)
# Set the mote to send every minute
time.sleep(0.5)
print "Set timer to send data repeatedly..."
# mote_timer = RepeatedTimer(15,mote.send_data,0,61)
# mote_timer = RepeatedTimer(15,mote.send_data,5,a.get_hr_int)
mote_timer = RepeatedTimer(60, send_packet_over_lora)
