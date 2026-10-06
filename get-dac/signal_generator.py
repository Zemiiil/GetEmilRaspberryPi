import numpy as np
import time


def get_sin_wave_amplitude(freq, time_value):
    value = np.sin(2 * np.pi * freq * time_value)
    value = value + 1
    value = value / 2
    return value

def wait_for_sampling_period(sampling_frequency):
    period = 1 / sampling_frequency
    time.sleep(period)
