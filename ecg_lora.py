import serial
import time
from bitstring import BitArray
import serial.tools.list_ports as serP
import platform


class lora:
    def __init__(self, com):
        # Set up serial port with LoRa mote
        self.ser = serial.Serial(
            port = com,
            baudrate = 9600,
            parity = serial.PARITY_ODD,
            stopbits = serial.STOPBITS_TWO,
            bytesize = serial.SEVENBITS)
        # Open the port
        self.ser.isOpen()
        # Initialize the message id
        self.msgID = 0

    def send(self, input):
        # send the character to the device
        self.ser.write(input + '\r\n')

    def receive(self):
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        # Receive the reply
        out = ''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)
        # return the reply
        return out

    def send_n_verify(self, input, output):
        self.send(input)
        out = self.receive()
        if out != output + '\r\n':
            print "Failed: " + out

    def start_up(self):
        self.send_n_verify("mac set appkey FC50E986B86514E4F03F1F2842C5C3D0","ok")
        self.send_n_verify("mac set appeui 70B3D57EF000396E","ok")
        self.send_n_verify("mac set adr off","ok")
        self.send_n_verify("mac save","ok")

    def connect(self):
        self.send_n_verify("mac join otaa","ok")

        while True:
            status = self.receive()
            if status != '':
                if status == 'accepted\r\n':
                    print "Join Server Status: " + status.rstrip()
                    break
                else:
                    print "Join Server Status: " + status.rstrip()
                    self.send_n_verify("mac join otaa","ok")

    def build_package(self,heartStatus,heartRate):
        curTime = time.gmtime()

        hour = curTime[3]
        hourB = [int(x) for x in '{:05b}'.format(hour)]
        hourB = hourB[:5]

        minute = curTime[4]
        minuteB = [int(x) for x in '{:06b}'.format(minute)]
        minuteB = minuteB[:6]

        second = curTime[5]

        heartStatusB = [int(x) for x in '{:05b}'.format(heartStatus)]
        heartStatusB = heartStatusB[:5]

        heartRateB = [int(x) for x in '{:08b}'.format(heartRate)]
        heartRateB = heartRateB[:8]

        msgIDB = [int(x) for x in '{:08b}'.format(self.msgID)]
        if(self.msgID >= 255):
            self.msgID = 0
        else:
            self.msgID += 1

        messageB = msgIDB + hourB + minuteB + heartStatusB + heartRateB
        messageB = BitArray(messageB)
        message = format(messageB.uint, 'x').zfill(8)

        return message

    def send_data(self, heartStatus, heartRate):
        # Build the message
        message = self.build_package(heartStatus,heartRate)
        # Connect to the server
        self.connect()
        # Send package
        print "Sending data: " + message
        self.send_n_verify("mac tx cnf 1 " + message,"ok")
        while True:
            status = self.receive()
            if status != '':
                if status == 'mac_tx_ok\r\n':
                    print "message status: " + status.rstrip()
                    break
                else:
                    print "message status: " + status.rstrip()
                    self.send_n_verify("mac tx cnf 1 " + message,"ok")


