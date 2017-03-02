#!/usr/bin/env python2.7
import argparse  # new in Python2.7
import os
import time
import string
import atexit
import threading
import logging
import sys

import open_bci_v3 as bci

from yapsy.PluginManager import PluginManager

manager = PluginManager()
manager.setPluginPlaces(["plugins"])
manager.collectPlugins()

print ("\n-------INSTANTIATING BOARD-------")
board = bci.OpenBCIBoard(port='/dev/ttyUSB0',
                             scaled_output=True)

print (board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz.")

callback_list = []
plug_name = "print"
plug = manager.getPluginByName(plug_name)
if plug == None:
    # eg: if an import fail inside a plugin, yapsy skip it
    print ("Error: [", plug_name, "] not found or could not be loaded. Check name and requirements.")
else:
    print ("\nActivating plugin...")
    if not plug.plugin_object.pre_activate([], sample_rate=board.getSampleRate(), eeg_channels=board.getNbEEGChannels(), aux_channels=board.getNbAUXChannels()):
        print ("Error while activating ", plug_name, " check output for more info.")
    else:
        print ("Plugin", plug_name, " added to the list")
        callback_list.append(plug.plugin_object)

fun = callback_list
board.start_streaming(callback=fun)
