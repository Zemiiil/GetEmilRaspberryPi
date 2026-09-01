# Импортируем необходимые библиотеки
import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
frequency = 1  # частота сигнала в Гц
amplitude = 1  # амплитуда сигнала в В
duration = 2   # длительность сигнала в секундах
sampling_rate = 20  # частота дискретизации в Гц
quantization_levels = 8  # количество уровней квантования

# Создаем временной массив
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Создаем аналоговый сигнал (синусоида)
x = amplitude * np.sin(2 * np.pi * frequency * t)

# Квантование сигнала
step = 2 * amplitude / quantization_levels
x_quantized = np.floor(x / step) * step
# Делаем именно 8, а не 9 уровней квантования
x_quantized = x_quantized.clip(max=0.75)

# Строим графики
plt.figure(figsize=(10, 5))
plt.stem(t, x_quantized, 
         markerfmt='ro',  # красные кружки для маркеров
         basefmt='k-',    # черная базовая линия
         linefmt='r-',    # красные линии от базовой линии,
         label=f'Сигнал: {frequency} Гц, {amplitude} В')

# Добавляем подписи и сетку
formula = r'$x[n] = A \cdot \sin(2\pi f \cdot n \Delta t)$' # LaTeX-формула
plt.title(f'Цифровой сигнал {formula}, уровней квантования: {quantization_levels}')
plt.xlabel('Время t, с')
plt.ylabel('Амплитуда x, В')
plt.grid(True)
plt.legend()

# Сохраняем график в файл (dpi определяет разрешение изображения)
plt.savefig('Цифровой и аналоговый миры/pics/digital-signal.png', dpi=92, transparent=False)

# Показываем график
plt.show()
