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
import os


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
    if h.ready_to_send() != 0:
        temp = int(h.get_avg_heart_rate())
        print "Sending: ",
        print temp
        mote.send_data(5,temp)
    else:
        print "No data to send"


if __name__ == "__main__":
    # Set up signal handler for clean up
    signal.signal(signal.SIGINT, handler)

    # Create class for heart process
    h = heart(250)

    # Create an object for the example class
    # a = ex_proc()

    # Set up LoRa mote
    loop = 0;
    while True:
        mote = setupLoRaMote()
        loop += 1
        if mote != 0:
            break
        if loop > 10:
            os.system('reboot now')

    # Setup Cyton Biosensing board
    loop = 0;
    while True:
        cytonBrd = setupCytonDongle()
        loop += 1
        if cytonBrd != 0:
            break
        if loop > 10:
            os.system('reboot now')

    # Sleep to allow mote to warm up
    time.sleep(0.5)


    print "Set timer to send data repeatedly...",
    mote_timer = RepeatedTimer(60, send_packet_over_lora, mote)
    print "Done"

    loop = 0;
    while True:
        loop += 1
        isConnected = cytonBrd.start_stream()
        if isConnected == 1:
            break
        if loop > 10:
            os.system('reboot now')


    while True:
        cytonBrd.read_line()

        if cytonBrd.is_window_full():
            # Set the signal to be processed
            h.set_signal(cytonBrd.get_signal())

            try:
                # Process signal and show the result in the GUI
                h.process()
            except:
                print "Processing error. No heartrate"
                continue
            # Print the calculated heart rates
            # h_obj.print_heart_rate()
            # Print the calculated average heart rate
            temp = h.calc_avg_heart_rate()
            print "Avg Heartrate"
            print temp
            h.add_heart_rate(temp)
