Oblivion
=====
This repository houses the python digital signal processing application for the 2017 DornerWorks Senior project. This project models a LoRaWAN IOT device that monitors a human's heart rate and updates a web application with heart rate and important events. The DSP (`Raspberry Pi 3 B`_) uses python to read in 24-bit ADC (`Cyton Biosensing Board`_) value from electrodes, find the QRS wave within the ADC reading, calculate the average heart rate, and send the heart rate once per minute or when a rapid or slow heart hate event is detected.

File Overview
----------
Functionality is broken up into seperate files.

The main files for execution are listed below.

===================== ============
File                  Description
===================== ============
ecg_processing.py_    Main file for reading and sending heartrate
ecg_lora.py_          Connects and sends packets over LoRa
ecg_cyton.py_         Connects and reads from the Cyton Biosensing Board
heart.py_             Manages and calculates heartrate 
RepeatedTimer.py_     Starts a seperate thread on a timer for sending sycnronous LoRa messages
coms.py_              Auto finds the device for LoRa mote and Cyton Biosensing Board
===================== ============

Other files in the repo are described below.

===================== ============
File                  Description
===================== ============
mote_setup.py         Initially sets up LoRa motes with correct App and Mote IDs
dormire.service       The service file for systemd startup
reloadService.sh      Shell script to move and activate systemd
nicks_heart_1.csv     Recorded live data to be read for recorded demo
OpenBCI-RAW-2017.txt  Raw recorded live data from the OpenBCI GUI
requirements.txt      Required python packages used
===================== ============

.. _`Raspberry Pi 3 B`: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
.. _`Cyton Biosensing Board`: http://docs.openbci.com/Hardware/02-Cyton
.. _ecg_processing.py: docs/ecg_processing.rst
.. _ecg_lora.py: docs/ecg_lora.rst
.. _ecg_cyton.py: docs/ecg_cyton.rst
.. _heart.py: docs/heart.rst
.. _RepeatedTimer.py: docs/RepeatedTimer.rst
.. _coms.py: docs/coms.rst
