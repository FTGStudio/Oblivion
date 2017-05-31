import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer
from ecg_lora import lora
<<<<<<< HEAD
from ecg_cyton import cyton
=======
from coms import get_com
import time

def send_packet_over_lora():
    mote.send_data(5,a.get_hr_int())
>>>>>>> master

class ex_proc:

    def __init__(self):
<<<<<<< HEAD
        self.heartRate = []

    def add_heart_rate(self, heart_rate):
        self.heartRate.append(heart_rate)

    def get_avg_heart_rate(self):
        temp = 0.0;
        if len(self.heartRate) is not 0:
            temp = sum(self.heartRate) / float(len(self.heartRate))
            self.heartRate = []
        return temp

    def test_print(self, data):
        print "LORA SEND: " + data

# Set up LoRa mote
#mote = lora()
#print "Setting up LoRa mote..."
#mote.start_up()
#print "Connecting to LoRa gateway..."
#mote.connect()

=======
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
>>>>>>> master
# Create class for heart process
h = heart(250)

# Create an object for the example class
a = ex_proc()

# Create class for cyton board
c = cyton()

# Set the mote to send every minute
time.sleep(0.5)
print "Set timer to send data repeatedly..."
<<<<<<< HEAD
#mote_timer = RepeatedTimer(60,mote.send_data,a.get_avg_heart_rate())
mote_timer = RepeatedTimer(60,a.test_print,a.get_avg_heart_rate())

c.start_stream()
while True:
    c.read_line()

    if c.is_window_full():
        # Set the signal to be processed
        h.set_signal(c.get_signal())
        # Process signal and show the result in the GUI
        h.process()
        # Print the calculated heart rates
        # h_obj.print_heart_rate()
        # Print the calculated average heart rate
        temp = h.calc_avg_heart_rate()
        print "Avg Heartrate"
        print temp
        a.add_heart_rate(temp)
=======
# mote_timer = RepeatedTimer(15,mote.send_data,0,61)
# mote_timer = RepeatedTimer(15,mote.send_data,5,a.get_hr_int)
mote_timer = RepeatedTimer(60, send_packet_over_lora)
>>>>>>> master
