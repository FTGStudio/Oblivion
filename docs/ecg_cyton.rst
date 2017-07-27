``ecg_cyton.py``
-----

**File Overview:** Manages connecting, reseting, and reading from the Cyton Biosensing Board.

``__init__()``
-----

**Function Overview:** Init function establishes connection with the serial port and initializes the channel arrays.

**Input Parameters**:

    com
        Device name of the Cyton Biosensing Board Dongle

**Return:** None.
    
``start_stream()``
-----

**Function Overview:** Stops and resets the Cyton Board and wait until the board is ready to start sending data.

**Input Parameters**:

    None

**Return:** Returns 1 on success and 0 on failure

``stop_stream()``
-----

**Function Overview:** Stops the stream. Used in interupt handler in main.

**Input Parameters**:

    None

**Return:** None

``read_line()``
-----

**Function Overview:** Reads one packets worth of data and unpacks the desired channels of that packet into the channel arrays.

**Input Parameters**:

    None

**Return:** None

``print_line()``
-----

**Function Overview:** Mainly debugging function to print the last element of all of the channel arrays.

**Input Parameters**:

    None

**Return:** None

``get_signal()``
-----

**Function Overview:** Returns the first channel array. Shifts the array to have the last two seconds remain in it.

**Input Parameters**:

    None

**Return:** The numpy array of the last 5 seconds of data from channel one.

``is_window_full()``
-----

**Function Overview:** Returns if the array is full of 5 seconds of data.

**Input Parameters**:

    None

**Return:** Returns 1 when the channel array holds over 5 seconds of data, else 0.

-----

Head on back_!

.. _back: ../README.rst
