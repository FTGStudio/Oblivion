``RepeatedTimer.py``
-----

**File Overview:** Runs threads at a set interval for sending LoRa messages or reading the recorded data file.

``__init__()``
-----

**Function Overview:** Init function sets the function to be run, passed arguments, interval to execute and starts the timer to execute the function.

**Input Parameters**:

    interval
        Number of seconds to wait before the function is executed

    function
        The specified function to be run

    \*args
        The list of arguments for the function

    \**kwargs
        Arguments for the function that have not been defined

**Return:** None.
    
-----

Head on back_!

.. _back: ../README.rst
