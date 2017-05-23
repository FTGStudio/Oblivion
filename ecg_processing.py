from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer
from ecg_lora import lora
from ecg_cyton import cyton

class ex_proc:
    def __init__(self):
        self.heartRate = []

    def add_heart_rate(self, heart_rate):
        self.heartRate.append(heart_rate)

    def get_avg_heart_rate(self):
        temp = 0.0;
        if len(self.heartRate) is not 0:
            temp = sum(self.heartRate) / float(len(self.heartRate))
            self.heartRate = []
        return temp

    def test_print(self, data):
        print "LORA SEND: " + data

# Set up LoRa mote
#mote = lora()
#print "Setting up LoRa mote..."
#mote.start_up()
#print "Connecting to LoRa gateway..."
#mote.connect()

# Create class for heart process
h = heart(250)

# Create an object for the example class
a = ex_proc()

# Create class for cyton board
c = cyton()

# Set the mote to send every minute
print "Set timer to send data repeatedly..."
#mote_timer = RepeatedTimer(60,mote.send_data,a.get_avg_heart_rate())
mote_timer = RepeatedTimer(60,a.test_print,a.get_avg_heart_rate())

c.start_stream()
while True:
    c.read_line()

    if c.is_window_full():
        # Set the signal to be processed
        h.set_signal(c.get_signal())
        # Process signal and show the result in the GUI
        h.process()
        # Print the calculated heart rates
        # h_obj.print_heart_rate()
        # Print the calculated average heart rate
        temp = h.calc_avg_heart_rate()
        print "Avg Heartrate"
        print temp
        a.add_heart_rate(temp)
