import sys
import numpy as np
import matplotlib
from PyQt5.QtCore import QLocale

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QDoubleValidator
from matplotlib.lines import Line2D


class EMFieldPlot(FigureCanvas):
    def __init__(self, parent=None):
        self.epsilon1 = None
        self.epsilon2 = None
        self.E0 = None
        self.theta_deg = None
        self.limit_x = None
        self.limit_y = None
        self.is_panning = False
        self.press = None
        self.full_reflection = False
        self.current_plot_type = 'E'  # По умолчанию график E
        self.fig = Figure()
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        self.fig.tight_layout()
        self.mpl_connect('scroll_event', self.zoom)
        self.mpl_connect('button_press_event', self.on_press)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('motion_notify_event', self.on_move)

    def on_press(self, event):
        """Обрабатывает нажатие кнопки мыши"""
        if event.button == 1:  # ЛКМ
            self.is_panning = True
            self.press = (event.xdata, event.ydata)

    def on_release(self, event):
        """Обрабатывает отпускание кнопки мыши"""
        if event.button == 1:  # ЛКМ
            self.is_panning = False
            self.press = None

    def on_move(self, event):
        """Обрабатывает движение мыши, если панорамирование активно"""
        if self.is_panning:
            dx = event.xdata - self.press[0]
            dy = event.ydata - self.press[1]
            self.ax.set_xlim(self.ax.get_xlim() - dx)
            self.ax.set_ylim(self.ax.get_ylim() - dy)
            self.draw()
            self.press = (event.xdata, event.ydata)

    def zoom(self, event):
        """Обработчик события прокрутки мыши для изменения масштаба."""
        scale_factor = 1.1
        if event.button == 'up':
            self.ax.set_xlim(self.ax.get_xlim()[0] / scale_factor, self.ax.get_xlim()[1] / scale_factor)
            self.ax.set_ylim(self.ax.get_ylim()[0] / scale_factor, self.ax.get_ylim()[1] / scale_factor)
        elif event.button == 'down':
            self.ax.set_xlim(self.ax.get_xlim()[0] * scale_factor, self.ax.get_xlim()[1] * scale_factor)
            self.ax.set_ylim(self.ax.get_ylim()[0] * scale_factor, self.ax.get_ylim()[1] * scale_factor)
        self.draw()

    def compute_fields(self):
        if None in (self.epsilon1, self.epsilon2, self.E0, self.theta_deg, self.limit_x, self.limit_y):
            return
        self.x = np.linspace(-self.limit_x, self.limit_x, 400)
        self.y = np.linspace(-self.limit_y, self.limit_y, 400)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        alpha = np.deg2rad(self.theta_deg)
        n1 = np.sqrt(self.epsilon1)
        n2 = np.sqrt(self.epsilon2)
        sin_val = n1 * np.sin(alpha) / n2
        if abs(sin_val) <= 1:
            self.full_reflection = False
            alpha2 = np.arcsin(sin_val)
            Ex2 = self.E0 * np.cos(alpha2)
            Ey2 = self.E0 * np.sin(alpha2)
        else:
            self.full_reflection = True
            Ex2 = 0.0
            Ey2 = 0.0
        Ex1 = self.E0 * np.cos(alpha)
        Ey1 = self.E0 * np.sin(alpha)
        D1x = self.epsilon1 * Ex1
        D1y = self.epsilon1 * Ey1
        D2x = self.epsilon2 * Ex2
        D2y = self.epsilon2 * Ey2
        Ex_bottom = Ex1
        Ey_bottom = Ey1
        Dx_bottom = D1x
        Dy_bottom = D1y
        Ex_top = Ex2
        Ey_top = Ey2
        Dx_top = D2x
        Dy_top = D2y
        self.Ex = np.where(self.Y >= 0, Ex_top, Ex_bottom)
        self.Ey = np.where(self.Y >= 0, Ey_top, Ey_bottom)
        self.Dx = np.where(self.Y >= 0, Dx_top, Dx_bottom)
        self.Dy = np.where(self.Y >= 0, Dy_top, Dy_bottom)

    def calculate_refraction_angles(self):
        """
        Рассчитывает угол преломления для двух диэлектриков, используя закон Снеллиуса.
        Возвращает угол преломления в градусах, если возможен, иначе None (полное внутреннее отражение).
        """
        theta_inc = np.radians(self.theta_deg)
        sin_theta_ref = np.sqrt(self.epsilon1) * np.sin(theta_inc) / np.sqrt(self.epsilon2)

        # Проверяем на полное внутреннее отражение
        if abs(sin_theta_ref) > 1:
            return None
        else:
            theta_ref = np.arcsin(sin_theta_ref)
            return np.degrees(theta_ref)

    def plot_refraction_lines(self):
        """Рисует линии преломления."""
        theta_ref_deg = self.calculate_refraction_angles()

        # Если полное внутреннее отражение
        if theta_ref_deg is None:
            print(f"Полное внутреннее отражение для угла падения: {self.theta_deg}")
            return

        theta_inc = np.radians(self.theta_deg)
        theta_ref = np.radians(theta_ref_deg)

        # Генерация линий поля
        x_inc = np.linspace(-5, 0, 10)  # Падающее поле
        y_inc = np.tan(theta_inc) * x_inc

        x_ref = np.linspace(0, 5, 10)  # Преломлённое поле
        y_ref = np.tan(theta_ref) * x_ref

        self.ax.plot(x_inc, y_inc, 'b--', label='Падающее поле')
        self.ax.plot(x_ref, y_ref, 'r-', label='Преломлённое поле')

    def plot_fields(self):
        if None in (self.epsilon1, self.epsilon2, self.E0, self.theta_deg, self.limit_x, self.limit_y):
            self.ax.clear()
            self.ax.set_xlim(-10, 10)
            self.ax.set_ylim(-10, 10)
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_title('Граничные условия двух диэлектриков')
            self.draw()
            return
        self.ax.clear()
        self.ax.fill_between(self.x, 0, self.limit_y, color='lightgray', alpha=0.5, label='ε₂')
        self.ax.fill_between(self.x, -self.limit_y, 0, color='white', alpha=0.5, label='ε₁')
        self.ax.axhline(0, color='k', linewidth=2)

        if self.current_plot_type == 'E':  # График для напряженности E
            density = 1.5
            self.ax.streamplot(self.X, self.Y, self.Ex, self.Ey, color='blue', linewidth=1, density=density,
                               arrowsize=1)
            self.ax.legend(['Линии напряженности E'])
        elif self.current_plot_type == 'D':  # График для смещения D
            density = 1.5
            self.ax.streamplot(self.X, self.Y, self.Dx, self.Dy, color='red', linewidth=1, density=density, arrowsize=1)
            self.ax.legend(['Линии смещения D'])
        elif self.current_plot_type == 'Combined':  # Комбинированный график
            density = 1.5
            self.ax.streamplot(self.X, self.Y, self.Ex, self.Ey, color='blue', linewidth=1, density=density,
                               arrowsize=1)
            self.ax.streamplot(self.X, self.Y, self.Dx, self.Dy, color='red', linewidth=1, density=density, arrowsize=1)
            custom_lines = [Line2D([0], [0], color='blue', lw=2), Line2D([0], [0], color='red', lw=2)]
            self.ax.legend(custom_lines, ['Напряженность E', 'Смещение D'])
        elif self.current_plot_type == 'Refraction':  # Новый график для преломления
            self.plot_refraction_lines()  # Рисуем линии преломления
            self.ax.set_title("Преломление линий напряженности и смещения на границе диэлектриков")

        self.ax.set_xlim(-self.limit_x, self.limit_x)
        self.ax.set_ylim(-self.limit_y, self.limit_y)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title(f'График: {self.current_plot_type}')
        self.draw()

    def set_plot_type(self, plot_type):
        self.current_plot_type = plot_type
        self.plot_fields()

    def update_parameters(self, epsilon1, epsilon2, E0, theta_deg, limit_x, limit_y):
        self.epsilon1 = epsilon1
        self.epsilon2 = epsilon2
        self.E0 = E0
        self.theta_deg = theta_deg
        self.limit_x = limit_x
        self.limit_y = limit_y
        self.compute_fields()
        self.plot_fields()


