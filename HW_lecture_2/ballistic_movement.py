import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.81


def trajectory(v0, angle, h0):
    theta = np.radians(angle)
    t_flight = (v0 * np.sin(theta) + np.sqrt((v0 * np.sin(theta)) ** 2 + 2 * g * h0)) / g
    t = np.linspace(0, t_flight, num=500)
    x = v0 * np.cos(theta) * t
    y = h0 + v0 * np.sin(theta) * t - 0.5 * g * t ** 2
    return t, x, y


def velocity(v0, angle, t):
    theta = np.radians(angle)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta) - g * t
    v = np.sqrt(vx ** 2 + vy ** 2)
    return vx, vy, v


def animate_ballistic_motion(h0, v0, angle):
    t, x, y = trajectory(v0, angle, h0)
    vx, vy, v = velocity(v0, angle, t)

    fig, axes = plt.subplots(3, 1, figsize=(8, 10))
    fig.suptitle("Баллистическое движение тела", fontsize=16)

    # График траектории
    axes[0].set_title("Траектория движения тела")
    axes[0].set_xlabel("Расстояние (м)")
    axes[0].set_ylabel("Высота (м)")
    axes[0].grid()
    traj_line, = axes[0].plot([], [], 'b')

    # График скорости
    axes[1].set_title("Зависимость скорости от времени")
    axes[1].set_xlabel("Время (с)")
    axes[1].set_ylabel("Скорость (м/с)")
    axes[1].grid()
    speed_line, = axes[1].plot([], [], 'g')

    # Графики координат
    axes[2].set_title("Координаты от времени")
    axes[2].set_xlabel("Время (с)")
    axes[2].set_ylabel("Координаты (м)")
    axes[2].grid()
    x_line, = axes[2].plot([], [], 'r', label="x(t)")
    y_line, = axes[2].plot([], [], 'm', label="y(t)")
    axes[2].legend()

    def update(frame):
        traj_line.set_data(x[:frame], y[:frame])
        speed_line.set_data(t[:frame], v[:frame])
        x_line.set_data(t[:frame], x[:frame])
        y_line.set_data(t[:frame], y[:frame])

        axes[0].set_xlim(0, max(x))
        axes[0].set_ylim(0, max(y) + 1)

        axes[1].set_xlim(0, max(t))
        axes[1].set_ylim(0, max(v) + 1)

        axes[2].set_xlim(0, max(t))
        axes[2].set_ylim(0, max(max(x), max(y)) + 1)

        return traj_line, speed_line, x_line, y_line

    ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    h0 = float(input("Введите начальную высоту (м): "))
    v0 = float(input("Введите начальную скорость (м/с): "))
    angle = float(input("Введите угол (градусы): "))

    animate_ballistic_motion(h0, v0, angle)
