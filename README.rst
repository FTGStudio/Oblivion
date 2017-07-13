Oblivion
=====
This repository houses the python digital signal processing application for the 2017 DornerWorks Senior project. This project models a LoRaWAN IOT device that monitors a human's heart rate and updates a web application with heart rate and important events. The DSP uses python to read in 24-bit ADC value from electrodes, find the QRS wave within the ADC reading, calculate the average heart rate, and send the heart rate once per minute or when a rapid or slow heart hate event is detected.
