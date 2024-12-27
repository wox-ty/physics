import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Ввод параметров
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
line, = ax.plot([], [], lw=2, color="purple")
trail, = ax.plot([], [], lw=1, color="blue")

# Функция инициализации
def init():
    line.set_data([], [])
    trail.set_data([], [])
    return line, trail

# Функция анимации
def animate(i):
    # Текущая точка и траектория
    line.set_data([x[i]], [y[i]])
    trail.set_data(x[:i + 1], y[:i + 1])
    return line, trail

# Создание анимации
anim = FuncAnimation(fig, animate, init_func=init, frames=frame_count, interval=20, blit=True, repeat=False)

plt.title('Анимация движения точки на ободе колеса')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
