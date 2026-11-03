import time

import numpy as np
import pandas as pd
import RPi.GPIO as GPIO

from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time
from adc_plot import plot_sampling_period_hist

gpio_pin = 14          # выход, на который подаём сигнал (BCM-нумерация)
charge_duration = 1.0  # сколько секунд выход 14 включён
discharge_duration = 1.0  # сколько секунд снимаем после выключения
dynamic_range = 5.186

voltage_values = []
time_values = []
gpio_states = []
adc = None


def measure(duration, state, start_time):
    # Снимаем показания АЦП в течение duration секунд
    period_start = time.time()
    while time.time() - period_start < duration:
        voltage = adc.get_voltage()
        voltage_values.append(voltage)
        time_values.append(time.time() - start_time)
        gpio_states.append(state)


GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT, initial=0)
try:
    adc = MCP3021(dynamic_range, verbose=False)
    start_time = time.time()

    # 1 секунда: выход 14 включён
    GPIO.output(gpio_pin, 1)
    measure(charge_duration, 1, start_time)

    # 1 секунда: выход 14 выключен
    GPIO.output(gpio_pin, 0)
    measure(discharge_duration, 0, start_time)

    print(f"Всего измерений: {len(voltage_values)}")

    if voltage_values:
        data = pd.DataFrame({
            "time_s": np.array(time_values),
            "voltage_V": np.array(voltage_values),
            "gpio14": np.array(gpio_states),
        })
        data.to_csv("lab.csv", index=False)
        print("Данные сохранены в lab.csv")

        plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
        plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nПрограмма завершилась")
finally:
    GPIO.output(gpio_pin, 0)
    GPIO.cleanup()
    if adc is not None:
        adc.deinit()
