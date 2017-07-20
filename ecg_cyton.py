import serial
import time
import struct
import numpy as np
from coms import get_cyton

class cyton:
    def __init__(self, com):
        # Set up serial port with Cyton board
        self.ser = serial.Serial(
            port = com,
            baudrate = 115200,
            parity = serial.PARITY_ODD,
            stopbits = serial.STOPBITS_TWO,
            bytesize = serial.SEVENBITS)
        # Open the port
        self.ser.isOpen()
        self.winCh1 = np.array([])
        self.winCh2 = np.array([])
        self.winCh3 = np.array([])

    def start_stream(self):
        # sending a 's' stops the cyton
        self.ser.write('s')

        # sleep waiting for data to stop coming to come in
        time.sleep(1)
    
        # clear possible extra data
        self.ser.reset_input_buffer()

        # sending a 'v' resets the cyton
        self.ser.write('v')
        print 'reset cyton'

        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(2)
        # Read in the reply
        out = ''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)

        # cyton returns '$$$' when done initializing
        if "$$$" in out:
            # sending a 'b' starts the cyton data stream
            self.ser.write('b')
            print 'starting cyton stream'
            status = 1
        else:
            print 'cyton reset error'
            status = 0

        return status

    def stop_stream(self):
        #sending a 's' to stop stream
        self.ser.write('s')
        print 'stop cyton'

    def read_line(self):
        out = self.ser.read(33)

        startByte = struct.unpack('<I', out[0] + '\0\0\0')[0]
        seqNum = struct.unpack('<I', out[1] + '\0\0\0' )[0]

        self.winCh1 = np.append(self.winCh1, struct.unpack('>i', ('\0' if out[2] < '\x80' else '\xff') + out[2:5])[0])
        self.winCh2 = np.append(self.winCh2, struct.unpack('>i', ('\0' if out[5] < '\x80' else '\xff') + out[5:8])[0])
        self.winCh3 = np.append(self.winCh3, struct.unpack('>i', ('\0' if out[8] < '\x80' else '\xff') + out[8:11])[0])

    def print_line(self):
        print str(self.winCh1[-1]) + " " + str(self.winCh2[-1]) + " " + str(self.winCh3[-1])
        

    def get_signal(self):
        temp = self.winCh1
        #leave last 2 seconds in window
        self.winCh1 = self.winCh1[-500:]
        self.winCh2 = self.winCh2[-500:]
        self.winCh3 = self.winCh3[-500:]

        return temp

    def is_window_full(self):
        return len(self.winCh1) >= 1250;

if __name__ == "__main__":
    com = get_cyton()
    c = cyton(com)
    c.start_stream()
    while True:
        c.read_line()
        c.print_line()
