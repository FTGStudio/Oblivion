import serial
import time
import struct

class cyton:
    def __init__(self):
        # Set up serial port with Cyton board
        self.ser = serial.Serial(
            port = '/dev/ttyUSB0',
            baudrate = 115200,
            parity = serial.PARITY_ODD,
            stopbits = serial.STOPBITS_TWO,
            bytesize = serial.SEVENBITS)
        # Open the port
        self.ser.isOpen()

    def start_stream(self):
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
        else:
            print 'cyton reset error'


    def read_line(self):
        out = self.ser.read(33)

        startByte = struct.unpack('<I', out[0] + '\0\0\0')[0]
        seqNum = struct.unpack('<I', out[1] + '\0\0\0' )[0]
        chan1 = struct.unpack('<i', out[2:5] + '\0')[0]
        chan2 = struct.unpack('<i', out[5:8] + '\0')[0]
        chan3 = struct.unpack('<i', out[8:11] + '\0')[0]
        print '{} {} {} {} {}'.format(startByte, seqNum, chan1, chan2, chan3)



c = cyton()
c.start_stream()
while True:
    c.read_line()
