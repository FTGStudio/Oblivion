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
import math
import threading

LORA_STATUS_NORMAL = 0
LORA_STATUS_SLOW = 1
LORA_STATUS_FAST = 2
LORA_STATUS_ABNORMAL = 4
LORA_STATUS_NOT_CONNECTED = 5

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
    global eventStatus

    if h.ready_to_send() != 0:
        temp = int(h.get_avg_heart_rate())
        if eventStatus == LORA_STATUS_NOT_CONNECTED:
            temp = 0
        print "Sending: ",
        print temp
        mote.send_data(eventStatus,temp)
    else:
        print "No data to send"

def event_status(heart_rate):

    global eventStatus
    global loraEventConfidence
    global lastSendEvent 

    if heart_rate is None or math.isnan(heart_rate):
        if eventStatus != LORA_STATUS_NOT_CONNECTED:
            loraEventConfidence = 0
        loraEventConfidence += 1
        print "Lora not connected number"
        print loraEventConfidence
        eventStatus = LORA_STATUS_NOT_CONNECTED
    elif heart_rate <= 40:
        if eventStatus != LORA_STATUS_SLOW:
            loraEventConfidence = 0
        loraEventConfidence += 1
        print "slow number"
        print loraEventConfidence
        eventStatus = LORA_STATUS_SLOW
    elif heart_rate >= 120:
        if eventStatus != LORA_STATUS_FAST:
            loraEventConfidence = 0
        loraEventConfidence += 1
        print "fast number"
        print loraEventConfidence
        eventStatus = LORA_STATUS_FAST
    else:
        if eventStatus != LORA_STATUS_NORMAL:
            loraEventConfidence = 0
        loraEventConfidence += 1
        eventStatus = LORA_STATUS_NORMAL

    if loraEventConfidence == 3 and lastSendEvent != eventStatus:
        # Get and clear the buffer
        temp = int(h.get_avg_heart_rate())
        if eventStatus == LORA_STATUS_NOT_CONNECTED:
            heart_rate = 0.0
        print "Sending Event: ",
        print int(heart_rate)
        t = threading.Thread(target=mote.send_data, args=(eventStatus, int(heart_rate,)))
        t.start()
        #mote.send_data(eventStatus, int(heart_rate))
        lastSendEvent = eventStatus

        mote_timer.stop()
        mote_timer.start()



eventStatus = LORA_STATUS_NORMAL
lastSendEvent = LORA_STATUS_NORMAL
loraEventConfidence = 0

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
                event_status(None)
                continue
            # Print the calculated heart rates
            # h_obj.print_heart_rate()
            # Print the calculated average heart rate
            temp = h.calc_avg_heart_rate()
            print "Avg Heartrate"
            print temp

            event_status(temp)

            h.add_heart_rate(temp)

