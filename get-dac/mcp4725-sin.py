import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 3.2 
signal_frequency = 10 
sampling_frequency = 1000 

try:
    dac = mcp.MCP4725(5.11, verbose=False)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time

        sin_value = sg.get_sin_wave_amplitude(
            signal_frequency,
            current_time
        )

        voltage = amplitude * sin_value

        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)
except KeyboardInterrupt:
    print("\nПограмма завершилась")
finally:
    dac.deinit()
