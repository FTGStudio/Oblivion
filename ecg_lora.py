import serial
import time
from bitstring import BitArray

# Todo
#   * Look for if it's already connected to the server
#   * Clear buffer before reading

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
        # Attemp to join gateway
        self.send_n_verify("mac join otaa","ok")

        while True:
            status = self.receive().rstrip()
            if status != '':
                print "Join Server Status: " + status
                break


    def build_package(self,heartStatus,heartRate):
        # Get the current time
        curTime = time.gmtime()
        # Extract the hour and get the binary array
        hour = curTime[3]
        hourB = [int(x) for x in '{:05b}'.format(hour)]
        hourB = hourB[:5]
        # Extract the minute and get the binary array
        minute = curTime[4]
        minuteB = [int(x) for x in '{:06b}'.format(minute)]
        minuteB = minuteB[:6]
        # Extract the second
        second = curTime[5]
        # Get the binary array for the heart status
        heartStatusB = [int(x) for x in '{:05b}'.format(heartStatus)]
        heartStatusB = heartStatusB[:5]
        # Get the binary array for the heart rate
        heartRateB = [int(x) for x in '{:08b}'.format(heartRate)]
        heartRateB = heartRateB[:8]
        # Get the binary array for the message ID number
        msgIDB = [int(x) for x in '{:08b}'.format(self.msgID)]
        # Calculate the message ID number for next time
        if(self.msgID >= 255):
            self.msgID = 0
        else:
            self.msgID += 1
        # Combine into one array
        messageB = msgIDB + hourB + minuteB + heartStatusB + heartRateB
        # Convert to number from array of bits
        messageB = BitArray(messageB)
        # Convert to hex and pad with zeros
        message = format(messageB.uint, 'x').zfill(8)
        # Return the 32-bit hex string
        return message


    def send_data(self, heartStatus, heartRate):
        # Build the message
        message = self.build_package(heartStatus,heartRate)
        # Send package
        print "Sending data: " + message
        self.send_n_verify("mac tx cnf 1 " + message,"ok")
        while True:
            status = self.receive().rstrip()
            if status != '':
                print "message status: " + status
                if status == 'mac_tx_ok':
                    break
                else if status == 'not_joined':
                    # Try to connect to the gateway
                    self.connect()
                    # Then resend the message
                    self.send_n_verify("mac tx cnf 1 " + message,"ok")
                else:
                    # Retry to send the message
                    self.send_n_verify("mac tx cnf 1 " + message,"ok")
