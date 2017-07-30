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

**Return:** 

    mask
        A numobservations-length boolean array.

``get_avg_heart_rate(self)``
-----

**Function Overview:** Returns the average heart rate for all data points in heartRate list. It also checks for outliers before calculating the average.

**Input Parameters:** None.

**Return:** None.

    avgHeartRate
        The average calculated heart rate for all points in the heartRate list, excluding outliers.
        
``getData(self, signal)``
-----

**Function Overview:** Gets the sliding window from the .CSV recorded data, processes it, and stores it. This function is only used for the CSV and not used for live data.

**Input Parameters:**

    signal
        The signal is the entire signal from the CSV file. The function will select a window from the signal and process it and set the heart rate.

**Return:** None.

``set_signal(self, signal)``
-----

**Function Overview:** Sets the signal to be processed. Note: this doesn't process the signal

**Input Parameters:**

    signal
        The list of raw data that is to be processed for heart rate.

**Return:** None.

``print_signal(self)``
-----

**Function Overview:** Used for debugging. Prints the set signal list in self.sig.

**Input Parameters:** None.

**Return:** None.

``print_heart_rate(self)``
-----

**Function Overview:** Used for debugging. Prints the array of heart rates calculated in the process function.

**Input Parameters:** None.

**Return:** None.

``process(self)``
-----

**Function Overview:** Processes the raw signal set in the self.sig (see set_signal function). This stores a list of calculated heart rates in the self.result attribute. A heart rate is calculated by finding the QRS portion of the ECG signal. The signal is compared with the last two QRS signals and an average heart rate is calculated based on the timing of the three QRS signals.

**Input Parameters:** None.

**Return:** None.

``process_show(self)``
-----

**Function Overview:** Similar to the process function except the result is shown in a graph which will show in the screen.

**Input Parameters:** None.

**Return:** None.

``calc_avg_heart_rate(self)``
-----

**Function Overview:** Calculates the average heart rate for all the heart rates calculated in the self.result list (see process function). The average is saved in the self.avg_hr attribute and also returned.

**Input Parameters:** None.

**Return:**

    avg_hr
        The average heart rate calculated from the heart rates saved in the self.result attribute.
