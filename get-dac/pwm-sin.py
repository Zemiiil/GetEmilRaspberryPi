import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.2 
signal_frequency = 10 
sampling_frequency = 1000 
gpio_pin = 12 
pwm_frequency = 500 
dynamic_range = 3.298

try:
    dac = pwm.PWM_DAC( gpio_pin, pwm_frequency, dynamic_range, False)
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
