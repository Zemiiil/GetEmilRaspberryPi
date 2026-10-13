import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time
from adc_plot import plot_sampling_period_hist
dynamic_range = 3.16
duration = 3.0
voltage_values = []
time_values = []
adc = None
try:
    adc = R2R_ADC(
        dynamic_range,
        compare_time=0.0001,
        verbose=False
    )
    start_time = time.time()
    while time.time() - start_time < duration:
        voltage = adc.get_sc_voltage()
        voltage_values.append(voltage)
        elapsed_time = time.time() - start_time
        time_values.append(elapsed_time)

    print(f"Всего измерений: {len(voltage_values)}")
    if voltage_values:
        plot_voltage_vs_time(
            time_values,
            voltage_values,
            dynamic_range
        )
        plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nПограмма завершилась")

finally:
    if adc is not None:
        adc.deinit()
