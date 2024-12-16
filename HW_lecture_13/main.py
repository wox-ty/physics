import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
from matplotlib.animation import FuncAnimation

# Константы
k = 8.9875e9  # Константа Кулона (Н·м²/Кл²)
charges = []  # Список зарядов
dipole = None  # Диполь (положение и момент)
selected_charge = None  # Заряд, который двигаем
selected_dipole = False  # Флаг для перемещения диполя
add_dipole_mode = False  # Режим добавления диполя

# Сетка координат
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots(figsize=(10, 8))
charge_patches = []  # Графические элементы для зарядов


def calculate_potential(charges, X, Y):
    potential = np.zeros_like(X)
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        potential += k * q / np.sqrt((X - x0) ** 2 + (Y - y0) ** 2 + 1e-10)
    return potential


def calculate_field(charges, X, Y):
    Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        R2 = (X - x0) ** 2 + (Y - y0) ** 2 + 1e-10
        Ex += k * q * (X - x0) / R2 ** 1.5
        Ey += k * q * (Y - y0) / R2 ** 1.5
    return Ex, Ey


def calculate_dipole_force_and_torque(dipole, charges):
    px, py = dipole["moment"]
    x_dip, y_dip = dipole["pos"]
    Fx, Fy, torque = 0, 0, 0
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        R2 = (x_dip - x0) ** 2 + (y_dip - y0) ** 2 + 1e-10
        Ex = k * q * (x_dip - x0) / R2 ** 1.5
        Ey = k * q * (y_dip - y0) / R2 ** 1.5
        Fx += px * Ex + py * Ey
        Fy += px * Ey - py * Ex
        torque += q * ((y_dip - y0) * px - (x_dip - x0) * py) / R2 ** 1.5
    return Fx, Fy, torque


def update_field():
    ax.clear()
    V = calculate_potential(charges, X, Y)
    Ex, Ey = calculate_field(charges, X, Y)
    ax.streamplot(X, Y, Ex, Ey, color='green', density=1.5, linewidth=0.8)
    ax.contour(X, Y, V, levels=20, colors='red', linewidths=0.8)
    ax.axis('equal')
    ax.grid(True)
    charge_patches.clear()
    for charge in charges:
        color = 'red' if charge["q"] > 0 else 'blue'
        patch = Circle(charge["pos"], 0.05, color=color)
        charge_patches.append(patch)
        ax.add_patch(patch)
    if dipole:
        x_dip, y_dip = dipole["pos"]
        px, py = dipole["moment"]
        ax.add_patch(FancyArrow(x_dip, y_dip, px * 0.2, py * 0.2, color='purple', width=0.02))
        Fx, Fy, torque = calculate_dipole_force_and_torque(dipole, charges)
        ax.text(-1.8, 1.8, f"F_x: {Fx:.2e} N\nF_y: {Fy:.2e} N\nTorque: {torque:.2e} N·m", color='purple')
    plt.draw()  # Явно перерисовываем график после обновления


def on_click(event):
    global selected_charge, selected_dipole, dipole
    if event.inaxes is None:
        return
    for charge in charges:
        x0, y0 = charge["pos"]
        if np.hypot(event.xdata - x0, event.ydata - y0) < 0.1:
            selected_charge = charge
            return
    if add_dipole_mode:  # Добавление диполя
        dipole = {"pos": (event.xdata, event.ydata), "moment": (1e-9, 0)}
        update_field()
    elif event.button == 1:  # Добавление положительного заряда
        charges.append({"q": 1e-9, "pos": (event.xdata, event.ydata)})
        update_field()
    elif event.button == 3:  # Добавление отрицательного заряда
        charges.append({"q": -1e-9, "pos": (event.xdata, event.ydata)})
        update_field()


def on_release(event):
    global selected_charge, selected_dipole
    selected_charge = None
    selected_dipole = False


def on_motion(event):
    if selected_charge is not None and event.inaxes:
        selected_charge["pos"] = (event.xdata, event.ydata)
        update_field()
    elif selected_dipole and dipole and event.inaxes:
        dipole["pos"] = (event.xdata, event.ydata)
        update_field()


def on_scroll(event):
    if event.inaxes is None:
        return
    for charge in charges:
        x0, y0 = charge["pos"]
        if np.hypot(event.xdata - x0, event.ydata - y0) < 0.1:
            charge["q"] += 1e-10 * event.step
            update_field()
            return
    if dipole and np.hypot(event.xdata - dipole["pos"][0], event.ydata - dipole["pos"][1]) < 0.1:
        dipole["moment"] = (dipole["moment"][0] + 1e-10 * event.step, dipole["moment"][1])
        update_field()


def on_key(event):
    global add_dipole_mode
    if event.key == "d":
        add_dipole_mode = not add_dipole_mode
        print("Режим добавления диполя:", "Включен" if add_dipole_mode else "Выключен")


def main():
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('scroll_event', on_scroll)
    fig.canvas.mpl_connect('key_press_event', on_key)
    update_field()
    plt.show()


if __name__ == "__main__":
    main()
