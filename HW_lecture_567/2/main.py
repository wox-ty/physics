import numpy as np
import matplotlib.pyplot as plt
import sys

# Выбор типа поля
print("Выберите тип силового поля:")
print("1. Гравитационное поле: U = m * g * y, зависит от высоты.")
print("2. Пружинное поле: U = 1/2 * k * (x^2 + y^2), симметрично вокруг начала координат.")
print("3. Пользовательское поле: степенная функция от координат.")

try:
    field_type = int(input("Введите номер поля: "))
except ValueError:
    sys.exit("Ошибка: номер поля должен быть числом.")

if field_type == 1:
    try:
        m = float(input("Введите массу тела (кг): "))  # Масса для гравитационного поля
        g = 9.81  # Ускорение свободного падения, м/с^2

        # Функция для гравитационной потенциальной энергии
        def potential_energy(x, y):
            return m * g * y  # U = m * g * y, зависит только от высоты y
    except ValueError:
        sys.exit("Ошибка: масса тела должна быть числом.")

elif field_type == 2:
    try:
        k = float(input("Введите жесткость пружины (Н/м): "))  # Коэффициент жесткости пружины

        # Функция для потенциальной энергии упругости
        def potential_energy(x, y):
            return 0.5 * k * (x**2 + y**2)  # U = 1/2 * k * r^2, где r - расстояние от точки (0,0)
    except ValueError:
        sys.exit("Ошибка: коэффициент жесткости должен быть числом.")

elif field_type == 3:
    try:
        a = float(input("Введите степень зависимости силы по x (например, 2 для x^2): "))
        b = float(input("Введите степень зависимости силы по y (например, 2 для y^2): "))
        coeff = float(input("Введите коэффициент перед степенной функцией: "))

        # Пользовательская функция для потенциальной энергии
        def potential_energy(x, y):
            return coeff * (x**a + y**b)
    except ValueError:
        sys.exit("Ошибка: параметры пользовательского поля должны быть числами.")

else:
    sys.exit("Неверный выбор поля. Программа завершена.")

# Задание диапазона координат
try:
    x_min = float(input("Введите минимальное значение x: "))
    x_max = float(input("Введите максимальное значение x: "))
    y_min = float(input("Введите минимальное значение y: "))
    y_max = float(input("Введите максимальное значение y: "))
except ValueError:
    sys.exit("Ошибка: границы координат должны быть числами.")

x_points = np.linspace(x_min, x_max, 100)
y_points = np.linspace(y_min, y_max, 100)

# Создание сетки координат
X, Y = np.meshgrid(x_points, y_points)
U = potential_energy(X, Y)

# Визуализация потенциального поля
plt.figure(figsize=(8, 6))
cp = plt.contourf(X, Y, U, levels=100, cmap='plasma')
plt.colorbar(cp, label='Потенциальная энергия U(x, y)')
plt.title("Потенциальное поле")
plt.xlabel("x (м)")
plt.ylabel("y (м)")
plt.show()
