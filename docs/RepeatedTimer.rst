``RepeatedTimer.py``
-----

**File Overview:** Runs threads at a set interval for sending LoRa messages or reading the recorded data file.

``__init__(self, interval, function, *args, **kwargs)``
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

``_run(self)``
-----

**Function Overview:** A function for internal use that starts the function thread and starts the timer for the next thread to run.

**Input Parameters:** None.

**Return:** None.

``start(self)``
-----

**Function Overview:** The start function begins the thread and runs the specified function every time the timer expires. This function is automatically called when the timer is created, but it can be used to restart the thread if the stop function is called.

**Input Parameters:** None.

**Return:** None.

``stop(self)``
-----

**Function Overview:** The stop function halts the thread by disabling the timer that recalls the function when it expires. This will allow the current function to finish but stops the timer from calling the function again.

**Input Parameters:** None.

**Return:** None.

-----

Head on back_!

.. _back: ../README.rst
