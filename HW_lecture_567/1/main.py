import numpy as np
import matplotlib.pyplot as plt

# Ввод начальных параметров через консоль
g = 9.81  # Ускорение свободного падения, м/с^2
v0 = float(input("Введите начальную скорость (м/с): "))
angle = float(input("Введите угол броска (в градусах): "))
y0 = float(input("Введите начальную высоту (м): "))
k = float(input("Введите коэффициент сопротивления среды k: "))

# Преобразование угла в радианы
theta = np.radians(angle)

# Начальные компоненты скорости
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)

# Время моделирования и шаг времени
t_max = 10  # Максимальное время моделирования, сек
dt = 0.01  # Шаг интегрирования, сек

# Массивы для хранения значений
t_values = [0]
x_values = [0]
y_values = [y0]
vx_values = [vx0]
vy_values = [vy0]


# Функции для производных
def dxdt(vx):
    return vx


def dydt(vy):
    return vy


def dvxdt(vx):
    return -k * vx


def dvydt(vy):
    return -g - k * vy


# Метод Рунге-Кутты 4-го порядка для численного интегрирования
t = 0
x, y = 0, y0
vx, vy = vx0, vy0

while y >= 0:
    # Расчет коэффициентов Рунге-Кутты для x
    k1_x = dxdt(vx)
    k1_y = dydt(vy)
    k1_vx = dvxdt(vx)
    k1_vy = dvydt(vy)

    k2_x = dxdt(vx + 0.5 * dt * k1_vx)
    k2_y = dydt(vy + 0.5 * dt * k1_vy)
    k2_vx = dvxdt(vx + 0.5 * dt * k1_vx)
    k2_vy = dvydt(vy + 0.5 * dt * k1_vy)

    k3_x = dxdt(vx + 0.5 * dt * k2_vx)
    k3_y = dydt(vy + 0.5 * dt * k2_vy)
    k3_vx = dvxdt(vx + 0.5 * dt * k2_vx)
    k3_vy = dvydt(vy + 0.5 * dt * k2_vy)

    k4_x = dxdt(vx + dt * k3_vx)
    k4_y = dydt(vy + dt * k3_vy)
    k4_vx = dvxdt(vx + dt * k3_vx)
    k4_vy = dvydt(vy + dt * k3_vy)

    # Обновление значений координат и скорости
    x += (dt / 6) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)
    y += (dt / 6) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
    vx += (dt / 6) * (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx)
    vy += (dt / 6) * (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy)
    t += dt

    # Запись результатов
    t_values.append(t)
    x_values.append(x)
    y_values.append(y)
    vx_values.append(vx)
    vy_values.append(vy)

# Визуализация результатов
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Траектория
axs[0, 0].plot(x_values, y_values)
axs[0, 0].set_title("Траектория движения")
axs[0, 0].set_xlabel("x (м)")
axs[0, 0].set_ylabel("y (м)")

# Скорость по x
axs[0, 1].plot(t_values, vx_values, label='Vx')
axs[0, 1].plot(t_values, vy_values, label='Vy')
axs[0, 1].set_title("Скорости по осям x и y")
axs[0, 1].set_xlabel("Время (с)")
axs[0, 1].set_ylabel("Скорость (м/с)")
axs[0, 1].legend()

# Координата x от времени
axs[1, 0].plot(t_values, x_values)
axs[1, 0].set_title("Координата x от времени")
axs[1, 0].set_xlabel("Время (с)")
axs[1, 0].set_ylabel("x (м)")

# Координата y от времени
axs[1, 1].plot(t_values, y_values)
axs[1, 1].set_title("Координата y от времени")
axs[1, 1].set_xlabel("Время (с)")
axs[1, 1].set_ylabel("y (м)")

plt.tight_layout()
plt.show()
