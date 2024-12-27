import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Константы
G = 9.81  # Ускорение свободного падения, м/с^2

def get_initial_parameters():
    """Функция для ввода начальных параметров."""
    try:
        v0 = float(input("Введите начальную скорость (м/с): "))
        angle = float(input("Введите угол броска (в градусах): "))
        y0 = float(input("Введите начальную высоту (м): "))
        k = float(input("Введите коэффициент сопротивления среды k: "))
        if v0 <= 0 or angle < 0 or y0 < 0 or k < 0:
            raise ValueError("Все значения должны быть положительными, кроме угла, который может быть 0.")
        return v0, angle, y0, k
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
        exit(1)

def runge_kutta_4(v0, angle, y0, k, dt=0.01, t_max=10):
    """Решение задачи методом Рунге-Кутты 4-го порядка."""
    theta = np.radians(angle)
    vx, vy = v0 * np.cos(theta), v0 * np.sin(theta)

    t_values, x_values, y_values, vx_values, vy_values = [0], [0], [y0], [vx], [vy]

    x, y, t = 0, y0, 0
    while y >= 0 and t <= t_max:
        k1_x, k1_y, k1_vx, k1_vy = vx, vy, -k * vx, -G - k * vy
        k2_x, k2_y = vx + 0.5 * dt * k1_vx, vy + 0.5 * dt * k1_vy
        k2_vx, k2_vy = -k * (vx + 0.5 * dt * k1_vx), -G - k * (vy + 0.5 * dt * k1_vy)

        k3_x, k3_y = vx + 0.5 * dt * k2_vx, vy + 0.5 * dt * k2_vy
        k3_vx, k3_vy = -k * (vx + 0.5 * dt * k2_vx), -G - k * (vy + 0.5 * dt * k2_vy)

        k4_x, k4_y = vx + dt * k3_vx, vy + dt * k3_vy
        k4_vx, k4_vy = -k * (vx + dt * k3_vx), -G - k * (vy + dt * k3_vy)

        x += (dt / 6) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)
        y += (dt / 6) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
        vx += (dt / 6) * (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx)
        vy += (dt / 6) * (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy)
        t += dt

        t_values.append(t)
        x_values.append(x)
        y_values.append(y)
        vx_values.append(vx)
        vy_values.append(vy)

    return t_values, x_values, y_values, vx_values, vy_values

def animate_results(t_values, x_values, y_values, vx_values, vy_values):
    """Анимация всех графиков."""
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Настройка графиков
    axs[0, 0].set_xlim(0, max(x_values) * 1.1)
    axs[0, 0].set_ylim(0, max(y_values) * 1.1)
    axs[0, 0].set_title("Траектория движения")
    axs[0, 0].set_xlabel("x (м)")
    axs[0, 0].set_ylabel("y (м)")
    traj_line, = axs[0, 0].plot([], [], lw=2, label="Траектория")
    traj_point, = axs[0, 0].plot([], [], 'ro')  # Текущая точка

    axs[0, 1].set_xlim(0, max(t_values) * 1.1)
    axs[0, 1].set_ylim(min(min(vx_values), min(vy_values)) * 1.1, max(max(vx_values), max(vy_values)) * 1.1)
    axs[0, 1].set_title("Скорости по осям x и y")
    axs[0, 1].set_xlabel("Время (с)")
    axs[0, 1].set_ylabel("Скорость (м/с)")
    vx_line, = axs[0, 1].plot([], [], label="Vx")
    vy_line, = axs[0, 1].plot([], [], label="Vy")
    axs[0, 1].legend()

    axs[1, 0].set_xlim(0, max(t_values) * 1.1)
    axs[1, 0].set_ylim(0, max(x_values) * 1.1)
    axs[1, 0].set_title("Координата x от времени")
    axs[1, 0].set_xlabel("Время (с)")
    axs[1, 0].set_ylabel("x (м)")
    x_line, = axs[1, 0].plot([], [], label="x(t)")

    axs[1, 1].set_xlim(0, max(t_values) * 1.1)
    axs[1, 1].set_ylim(0, max(y_values) * 1.1)
    axs[1, 1].set_title("Координата y от времени")
    axs[1, 1].set_xlabel("Время (с)")
    axs[1, 1].set_ylabel("y (м)")
    y_line, = axs[1, 1].plot([], [], label="y(t)")

    # Функция для обновления кадров
    def update(frame):
        traj_line.set_data(x_values[:frame], y_values[:frame])
        traj_point.set_data([x_values[frame]], [y_values[frame]])

        vx_line.set_data(t_values[:frame], vx_values[:frame])
        vy_line.set_data(t_values[:frame], vy_values[:frame])

        x_line.set_data(t_values[:frame], x_values[:frame])
        y_line.set_data(t_values[:frame], y_values[:frame])

        return traj_line, traj_point, vx_line, vy_line, x_line, y_line

    # Анимация
    ani = FuncAnimation(fig, update, frames=len(t_values), interval=20, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

def main():
    v0, angle, y0, k = get_initial_parameters()
    t_values, x_values, y_values, vx_values, vy_values = runge_kutta_4(v0, angle, y0, k)
    animate_results(t_values, x_values, y_values, vx_values, vy_values)
    print(f"Максимальная длина траектории: {max(x_values):.2f} м")
    print(f"Общее время полета: {t_values[-1]:.2f} с")

if __name__ == "__main__":
    main()
