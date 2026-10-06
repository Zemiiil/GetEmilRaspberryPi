import time


def get_triangle_wave_amplitude(freq, time_value):
    period = 1 / freq
    time_value = time_value % period

    if time_value <= period / 2:
        value = 1 - 2 * freq * time_value
    else:
        value = 2 * freq * time_value - 1

    return value

def wait_for_sampling_period(sampling_frequency):
    period = 1 / sampling_frequency
    time.sleep(period)
