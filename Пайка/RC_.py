# Зарядка и разрядка RC-цепи.
# GPIO14 = 1 -> конденсатор заряжается, GPIO14 = 0 -> разряжается.
# Напряжение на конденсаторе меряет MCP3021 по I2C.
# Перед запуском (если I2C не работает после прошлых запусков):
#   raspi-gpio set 2 a0
#   raspi-gpio set 3 a0
import csv
import time

import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.186   # В, динамический диапазон MCP3021
PIN = 14                # GPIO (BCM), от которого питается RC-цепь
PRE_DISCHARGE = 50      # с, ждём перед началом, чтобы конденсатор разрядился
CHARGE_TIME = 50        # с, сколько держим GPIO14 = 1
DISCHARGE_TIME = 50     # с, сколько держим GPIO14 = 0
CSV_NAME = "lab.csv"
PLOT_NAME = "rc_plot.png"

times = []
voltages = []
states = []


def record(adc, duration, state, start):
    # Снимаем напряжение duration секунд
    t_end = time.time() + duration
    while time.time() < t_end:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)
        states.append(state)


def save_csv():
    with open(CSV_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "voltage_V", "gpio14"])
        for t, v, s in zip(times, voltages, states):
            writer.writerow([f"{t:.6f}", f"{v:.4f}", s])
    print(f"Сохранено в {CSV_NAME}")


def estimate_tau(t, u, s):
    # tau по зарядке: время, за которое напряжение выросло на 63% от размаха
    charge = s == 1
    if not charge.any():
        return None
    t_c, u_c = t[charge], u[charge]
    u_start, u_end = u_c[0], u_c.max()
    if u_end - u_start < 0.1:
        return None
    level = u_start + 0.63 * (u_end - u_start)
    idx = np.argmax(u_c >= level)
    return t_c[idx] - t_c[0]


def plot():
    t = np.array(times)
    u = np.array(voltages)
    s = np.array(states)

    title = "Зарядка и разрядка конденсатора"
    tau = estimate_tau(t, u, s)
    if tau is not None:
        title += f"  (tau ≈ {tau:.3f} с)"
        print(f"Постоянная времени tau ≈ {tau:.3f} с")

    plt.figure(figsize=(10, 6))
    plt.plot(t, u, ".-", markersize=2, label="Напряжение на конденсаторе")
    if (s == 0).any() and (s == 1).any():
        t_off = t[np.argmax(s == 0)]
        plt.axvline(t_off, color="red", linestyle="--", label="GPIO14 выключен")
    plt.title(title)
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.ylim(0, DYNAMIC_RANGE)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_NAME, dpi=150)
    print(f"График сохранён в {PLOT_NAME}")
    plt.show()


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=0)
adc = MCP3021(DYNAMIC_RANGE)
try:
    print(f"Разряжаю конденсатор {PRE_DISCHARGE} с перед началом...")
    time.sleep(PRE_DISCHARGE)
    start = time.time()

    print("Зарядка: GPIO14 = 1")
    GPIO.output(PIN, 1)
    record(adc, CHARGE_TIME, 1, start)

    print("Разрядка: GPIO14 = 0")
    GPIO.output(PIN, 0)
    record(adc, DISCHARGE_TIME, 0, start)
except KeyboardInterrupt:
    print("\nИзмерение прервано")
finally:
    GPIO.output(PIN, 0)
    GPIO.cleanup()
    adc.deinit()

if times:
    print(f"Измерений: {len(times)}, частота ~{len(times) / times[-1]:.0f} Гц")
    save_csv()
    plot()
