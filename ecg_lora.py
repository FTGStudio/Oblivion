import serial
import time
from bitstring import BitArray
import serial.tools.list_ports as serP
import platform

# Todo
#   * Look for if it's already connected to the server
#   * Clear buffer before reading


class lora:
    def __init__(self, com):
        # Set up serial port with LoRa mote
        self.ser = serial.Serial(
            port = com,
            baudrate = 9600,
            parity = serial.PARITY_ODD,
            stopbits = serial.STOPBITS_TWO,
            bytesize = serial.SEVENBITS,
            timeout = 1)
        # Open the port
        self.ser.isOpen()
        # Initialize the message id
        self.msgID = 0
        time.sleep(1)
        self.ser.flush()


    def send(self, input):
        # Flush the output buffer
        self.ser.reset_output_buffer()
        # send the character to the device
        self.ser.write(input + '\r\n')


    def receive(self):
        # Flush the input buffer
        self.ser.reset_input_buffer()
        # Wait until the mote starts responding
        while self.ser.inWaiting() == 0:
            pass
        # Wait for the rest of the message to come in
        time.sleep(0.05)
        # Clear the out string
        out = ''
        # Read in the message
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)
        # return the message
        return out.rstrip()


    def send_n_verify(self, input, output):
        self.send(input)
        out = self.receive()
        if out != output + '\r\n':
            print "Failed: " + out


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


    def start_up(self):
        print "--------------------------------------"
        print "LoRa Mote Setup:"
        status = 1

        print "   LoRa: Setting APPKEY...",
        self.send("mac set appkey FC50E986B86514E4F03F1F2842C5C3D0")
        reply1 = self.receive()
        if reply1 != "ok":
            status = 0
        print reply1

        print "   LoRa: Setting APPEUI...",
        self.send("mac set appeui 70B3D57EF000396E")
        reply2 = self.receive()
        if reply2 != "ok":
            status = 0
        print reply2

        print "   LoRa: Setting ADR OFF...",
        self.send("mac set adr off")
        reply3 = self.receive()
        if reply3 != "ok":
            status = 0
        print reply3

        print "   LoRa: MAC SAVE...",
        self.send("mac save")
        reply4 = self.receive()
        if reply4 != "ok":
            status = 0
        print reply4

        if status == 1:
            print "LoRa Setup Successful"
        else:
            print "LoRa Mote Setup Failed"

        print "--------------------------------------"

        return status

    def connect(self):
        print "--------------------------------------"
        print "LoRa Connect to Server:"
        status = 1

        print "   LoRa: Send Join Otaa Command...",
        self.send("mac join otaa")
        reply = self.receive()
        if reply != "ok":
            status = 0
        print reply

        print "   LoRa: Join Otaa...",
        reply = self.receive()
        if reply != "accepted":
            status = 0
        print reply

        if status == 1:
            print "LoRa Mote Join Successful"
        else:
            print "LoRa Mote Join Failed"

        print "--------------------------------------"

        return status


    def send_data(self, heartStatus, heartRate):
        print "************************************************"
        print "Sending Heart Message To Server:"
        status = 1
        try_connect = 0

        # Build the message
        message = self.build_package(heartStatus,heartRate)

        # Send package
        print "   LoRa: Sending Transmit Message " + message + "...",
        self.send("mac tx cnf 1 " + message)
        reply = self.receive()
        print reply
        if reply != "ok":
            status = 0
            if reply == "not_joined":
                try_connect = 1
        else:
            # Receive confirmation
            print "   LoRa: Transmission Status...",
            reply = self.receive()
            if reply != "mac_tx_ok":
                status = 0
            print reply

        if status == 1:
            print "LoRa Mote Transmission Successful"
        else:
            print "LoRa Mote Transmission Failed"

        print "************************************************"

        if try_connect == 1:
            self.connect()

        return status
