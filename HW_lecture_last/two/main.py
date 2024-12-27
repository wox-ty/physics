# Программа для расчета параметров плоского конденсатора

def get_dielectric_constant():
    dielectrics = {
        'вакуум': 1.0,
        'воздух': 1.0006,
        'полиэтилен': 2.3,
        'пластик': 3.0,
        'стекло': 5.0,
        'вода': 80.0
        # Добавьте другие материалы по необходимости
    }
    print("\nДоступные диэлектрики и их относительные диэлектрические проницаемости (εr):")
    for material, er in dielectrics.items():
        print(f"- {material}: {er}")
    while True:
        dielectric = input("Введите название диэлектрика из списка: ").strip().lower()
        if dielectric in dielectrics:
            return dielectrics[dielectric]
        else:
            print("Неверный ввод. Пожалуйста, выберите диэлектрик из списка.")


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Значение должно быть положительным.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числовое значение.")


def main():
    print("Расчет параметров плоского конденсатора")

    print("\nВыберите состояние конденсатора:")
    print("1. Подключён к источнику питания")
    print("2. Отключён от источника питания")
    while True:
        state = input("Введите 1 или 2: ").strip()
        if state == '1':
            connected = True
            break
        elif state == '2':
            connected = False
            break
        else:
            print("Неверный ввод. Пожалуйста, введите 1 или 2.")

    if connected:
        print("\nВведите параметры для подключённого конденсатора:")
        V = get_positive_float("Введите напряжение между пластинами (В): ")
    else:
        print("\nВведите параметры для отключённого конденсатора:")
        Q = get_positive_float("Введите заряд на пластинах (Кл): ")

    d = get_positive_float("Введите расстояние между пластинами (м): ")
    A = get_positive_float("Введите площадь пластин (м²): ")
    epsilon_r = get_dielectric_constant()

    # Электрическая постоянная (Ф/м)
    epsilon_0 = 8.854187817e-12

    # Емкость конденсатора
    C = epsilon_0 * epsilon_r * A / d  # в Фарадах

    if connected:
        # Если подключён, напряжение постоянное, заряд зависит от емкости
        Q = C * V  # Кулоны
        E = V / d  # В/м
        print("\nПараметры подключённого конденсатора:")
        print(f"Емкость (C): {C:.3e} Ф")
        print(f"Напряжённость электрического поля (E): {E:.2e} В/м")
        print(f"Заряд на пластинах (Q): {Q:.3e} Кл")
    else:
        # Если отключён, заряд постоянный, напряжение зависит от емкости
        V = Q / C  # Вольты
        E = V / d  # В/м
        print("\nПараметры отключённого конденсатора:")
        print(f"Емкость (C): {C:.3e} Ф")
        print(f"Напряжённость электрического поля (E): {E:.2e} В/м")
        print(f"Напряжение между пластинами (V): {V:.2f} В")


if __name__ == "__main__":
    main()
