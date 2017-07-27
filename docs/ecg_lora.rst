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
    
-----

Head on back_!

.. _back: ../README.rst
