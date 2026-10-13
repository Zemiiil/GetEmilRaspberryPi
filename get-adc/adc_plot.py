from matplotlib import pyplot as plt
def plot_voltage_vs_time(time_values, voltage_values, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(
        time_values,
        voltage_values,
        marker="o",
        markersize=3,
        label="Напряжение"
    )
    plt.title("Зависимость напряжения от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, max(time_values) if time_values else 1)
    plt.ylim(0, max_voltage)
    plt.grid(True, which="both", alpha=0.3)
    plt.legend(fontsize=8, loc="best")й
    plt.tight_layout()
    plt.show()
def plot_sampling_period_hist(time_values):
    sampling_periods = []
    for i in range(1, len(time_values)):
        period = time_values[i] - time_values[i - 1]
        sampling_periods.append(period)
    if not sampling_periods:
        print("Недостаточно измерений для гистограммы")
        return
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods)
    plt.title("Распределение периодов измерений")
    plt.xlabel("Время между измерениями, с")
    plt.ylabel("Количество измерений")
    plt.xlim(0, 0.06)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
