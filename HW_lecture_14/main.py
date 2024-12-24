import numpy as np
import matplotlib.pyplot as plt

def visualize_dielectric_interface(epsilon1, epsilon2, E0, angle):
    """
    Визуализация преломления электрических линий напряжённости и смещения
    на границе двух диэлектриков.

    Аргументы:
    epsilon1 -- диэлектрическая проницаемость первой среды
    epsilon2 -- диэлектрическая проницаемость второй среды
    E0 -- величина внешнего электрического поля
    angle -- угол падения электрического поля в радианах
    """
    # Определяем границу раздела
    boundary_x = np.linspace(-1, 1, 400)
    boundary_y = np.zeros_like(boundary_x)

    # Компоненты электрического поля в первой среде
    E0_x = E0 * np.cos(angle)
    E0_y = E0 * np.sin(angle)

    # Рассчитываем угол преломления во второй среде
    theta1 = angle
    theta2 = np.arcsin((epsilon1 / epsilon2) * np.sin(theta1))

    # Компоненты электрического поля во второй среде
    E2 = E0 * (epsilon1 / epsilon2)
    E2_x = E2 * np.cos(theta2)
    E2_y = E2 * np.sin(theta2)

    # Визуализация границы раздела
    plt.plot(boundary_x, boundary_y, 'k--', label="Граница раздела")

    # Визуализация линий напряжённости (Electric Field, E)
    plt.quiver(-0.5, 0.5, E0_x, E0_y, angles='xy', scale_units='xy', scale=1, color='r', label='Поле E в среде 1')
    plt.quiver(0.5, 0.5, E2_x, E2_y, angles='xy', scale_units='xy', scale=1, color='b', label='Поле E в среде 2')

    # Рассчитываем электрическое смещение (Displacement Vector, D)
    D0 = epsilon1 * E0
    D0_x = D0 * np.cos(angle)
    D0_y = D0 * np.sin(angle)
    D2 = epsilon2 * E2
    D2_x = D2 * np.cos(theta2)
    D2_y = D2 * np.sin(theta2)

    # Визуализация линий смещения (Displacement Field, D)
    plt.quiver(-0.5, -0.5, D0_x, D0_y, angles='xy', scale_units='xy', scale=1, color='g', label='Смещение D в среде 1')
    plt.quiver(0.5, -0.5, D2_x, D2_y, angles='xy', scale_units='xy', scale=1, color='m', label='Смещение D в среде 2')

    # Настройка графика
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.legend()
    plt.grid()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Преломление линий напряжённости и смещения на границе диэлектриков")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# Пример использования
epsilon1 = 2  # Диэлектрическая проницаемость первой среды
epsilon2 = 5  # Диэлектрическая проницаемость второй среды
E0 = 1        # Модуль внешнего электрического поля
angle = np.radians(45)  # Угол падения в радианах

visualize_dielectric_interface(epsilon1, epsilon2, E0, angle)
