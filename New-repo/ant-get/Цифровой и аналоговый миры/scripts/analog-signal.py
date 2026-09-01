# Импортируем необходимые библиотеки
import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
frequency = 1  # частота сигнала в Гц
amplitude = 1  # амплитуда сигнала в В
duration = 2   # длительность сигнала в секундах
sampling_rate = 1000  # частота дискретизации в Гц

# Создаем временной массив
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Создаем аналоговый сигнал (синусоида)
x = amplitude * np.sin(2 * np.pi * frequency * t)

# Строим график
plt.figure(figsize=(10, 5))  # задаем размер графика
plt.plot(t, x, label=f'Сигнал: {frequency} Гц, {amplitude} В', linewidth=3)

# Добавляем подписи и сетку
formula = r'$x(t) = A \cdot \sin(2\pi f \cdot t)$' # LaTeX-формула
plt.title(f'Аналоговый сигнал {formula}')
plt.xlabel('Время t, с')
plt.ylabel('Амплитуда x, В')
plt.grid(True)
plt.legend()

# Сохраняем график в файл (dpi определяет разрешение изображения)
plt.savefig('Цифровой и аналоговый миры/pics/analog-signal.png', dpi=92, transparent=False)

# Показываем график
plt.show()
