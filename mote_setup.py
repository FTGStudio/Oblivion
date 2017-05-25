import numpy as np
from matplotlib import pyplot as pl
from biosppy import storage
from heart import heart
from RepeatedTimer import RepeatedTimer
from ecg_lora import lora
from coms import get_com
import time

# Set up LoRa mote
# Get LoRa COM port
print "Get LoRa COM Port...",
lora_com = get_com()
print lora_com
# Set up LoRa object
mote = lora(lora_com)
# Set MAC setttings
mote.start_up()
