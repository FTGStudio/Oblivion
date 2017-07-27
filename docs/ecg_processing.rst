``RepeatedTimer.py``
-----

**File Overview:** This is the main loop of the process. Heart rate is collected, processed and sent over LoRa.

-Connection is made with the LoRa Remote and Cyton Biosensing Board. If connection fails more than 10 times the system will reboot and try again.
-The repeat timer is set to send a LoRa message every 60 seconds.
-The Cyton stream starts. If the ``start_stream()`` function fails 10 times the system will reboot and try again.
-In the main loop, the cyton is continually polled for a new transmition.
-If the window is full the data gets processed and stored.
-Events are checked with each new processing and send asynchronously if needed.

``handler()``
-----

**Function Overview:** Signal handler for exiting gracefully.

**Input Parameters**:

    signum
        Signal number of signal

    frame
        Auto generated frame stack info

**Return:** None.
    
``setupLoRaMote()``
-----

**Function Overview:** Connects to the LoRa mote. Finds device name, create object, and connect.

**Input Parameters**:

    None.

**Return:** Returns mote object on success and 0 on failure.
    
``setupCytonDongle()``
-----

**Function Overview:** Connects to the Cyton Biosensing Board. Finds device name, create object and connect.

**Input Parameters**:

    None.

**Return:** Returns cytonboard object on success and 0 on failure.
    
``send_packet_over_lora()``
-----

**Function Overview:** Checks that it is ready to send and then send the average heart rate. This function is called by the RepeatTimer for sending LoRa messages every minute.

**Input Parameters**:

    mote
        The LoRa remote object to send the average heart rate to.

**Return:** None.
    
``event_status()``
-----

**Function Overview:** Keeps track of the current message status and sends the asynchronous messages. It takes 3 of the same types of statuses in a row to change the current status and send an event message. When sending an event the buffer of heart rates are cleared and the Repeat timer is reset.

**Input Parameters**:

    heart_rate
        The last processed heart rate

**Return:** None.
    
-----

Head on back_!

.. _back: ../README.rst
