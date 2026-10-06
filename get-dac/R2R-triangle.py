import R2R_dac as r2r
import triangle_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
gpio_bits = [16, 20, 21, 25, 26, 17, 27, 22]

try:
    dac = r2r.R2R_DAC(gpio_bits, 3.3, False)

    start_time = time.time()

    while True:
        current_time = time.time() - start_time

        sin_value = sg.get_triangle_wave_amplitude(
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
