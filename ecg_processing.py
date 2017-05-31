import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer
from ecg_lora import lora
from ecg_cyton import cyton
import coms
import time

def send_packet_over_lora():
    temp = int(a.get_avg_heart_rate())
    print "Sending: "
    print temp
    mote.send_data(5,temp)

class ex_proc:

    def __init__(self):
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
# Get LoRa COM port
print "Get LoRa COM Port...",
lora_com = coms.get_com()
print lora_com
# Set up LoRa object
mote = lora(lora_com)
# Join server
mote.connect()

# Create class for heart process
h = heart(250)

# Create an object for the example class
a = ex_proc()

# Get cyton COM port
cyton_com = coms.get_cyton()
# Create class for cyton board
c = cyton(cyton_com)

# Set the mote to send every minute
time.sleep(0.5)
print "Set timer to send data repeatedly..."
mote_timer = RepeatedTimer(15, send_packet_over_lora)

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
