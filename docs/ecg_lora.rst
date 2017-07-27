``ecg_lora.py``
-----

**File Overview:** Controls the interface for the LoRa mote. Commands are sent and received from the mote using serial communication. This class also compiles a the data packet to be sent based on the current information.

``__init__(self, com)``
-----

**Function Overview:** Init function sets up the serial communication port to communicate with the LoRa mote. Once the LoRa mote serial port is opened, commands and data can be sent and received.

**Input Parameters**:

    com
        The name of the serial port to connect to. For example, "/dev/ttyS1" (linux) or "COM4" (windows).

**Return:** None.

``send(self, input)``
-----

**Function Overview:** Send function writes the input string to the serial buffer and sends it to the LoRa mote.

**Input Parameters:**

    input
        The string to send over serial communication with LoRa. This should be a LoRa serial command, such as "mac join otaa".

**Return:** None.

``receive(self)``
-----

**Function Overview:** Receives a string from the LoRa mote via serial port. Once the string starts receiving the system waits 50ms more to make sure the entire string is done sending and returns the resulting string.

**Input Parameters:** None.

**Return:**

    out
        The string that is received on the serial port from the LoRa mote
        
``send_n_verify(self, input, output)``
-----

**Function Overview:** Executes the send function followed by the receive function. If the received string isn't the same as the output variable, then a message is printed to the terminal that the command failed.

**Input Parameters:**

    input
        The string to send to the LoRa mote
        
    output
        The expected string to be received after sending the input to the LoRa mote.

**Return:** None.

``build_package(self, heartStatus, heartRate)``
-----

**Function Overview:** Takes in the heart status number and the heart rate to send to the server. The information is taken and compiled into one 32-bit package that can be transmitted over LoRa.

**Input Parameters:**

    heartStatus
        A number ranging from 0 to 15 representing the current status of the heart (normal, fast, slow, disconnected). These are defined in ecg_processing.py.
        
    heartRate
        A number from 0 to 255 representing the heart rate to send to the server in beats per minute (BPM).

**Return:**

    message
        The 32-bit message that can be used to send over LoRa.
        
``start_up(self)``
-----

**Function Overview:** Sets up the LoRa mote with internal settings. It starts by indentifying the device and assigning the appropriate app key. Then is sets the app eui. These settings are saved to the mote and a status bit is returned to verify that the startup succeeded.

**Input Parameters:** None.

**Return:**

    status
        1 - Successful setup
        0 - Failed setup
    
``connect(self)``
-----

**Function Overview:** Connects the LoRa mote with the gateway. The LoRa mote attempts to join the gateway and returns the status if it was successful or not.

**Input Parameters:** None.

**Return:**

    status
        1 - Successful connection
        0 - Failed setup
        
``send_data(self, heartStatus, heartRate)``
-----

**Function Overview:** The send_data function takes the heart status and the heart rate, compiles the data package to send, and attempts to send the package to the LoRa server. If the mote isn't connected, the function attempts to connect to the mote again. 

**Input Parameters:** 

    heartStatus
        A number ranging from 0 to 15 representing the current status of the heart (normal, fast, slow, disconnected). These are defined in ecg_processing.py.
        
    heartRate
        A number from 0 to 255 representing the heart rate to send to the server in beats per minute (BPM).

**Return:**

    status
        1 - Successful connection
        0 - Failed setup
        
-----

Head on back_!

.. _back: ../README.rst
