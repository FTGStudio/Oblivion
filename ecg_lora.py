import serial
import time

class lora:
    def __init__(self):
        # Set up serial port with LoRa mote
        self.ser = serial.Serial(
            port = 'COM7',
            baudrate = 9600,
            parity = serial.PARITY_ODD,
            stopbits = serial.STOPBITS_TWO,
            bytesize = serial.SEVENBITS)
        # Open the port
        self.ser.isOpen()

    def send(self, input):
        # send the character to the device
        self.ser.write(input + '\r\n')
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        # Read in the reply
        out = ''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)
        # return the reply
        return out

    def send_n_verify(self, input, output):
        out = self.send(input)
        if out == output + '\r\n':
            print "good"
        else:
            print "bad"

n = lora()
n.send_n_verify("mac set appkey 989BC0559766877D7246D4CF96050DB5","ok")
