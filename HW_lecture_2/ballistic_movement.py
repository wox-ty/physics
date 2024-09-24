import numpy as np
import matplotlib.pyplot as plt

g = 9.81


def trajectory(v0, angle, h0):
    # Перевод угла в радианы
    theta = np.radians(angle)

    # Время полета
    t_flight = (v0 * np.sin(theta) + np.sqrt((v0 * np.sin(theta)) ** 2 + 2 * g * h0)) / g

    # Время для построения графика
    t = np.linspace(0, t_flight, num=500)

    # Координаты движения по осям x и y
    x = v0 * np.cos(theta) * t
    y = h0 + v0 * np.sin(theta) * t - 0.5 * g * t ** 2

    return t, x, y


# Функция для расчета скорости на каждом этапе
def velocity(v0, angle, t):
    theta = np.radians(angle)

    # Скорость по осям x и y
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta) - g * t

    # Полная скорость (векторная сумма)
    v = np.sqrt(vx ** 2 + vy ** 2)

    return vx, vy, v


# Основная функция для визуализации
def plot_ballistic_motion(h0, v0, angle):
    t, x, y = trajectory(v0, angle, h0)

    # Расчет скоростей
    vx, vy, v = velocity(v0, angle, t)

    # График траектории
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(x, y)
    plt.title('Траектория движения тела')
    plt.xlabel('Расстояние (м)')
    plt.ylabel('Высота (м)')

    # График скорости от времени
    plt.subplot(3, 1, 2)
    plt.plot(t, v)
    plt.title('Зависимость скорости от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Скорость (м/с)')

    # Графики координат от времени
    plt.subplot(3, 1, 3)
    plt.plot(t, x, label="x(t)")
    plt.plot(t, y, label="y(t)")
    plt.title('Координаты от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Координаты (м)')
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    h0 = float(input("Введите начальную высоту (м): "))
    v0 = float(input("Введите начальную скорость (м/с): "))
    angle = float(input("Введите угол (градусы): "))

    plot_ballistic_motion(h0, v0, angle)
