

import serial.tools.list_ports as ser
import platform

#The list of com ports, and their values is passed to the ports variable
ports = list(ser.comports())

#checks whether the module is running on Windows or Linux
if platform.system() == "Linux":
    for p in ports:
        if "CDC RS-232 Emulation Demo" in p[1]:
            print (p[0])

else:
    for p in ports:
        if "RN"
        
