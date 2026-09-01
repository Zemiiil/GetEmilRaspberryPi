import numpy as np
import matplotlib.pyplot as plt

# Параметры процесса испарения
initial_mass = 500  # Начальная масса воды, г
evaporation_rate = 0.002  # Интенсивность испарения, 1/с

# Время измерения (в секундах)
t = np.linspace(0, 3600, 1000)  # от 0 до 1 часа

# Расчет массы воды с учетом испарения
# Используем экспоненциальное затухание
mass = initial_mass * np.exp(-evaporation_rate * t)

# Создание графика
plt.figure(figsize=(10, 5))
plt.plot(t/3600, mass, label='Масса воды, г', color='b', linewidth=2)

# Добавление визуальных элементов
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.fill_between(t/3600, mass, color='lightblue', alpha=0.5)

# Оформление графика
plt.title('Процесс испарения воды $m(t)=m_0 \cdot e^{−kt}$', fontsize=16)
plt.xlabel('Время, часы', fontsize=14)
plt.ylabel('Масса воды, г', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.ylim(0, initial_mass * 1.1)
plt.xlim(0, 1)
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=12)

# Добавление аннотаций
plt.text(0.3, initial_mass * 0.75,
         f'Начальная масса: {initial_mass:.1f} [г]\n'
         f'Интенсивность испарения: {evaporation_rate} [1/с]',
         fontsize=12, color='blue', backgroundcolor='white')

# Сохраняем график в файл (dpi определяет разрешение изображения)
plt.savefig('Цифровой и аналоговый миры/pics/water.png', dpi=92, transparent=False)

# Показываем график
plt.show()
