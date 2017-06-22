
import platform
import serial.tools.list_ports as ser



#This function just returns the comport of the device in question
def get_com():
    #The list of com ports, and their values is passed to the ports variable
    ports = list(ser.comports())
    port = 0

    #checks whether the module is running on Windows or Linux
    if platform.system() == "Linux":
        for p in ports:
            if "CDC RS-232 Emulation Demo" in p[1]:
                port = p[0]

    # If it's not Linux it looks for "USB Serial Port", which is what the
    # RN2903 shows up as in Windows. But this won't work,
    # cuz it's too generic. need to find a different solution
    else:
        for p in ports:
            if "USB Serial Port" in p[1]:
                port = p[0]

    return port

#This function just returns the comport of the device in question
def get_cyton():
    #The list of com ports, and their values is passed to the ports variable
    ports = list(ser.comports())
    port = 0

    #checks whether the module is running on Windows or Linux
    if platform.system() == "Linux":
        for p in ports:
            if "FT231X USB UART" in p[1]:
                port = p[0]

    # If it's not Linux it looks for "USB Serial Port", which is what the
    # RN2903 shows up as in Windows. But this won't work,
    # cuz it's too generic. need to find a different solution
    else:
        for p in ports:
            if "USB Serial Port" in p[1]:
                port = p[0]

    return port

        
