import math
from decimal import Decimal, getcontext


# Преобразование из декартовых координат в полярные (2D)
def cartesian_to_polar(x, y):
    r = Decimal(x).sqrt() ** 2 + Decimal(y) ** 2
    theta = Decimal(math.atan2(y, x))
    return r.sqrt(), Decimal(math.degrees(theta))


# Преобразование из полярных координат в декартовые (2D)
def polar_to_cartesian(r, theta_deg):
    theta_rad = Decimal(math.radians(theta_deg))
    x = Decimal(r) * Decimal(math.cos(theta_rad))
    y = Decimal(r) * Decimal(math.sin(theta_rad))
    return x, y


# Преобразование из декартовых координат в цилиндрические (3D)
def cartesian_to_cylindrical(x, y, z):
    r, theta = cartesian_to_polar(x, y)
    return r, theta, Decimal(z)


# Преобразование из цилиндрических координат в декартовые (3D)
def cylindrical_to_cartesian(r, theta_deg, z):
    x, y = polar_to_cartesian(Decimal(r), Decimal(theta_deg))
    return x, y, Decimal(z)


# Преобразование из декартовых координат в сферические (3D)
def cartesian_to_spherical(x, y, z):
    rho = (Decimal(x) ** 2 + Decimal(y) ** 2 + Decimal(z) ** 2).sqrt()
    theta = Decimal(math.atan2(y, x))
    phi = Decimal(math.acos(Decimal(z) / rho))
    return rho, Decimal(math.degrees(theta)), Decimal(math.degrees(phi))


# Преобразование из сферических координат в декартовые (3D)
def spherical_to_cartesian(rho, theta_deg, phi_deg):
    theta_rad = Decimal(math.radians(theta_deg))
    phi_rad = Decimal(math.radians(phi_deg))
    x = Decimal(rho) * Decimal(math.sin(phi_rad)) * Decimal(math.cos(theta_rad))
    y = Decimal(rho) * Decimal(math.sin(phi_rad)) * Decimal(math.sin(theta_rad))
    z = Decimal(rho) * Decimal(math.cos(phi_rad))
    return x, y, z


# Функция для вывода справочной информации
def print_help():
    print("""
Добро пожаловать в программу преобразования координат!

Доступные типы преобразований:
  - cartesian_to_polar: Преобразование из декартовой системы координат в полярную (2D).
  - polar_to_cartesian: Преобразование из полярной системы координат в декартовую (2D).
  - cartesian_to_cylindrical: Преобразование из декартовой системы координат в цилиндрическую (3D).
  - cylindrical_to_cartesian: Преобразование из цилиндрической системы координат в декартовую (3D).
  - cartesian_to_spherical: Преобразование из декартовой системы координат в сферическую (3D).
  - spherical_to_cartesian: Преобразование из сферической системы координат в декартовую (3D).

Использование:
  1. Введите тип преобразования.
  2. Введите требуемую точность (количество знаков после запятой).
  3. Введите необходимые координаты в зависимости от выбранного преобразования.

Пример:
  - Для преобразования из декартовых в полярные (x = 3, y = 4) с точностью до 2 знаков после запятой:
    Ввод: cartesian_to_polar
          2
          3
          4
    Вывод: Полярные координаты: r = 5.00, θ = 53.13 градусов

Чтобы завершить программу, введите 'exit'.
Чтобы вывести эту справочную информацию, введите 'help'.
    """)


def main():
    while True:
        # Запрашиваем тип преобразования
        conversion_type = input("Введите тип преобразования (или 'help' для справки, 'exit' для выхода): ").strip()

        if conversion_type == "exit":
            print("Завершение работы программы.")
            break
        elif conversion_type == "help":
            print_help()
            continue

        # Запрашиваем точность вычислений
        precision = int(input("Введите точность (количество знаков после запятой): ").strip())
        getcontext().prec = precision + 2  # Set precision a little higher for internal calculations

        # Запрашиваем необходимые координаты в зависимости от типа преобразования
        if conversion_type == "cartesian_to_polar":
            x = Decimal(input("Введите координату X: ").strip())
            y = Decimal(input("Введите координату Y: ").strip())
            r, theta = cartesian_to_polar(x, y)
            print(f"Полярные координаты: r = {r:.{precision}f}, θ = {theta:.{precision}f} градусов")

        elif conversion_type == "polar_to_cartesian":
            r = Decimal(input("Введите радиус r: ").strip())
            theta = Decimal(input("Введите угол θ (в градусах): ").strip())
            x, y = polar_to_cartesian(r, theta)
            print(f"Декартовы координаты: x = {x:.{precision}f}, y = {y:.{precision}f}")

        elif conversion_type == "cartesian_to_cylindrical":
            x = Decimal(input("Введите координату X: ").strip())
            y = Decimal(input("Введите координату Y: ").strip())
            z = Decimal(input("Введите координату Z: ").strip())
            r, theta, z_new = cartesian_to_cylindrical(x, y, z)
            print(
                f"Цилиндрические координаты: r = {r:.{precision}f}, θ = {theta:.{precision}f} градусов, z = {z_new:.{precision}f}")

        elif conversion_type == "cylindrical_to_cartesian":
            r = Decimal(input("Введите радиус r: ").strip())
            theta = Decimal(input("Введите угол θ (в градусах): ").strip())
            z = Decimal(input("Введите координату Z: ").strip())
            x, y, z_new = cylindrical_to_cartesian(r, theta, z)
            print(f"Декартовы координаты: x = {x:.{precision}f}, y = {y:.{precision}f}, z = {z_new:.{precision}f}")

        elif conversion_type == "cartesian_to_spherical":
            x = Decimal(input("Введите координату X: ").strip())
            y = Decimal(input("Введите координату Y: ").strip())
            z = Decimal(input("Введите координату Z: ").strip())
            rho, theta, phi = cartesian_to_spherical(x, y, z)
            print(
                f"Сферические координаты: ρ = {rho:.{precision}f}, θ = {theta:.{precision}f} градусов, φ = {phi:.{precision}f} градусов")

        elif conversion_type == "spherical_to_cartesian":
            rho = Decimal(input("Введите радиус ρ: ").strip())
            theta = Decimal(input("Введите угол θ (в градусах): ").strip())
            phi = Decimal(input("Введите угол φ (в градусах): ").strip())
            x, y, z = spherical_to_cartesian(rho, theta, phi)
            print(f"Декартовы координаты: x = {x:.{precision}f}, y = {y:.{precision}f}, z = {z:.{precision}f}")

        else:
            print("Неверный тип преобразования. Попробуйте снова или введите 'help' для справки.")


if __name__ == "__main__":
    main()