# Остальная часть кода для интерфейса (виджеты, окна и т. д.) будет оставаться той же.


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Визуализация граничных условий двух диэлектриков')
        self.setGeometry(100, 100, 1200, 800)
        w = QWidget()
        self.setCentralWidget(w)
        v = QVBoxLayout()
        w.setLayout(v)
        self.plot = EMFieldPlot(self)
        v.addWidget(self.plot)
        l1 = QHBoxLayout()
        dv = QDoubleValidator(bottom=0.0)
        dv.setLocale(QLocale(QLocale.C))
        l1.addWidget(QLabel('ε₁:'))
        self.eps1_input = QLineEdit()
        self.eps1_input.setValidator(dv)
        l1.addWidget(self.eps1_input)
        l1.addWidget(QLabel('ε₂:'))
        self.eps2_input = QLineEdit()
        self.eps2_input.setValidator(dv)
        l1.addWidget(self.eps2_input)
        l1.addWidget(QLabel('E₀:'))
        self.E0_input = QLineEdit()
        self.E0_input.setValidator(dv)
        l1.addWidget(self.E0_input)
        l1.addWidget(QLabel('θ (градусы):'))
        self.theta_input = QLineEdit()
        self.theta_input.setValidator(QDoubleValidator(0.0, 90.0, 2))
        l1.addWidget(self.theta_input)
        v.addLayout(l1)
        l2 = QHBoxLayout()
        l2.addWidget(QLabel('Лимит X:'))
        self.limit_x_input = QLineEdit()
        self.limit_x_input.setValidator(dv)
        l2.addWidget(self.limit_x_input)
        l2.addWidget(QLabel('Лимит Y:'))
        self.limit_y_input = QLineEdit()
        self.limit_y_input.setValidator(dv)
        l2.addWidget(self.limit_y_input)
        self.update_button = QPushButton('Обновить')
        self.update_button.clicked.connect(self.update_plot)
        l2.addWidget(self.update_button)
        v.addLayout(l2)

        # Кнопки для переключения графиков
        l3 = QHBoxLayout()
        self.e_button = QPushButton('График E')
        self.e_button.clicked.connect(lambda: self.plot.set_plot_type('E'))
        l3.addWidget(self.e_button)

        self.d_button = QPushButton('График D')
        self.d_button.clicked.connect(lambda: self.plot.set_plot_type('D'))
        l3.addWidget(self.d_button)

        self.combined_button = QPushButton('Комбинированный')
        self.combined_button.clicked.connect(lambda: self.plot.set_plot_type('Combined'))
        l3.addWidget(self.combined_button)

        self.refraction_button = QPushButton('Преломление')
        self.refraction_button.clicked.connect(lambda: self.plot.set_plot_type('Refraction'))
        l3.addWidget(self.refraction_button)

        v.addLayout(l3)

        self.limit_x_input.setText('10')
        self.limit_y_input.setText('10')

    def update_plot(self):
        try:
            epsilon1 = float(self.eps1_input.text())
            epsilon2 = float(self.eps2_input.text())
            E0 = float(self.E0_input.text())
            theta_deg = float(self.theta_input.text())
            limit_x = float(self.limit_x_input.text())
            limit_y = float(self.limit_y_input.text())
            if epsilon1 <= 0 or epsilon2 <= 0 or E0 <= 0 or limit_x <= 0 or limit_y <= 0:
                raise ValueError
            if not (0 <= theta_deg <= 90):
                raise ValueError
            self.plot.update_parameters(epsilon1, epsilon2, E0, theta_deg, limit_x, limit_y)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Некорректные значения параметров!')


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
