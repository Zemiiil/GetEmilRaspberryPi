# Импортируем необходимые библиотеки
import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
frequency = 1 # частота сигнала в Гц
amplitude = 1 # амплитуда сигнала в В
duration = 2  # длительность сигнала в секундах
sampling_rate = 1000 # частота дискретизации в Гц
quantization_levels = 8 # количество уровней квантования

# Создаем временной массив
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Создаем аналоговый сигнал (синусоида)
x = amplitude * np.sin(2 * np.pi * frequency * t)

# Квантование сигнала
# Определяем шаг квантования
step = 2 * amplitude / quantization_levels
# Квантуем сигнал
x_quantized = np.floor(x / step) * step
# Делаем именно 8, а не 9 уровней квантования
x_quantized = x_quantized.clip(max=0.75)

# Строим графики
plt.figure(figsize=(10, 5))
plt.plot(t, x_quantized, label=f'Сигнал: {frequency} Гц, {amplitude} В', linewidth=2, color='red')

# Добавляем подписи и сетку
formula = r'$x(t) = A \cdot \sin(2\pi f \cdot t)$' # LaTeX-формула
plt.title(f'Квантованный сигнал {formula}, уровней квантования: {quantization_levels}')
plt.xlabel('Время t, с')
plt.ylabel('Амплитуда x, В')
plt.grid(True)
plt.legend()

# Сохраняем график в файл (dpi определяет разрешение изображения)
plt.savefig('Цифровой и аналоговый миры/pics/quantized-signal.png', dpi=92, transparent=False)

# Показываем график
plt.show()
