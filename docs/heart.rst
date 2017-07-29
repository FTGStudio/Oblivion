``heart.py``
-----

**File Overview:** Creates a heart class to process raw data and output an average heart rate.

``__init__(self, sampleRate)``
-----

**Function Overview:** Init function sets the sample rate that the raw data is being obtained. This is critical to calculating an accurate heart rate.

**Input Parameters:**

    sampleRate
        An integer representing the rate at which the raw data is sampled in Hz.

**Return:** None.

``add_heart_rate(self, heart_rate)``
-----

**Function Overview:** Appends a single calculated heart rate to the list of calculated heart rates.

**Input Parameters:**

    heart_rate
        The calculated heart rate in beats per minute to append to the heartRate list.

**Return:** None.


``ready_to_send(self)``
-----

**Function Overview:** Returns the length of the heartRate list so that the program can determine if there is enough data to send a message of average heart rates.

**Input Parameters:** None.

**Return:**

    heartRateLength
        The total size of the heartRate list. This is used to determine if there is enough data to send an average heart rate.
        
``__is_outlier(self, points, thresh=3.5)``
-----

**Function Overview:** Caclulates to see if the heart rate is an outlier compared to previous heart rates. This is used to elminite false QRS detections due to muscle artifacts and noise.

**Input Parameters:**

    points
        An numobservations by numdimensions array of observations

    thresh
        The modified z-score to use as a threshold. Observations with a modified z-score (based on the median absolute deviation) greater than this value will be classified as outliers.

**Return:** None.

    mask
        A numobservations-length boolean array.
