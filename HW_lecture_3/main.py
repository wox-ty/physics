import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

R = float(input("Радиус колеса: "))
V = float(input("Скорость центра масс колеса: "))
frame_count = int(input("Количество кадров для анимации: "))

# Время для вычислений
t = np.linspace(0, 2 * np.pi, frame_count)

# Угловая скорость
omega = V / R

# Траектория точки на ободе
x = V * t - R * np.sin(omega * t)
y = R - R * np.cos(omega * t)

# Подготовка графика
fig, ax = plt.subplots()
ax.set_xlim(0, V * 2 * np.pi)
ax.set_ylim(-R, 2 * R)

colors = plt.cm.Purples(np.linspace(1, 0.5, frame_count))

def init():
    return []

def animate(i):
    ax.clear()
    ax.set_xlim(0, V * 2 * np.pi)
    ax.set_ylim(-R, 2 * R)
    plt.title('Анимация движения точки на ободе колеса')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    for j in range(i):
        ax.plot([x[j], x[j + 1]], [y[j], y[j + 1]], color=colors[j], lw=2)
    return []

anim = FuncAnimation(fig, animate, init_func=init, frames=len(t) - 1, interval=20, blit=True, repeat=False)

plt.show()
