import serial
import time

class lora:
    def __init__(self):
        # Set up serial port with LoRa mote
        self.ser = serial.Serial(
            port = 'COM9',
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
            print "bad: " + out

    def start_up(self):
        self.send_n_verify("mac set appkey 989BC0559766877D7246D4CF96050DB5","ok")
        self.send_n_verify("mac set appeui 70B3D57EF000396E","ok")
        self.send_n_verify("mac set adr off","ok")
        self.send_n_verify("mac save","ok")

    def connect(self):
        self.send_n_verify("mac join otaa","ok")

    def send_data(self, data):
        print "Sending data! " + data
        self.send_n_verify("mac tx cnf 1 " + data,"ok")

# n = lora()
# n.start_up()
# n.send_data("123456780")
