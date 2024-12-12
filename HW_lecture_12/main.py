import numpy as np
import matplotlib.pyplot as plt

# Задание параметров системы
charges = [
    {"q": 1e-9, "pos": (-0.5, 0)},  # Заряд +1 нКл
    {"q": -1e-9, "pos": (0.5, 0)},  # Заряд -1 нКл
]
k = 8.9875e9  # Константа Кулона (Н·м²/Кл²)

# Создание сетки координат
x = np.linspace(-1, 1, 200)
y = np.linspace(-1, 1, 200)
X, Y = np.meshgrid(x, y)

# Функция для расчёта потенциала
def calculate_potential(charges, X, Y):
    potential = np.zeros_like(X)
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        potential += k * q / np.sqrt((X - x0)**2 + (Y - y0)**2)
    return potential

# Функция для расчёта электрического поля
def calculate_field(charges, X, Y):
    Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        R2 = (X - x0)**2 + (Y - y0)**2
        Ex += k * q * (X - x0) / R2**1.5
        Ey += k * q * (Y - y0) / R2**1.5
    return Ex, Ey

# Вычисление потенциала и поля
V = calculate_potential(charges, X, Y)
Ex, Ey = calculate_field(charges, X, Y)

# Построение графиков
plt.figure(figsize=(10, 8))

# Линии напряжённости
plt.streamplot(X, Y, Ex, Ey, color='blue', density=1.5, linewidth=0.8)

# Эквипотенциальные поверхности
contours = plt.contour(X, Y, V, levels=20, colors='red', linewidths=0.8)

# Отображение зарядов
for charge in charges:
    plt.plot(charge["pos"][0], charge["pos"][1], 'o', markersize=10,
             color='red' if charge["q"] > 0 else 'blue')

plt.xlabel('X (м)')
plt.ylabel('Y (м)')
plt.title('Эквипотенциальные поверхности и линии напряжённости')
plt.colorbar(contours, label="Потенциал (В)")
plt.grid()
plt.axis('equal')
plt.show()
