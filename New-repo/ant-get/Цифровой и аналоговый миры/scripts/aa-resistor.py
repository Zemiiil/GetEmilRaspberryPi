import numpy as np
import matplotlib.pyplot as plt

# Параметры батарейки АА
E0 = 1.5  # Начальное напряжение, В
R_int = 0.1  # Внутреннее сопротивление, Ом
C = 2000  # Эквивалентная ёмкость, мАч

# Параметры нагрузки
R_load = 1000  # Сопротивление нагрузки, Ом

# Время измерения (в секундах)
t = np.linspace(0, 7200, 1000)  # от 0 до 2 часов

# Расчет тока разряда
I = E0 / (R_load + R_int)

# Расчет оставшегося заряда
Q_remaining = C - I * t / 3600  # перевод в часы

# Расчет напряжения с учетом разряда
U = E0 * np.exp(-t / (C * (R_load + R_int) / 3600))

# Создание графика
plt.figure(figsize=(10, 5))
plt.plot(t/3600, U, label='Напряжение, В', color='b', linewidth=2)

# Добавление визуальных элементов
plt.axhline(1.0, color='r', linestyle='--', linewidth=1.5, label='Критический уровень 1.0В')
plt.axhline(0.7, color='m', linestyle=':', linewidth=1.5, label='Минимальный уровень 0.7В')

# Оформление графика
plt.title(f'Разряд батарейки АА при нагрузке $R = {R_load}\Omega$', fontsize=16)
plt.xlabel('Время, часы', fontsize=14)
plt.ylabel('Напряжение, В', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.ylim(0, 1.6)
plt.xlim(0, 2)
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=12)

# Добавление аннотаций
plt.text(0.6, 1.4, f'Начальное напряжение: {E0} [В]', fontsize=12, color='blue', backgroundcolor='white')
plt.text(0.6, 1.3, f'Внутреннее сопротивление: {R_int} [Ом]', fontsize=12, color='blue', backgroundcolor='white')
plt.text(0.6, 1.2, f'Ёмкость: {C} [мАч]', fontsize=12, color='blue', backgroundcolor='white')

# Сохраняем график в файл (dpi определяет разрешение изображения)
plt.savefig('Цифровой и аналоговый миры/pics/aa-resistor.png', dpi=92, transparent=False)

# Показываем график
plt.show()
