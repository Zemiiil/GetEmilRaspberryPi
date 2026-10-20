import time
from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time
from adc_plot import plot_sampling_period_hist
duration = 3.0
voltage_values = []
time_values = []
time_elapsed=[]
adc = None
try:
    adc = MCP3021(5.186, verbose=False)
    start_time = time.time()
    while time.time() - start_time < duration:
        start_measure=time.time()
        voltage = adc.get_voltage()
        voltage_values.append(voltage)
        elapsed_time = time.time() - start_time
        time_exp=time.time()-start_measure
        time_values.append(elapsed_time)
        time_elapsed.append(time_exp)

    print(f"Всего измерений: {len(voltage_values)}")
    adc.deinit()
    if voltage_values:
        plot_voltage_vs_time(
            time_values,
            voltage_values,
            5
        )
        plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nПограмма завершилась")
