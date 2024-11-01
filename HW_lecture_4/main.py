import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Параметры системы
mass1 = 2.0  # Масса первого тела
mass2 = 1.0  # Масса второго тела
velocity1 = np.array([2.0, 3.0])  # Начальная скорость первого тела (x, y)
velocity2 = np.array([-1.5, -2.0])  # Начальная скорость второго тела (x, y)
position1 = np.array([2.0, 3.0])  # Начальная позиция первого тела (x, y)
position2 = np.array([8.0, 5.0])  # Начальная позиция второго тела (x, y)

# Размеры оболочки
width = 10.0
height = 10.0

# Параметры анимации
fig, ax = plt.subplots()
ax.set_xlim(0, width)
ax.set_ylim(0, height)

body1, = ax.plot([], [], 'ro', markersize=10)
body2, = ax.plot([], [], 'bo', markersize=10)


def update_positions(pos1, vel1, pos2, vel2, dt):
    # Обновление позиций
    pos1 += vel1 * dt
    pos2 += vel2 * dt

    # Проверка столкновения с оболочкой
    if pos1[0] <= 0 or pos1[0] >= width:
        vel1[0] *= -1
    if pos1[1] <= 0 or pos1[1] >= height:
        vel1[1] *= -1
    if pos2[0] <= 0 or pos2[0] >= width:
        vel2[0] *= -1
    if pos2[1] <= 0 or pos2[1] >= height:
        vel2[1] *= -1

    # Проверка столкновения тел
    delta_pos = pos2 - pos1
    distance = np.linalg.norm(delta_pos)
    if distance <= 0.5:  # Пороговое значение для столкновения (радиусы тел)
        # Расчет новых скоростей при абсолютно упругом столкновении
        delta_vel = vel2 - vel1
        collision_norm = delta_pos / distance

        v1_new = vel1 + (2 * mass2 / (mass1 + mass2)) * np.dot(delta_vel, collision_norm) * collision_norm
        v2_new = vel2 - (2 * mass1 / (mass1 + mass2)) * np.dot(delta_vel, collision_norm) * collision_norm

        vel1[:] = v1_new
        vel2[:] = v2_new

    return pos1, vel1, pos2, vel2


def animate(i):
    global position1, velocity1, position2, velocity2
    dt = 0.05
    position1, velocity1, position2, velocity2 = update_positions(position1, velocity1, position2, velocity2, dt)
    body1.set_data(position1[0], position1[1])
    body2.set_data(position2[0], position2[1])
    return body1, body2


ani = animation.FuncAnimation(fig, animate, frames=300, interval=50, blit=True)
plt.show()
