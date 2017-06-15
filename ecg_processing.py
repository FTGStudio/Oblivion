import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer
from ecg_lora import lora
from ecg_cyton import cyton
import coms
import time
import signal




class ex_proc:

    def __init__(self):
        self.heartRate = []
        self.i = 0

    def add_heart_rate(self, heart_rate):
        self.heartRate.append(heart_rate)

    def get_avg_heart_rate(self):
        temp = 0.0
        if len(self.heartRate) is not 0:
            temp = sum(self.heartRate) / float(len(self.heartRate))
            self.heartRate = []
        return temp

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


# Setup handler for exiting the script if "CTRL+C" is pressed
def handler(signum, frame):
    print 'Signal handler caught ', signum
    cytonBrd.stop_stream()
    mote_timer.stop()
    exit()

def setupLoRaMote():
    try:
        # Get LoRa COM port
        print "Get LoRa COM Port...",
        lora_com = coms.get_com()
        print lora_com
        # Set up LoRa object
        mote = lora(lora_com)
        # Join server
        mote.connect()
        # Set flag for the LoRa mote being present
        return mote
    except:
        print "Error - make sure the LoRa mote is plugged in"
        return 0

def setupCytonDongle():
    try:
        print "Get Cyton Biosensing COM Port...",
        # Get cyton COM port
        cyton_com = coms.get_cyton()
        print cyton_com
        # Create class for cyton board
        cytonBoard = cyton(cyton_com)
        # Set flag for the cyton dongle being present
        return cytonBoard
    except:
        print "Error - make sure the Cyton RF dongle is plugged in"
        return 0

def send_packet_over_lora(mote):
    temp = int(a.get_avg_heart_rate())
    print "Sending: ",
    print temp
    mote.send_data(5,temp)


if __name__ == "__main__":
    loraMotePresent = 0
    cytonPresent = 0

    # Set up signal handler for clean up
    signal.signal(signal.SIGINT, handler)

    # Create class for heart process
    h = heart(250)

    # Create an object for the example class
    a = ex_proc()

    # Set up LoRa mote
    mote = setupLoRaMote()

    # Setup Cyton Biosensing board
    cytonBrd = setupCytonDongle()

    # Sleep to allow mote to warm up
    time.sleep(0.5)

    if mote != 0:
        print "Set timer to send data repeatedly...",
        mote_timer = RepeatedTimer(15, send_packet_over_lora, mote)
        print "Done"

    if cytonBrd != 0:
        cytonBrd.start_stream()
        while True:
            cytonBrd.read_line()

            if cytonBrd.is_window_full():
                # Set the signal to be processed
                h.set_signal(cytonBrd.get_signal())
                # Process signal and show the result in the GUI
                h.process()
                # Print the calculated heart rates
                # h_obj.print_heart_rate()
                # Print the calculated average heart rate
                temp = h.calc_avg_heart_rate()
                print "Avg Heartrate"
                print temp
                a.add_heart_rate(temp)
    else:
        # Import the data from a csv file
        print "Importing data from CSV..."
        signal, mdata = storage.load_txt('nicks_heart_1.csv')
        # Create class for heart process
        h = heart(mdata['sampling_rate'])
        # Create an object for the example class
        a = ex_proc()
        # Set the function to run every x seconds
        print "Set timer to process data repeatedly..."
        pros_timer = RepeatedTimer(3, a.getData, h, signal)
        # Set the mote to send every minute
        time.sleep(0.5)
        print "Set timer to send data repeatedly..."
        # mote_timer = RepeatedTimer(15,mote.send_data,0,61)
        # mote_timer = RepeatedTimer(15,mote.send_data,5,a.get_hr_int)
        # mote_timer = RepeatedTimer(60, send_packet_over_lora)