import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Константы
k = 8.9875e9  # Константа Кулона (Н·м²/Кл²)
charges = []  # Список зарядов
selected_charge = None  # Заряд, который двигаем

# Сетка координат
x = np.linspace(-2, 2, 200)
y = np.linspace(-2, 2, 200)
X, Y = np.meshgrid(x, y)

# Функция для расчëта потенциала
def calculate_potential(charges, X, Y):
    potential = np.zeros_like(X)
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        potential += k * q / np.sqrt((X - x0)**2 + (Y - y0)**2 + 1e-10)
    return potential

# Функция для расчëта электрического поля
def calculate_field(charges, X, Y):
    Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        R2 = (X - x0)**2 + (Y - y0)**2 + 1e-10
        Ex += k * q * (X - x0) / R2**1.5
        Ey += k * q * (Y - y0) / R2**1.5
    return Ex, Ey

# Функция для обновления графики
def update_plot():
    plt.clf()
    V = calculate_potential(charges, X, Y)
    Ex, Ey = calculate_field(charges, X, Y)

    plt.streamplot(X, Y, Ex, Ey, color='green', density=1.5, linewidth=0.8)
    contours = plt.contour(X, Y, V, levels=20, colors='red', linewidths=0.8)

    for charge in charges:
        color = 'red' if charge["q"] > 0 else 'blue'
        plt.gca().add_patch(Circle(charge["pos"], 0.05, color=color))

    plt.axis('equal')
    plt.grid(True)
    plt.draw()

# Обработчики событий
def on_click(event):
    global selected_charge
    if event.inaxes is None:
        return

    # Проверка на выбор существующего заряда
    for charge in charges:
        x0, y0 = charge["pos"]
        if np.hypot(event.xdata - x0, event.ydata - y0) < 0.1:
            selected_charge = charge
            return

    # Левая кнопка мыши: добавить положительный заряд
    if event.button == 1:
        charges.append({"q": 1e-9, "pos": (event.xdata, event.ydata)})
    # Правая кнопка мыши: добавить отрицательный заряд
    elif event.button == 3:
        charges.append({"q": -1e-9, "pos": (event.xdata, event.ydata)})
    update_plot()


def on_release(event):
    global selected_charge
    selected_charge = None


def on_motion(event):
    if selected_charge is not None and event.inaxes:
        selected_charge["pos"] = (event.xdata, event.ydata)
        update_plot()


def on_scroll(event):
    if event.inaxes is None:
        return
    for charge in charges:
        x0, y0 = charge["pos"]
        if np.hypot(event.xdata - x0, event.ydata - y0) < 0.1:
            charge["q"] += 1e-10 * event.step  # Изменение силы заряда
            update_plot()
            break

# Главная функция
def main():
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('scroll_event', on_scroll)

    update_plot()
    plt.show()

if __name__ == "__main__":
    main()
