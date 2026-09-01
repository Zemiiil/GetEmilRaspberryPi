# Импортируем необходимые библиотеки
import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
frequency = 1  # частота сигнала в Гц
amplitude = 1  # амплитуда сигнала в В
duration = 2   # длительность сигнала в секундах
sampling_rate = 20  # частота дискретизации в Гц

# Создаем временной массив
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Создаем дискретный сигнал (синусоида)
x = amplitude * np.sin(2 * np.pi * frequency * t)

# Строим график дискретного сигнала
plt.figure(figsize=(10, 5))  # задаем размер графика
plt.stem(t, x, 
         markerfmt='ro',  # красные кружки для маркеров
         basefmt='k-',    # черная базовая линия
         linefmt='r-',    # красные линии от базовой линии
         label=f'Сигнал: {frequency} Гц, {amplitude} В')

# Добавляем подписи и сетку
formula = r'$x[n] = A \cdot \sin(2\pi f \cdot n \Delta t)$' # LaTeX-формула
plt.title(f'Дискретный сигнал {formula}')
plt.xlabel('Время t, с')
plt.ylabel('Амплитуда x, В')
plt.grid(True)
plt.legend()

# Сохраняем график в файл (dpi определяет разрешение изображения)
plt.savefig('Цифровой и аналоговый миры/pics/discrete-signal.png', dpi=92, transparent=False)

# Показываем график
plt.show()
