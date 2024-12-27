import numpy as np


class Circuit:
    def __init__(self):
        self.elements = []
        self.nodes = set()
        self.ground_node = None  # Опорный узел

    def add_resistor(self, node1, node2, resistance):
        self.elements.append({'type': 'resistor', 'node1': node1, 'node2': node2, 'value': resistance})
        self.nodes.update([node1, node2])

    def add_voltage_source(self, node1, node2, voltage):
        self.elements.append({'type': 'voltage_source', 'node1': node1, 'node2': node2, 'value': voltage})
        self.nodes.update([node1, node2])

    def remove_element(self, index):
        if 0 <= index < len(self.elements):
            removed = self.elements.pop(index)
            print(f"Элемент удалён: {removed}")
            self.recalculate_nodes()
        else:
            print("Неверный индекс элемента.")

    def recalculate_nodes(self):
        self.nodes = set()
        for element in self.elements:
            self.nodes.update([element['node1'], element['node2']])

    def set_ground_node(self, ground_node):
        if ground_node in self.nodes:
            self.ground_node = ground_node
            print(f"Опорный узел установлен: {ground_node}")
        else:
            print(f"Ошибка: узел {ground_node} отсутствует в цепи.")

    def solve(self):
        if not self.ground_node:
            raise ValueError("Опорный узел не установлен. Используйте команду 'ground <узел>'.")

        # Список узлов, исключая опорный узел
        nodes = list(self.nodes)
        if self.ground_node in nodes:
            nodes.remove(self.ground_node)
        node_indices = {node: i for i, node in enumerate(nodes)}
        num_nodes = len(nodes)

        # Список источников напряжения
        voltage_sources = [el for el in self.elements if el['type'] == 'voltage_source']
        num_vsources = len(voltage_sources)

        # Размер матрицы: узлы + источники напряжения
        size = num_nodes + num_vsources

        A = np.zeros((size, size))
        B = np.zeros(size)

        # Обработка резисторов
        for element in self.elements:
            if element['type'] == 'resistor':
                node1 = element['node1']
                node2 = element['node2']
                resistance = element['value']
                conductance = 1 / resistance

                if node1 != self.ground_node:
                    i = node_indices[node1]
                    A[i, i] += conductance
                if node2 != self.ground_node:
                    j = node_indices[node2]
                    A[j, j] += conductance
                if node1 != self.ground_node and node2 != self.ground_node:
                    i = node_indices[node1]
                    j = node_indices[node2]
                    A[i, j] -= conductance
                    A[j, i] -= conductance

        # Обработка источников напряжения
        for idx, vs in enumerate(voltage_sources):
            node1 = vs['node1']
            node2 = vs['node2']
            voltage = vs['value']

            # Индекс в матрице
            vs_index = num_nodes + idx

            # Добавляем уравнение для источника напряжения
            if node1 != self.ground_node:
                i = node_indices[node1]
                A[i, vs_index] += 1
                A[vs_index, i] += 1
            if node2 != self.ground_node:
                j = node_indices[node2]
                A[j, vs_index] -= 1
                A[vs_index, j] -= 1

            # Вектор источников
            B[vs_index] = voltage

        # Решение системы уравнений
        try:
            solution = np.linalg.solve(A, B)
            potentials = {}

            # Получение потенциалов узлов
            for node in nodes:
                potentials[node] = solution[node_indices[node]]

            potentials[self.ground_node] = 0.0  # Опорный узел

            # Получение токов через элементы
            currents = []
            for element in self.elements:
                if element['type'] == 'resistor':
                    node1_potential = potentials[element['node1']]
                    node2_potential = potentials[element['node2']]
                    current = (node1_potential - node2_potential) / element['value']
                    currents.append({
                        'type': 'resistor',
                        'nodes': (element['node1'], element['node2']),
                        'current': current
                    })
                elif element['type'] == 'voltage_source':
                    # Ток через источник напряжения
                    vs_idx = voltage_sources.index(element)
                    current = solution[num_nodes + vs_idx]
                    currents.append({
                        'type': 'voltage_source',
                        'nodes': (element['node1'], element['node2']),
                        'current': current
                    })

            return potentials, currents

        except np.linalg.LinAlgError:
            raise ValueError("Цепь не может быть решена (сингулярная матрица).")

    def print_circuit(self):
        for i, element in enumerate(self.elements):
            if element['type'] == 'resistor':
                print(f"[{i}] Резистор: {element['value']} Ω между {element['node1']} и {element['node2']}")
            elif element['type'] == 'voltage_source':
                print(f"[{i}] Источник напряжения: {element['value']} В между {element['node1']} и {element['node2']}")


def main():
    circuit = Circuit()

    print("Добро пожаловать в Конструктор Цепей!")
    print("Команды:")
    print("  resistor <узел1> <узел2> <сопротивление>: Добавить резистор")
    print("  voltage <узел1> <узел2> <напряжение>: Добавить источник напряжения")
    print("  remove <индекс>: Удалить элемент по индексу")
    print("  ground <узел>: Установить опорный узел")
    print("  solve: Решить цепь")
    print("  show: Показать текущую конфигурацию цепи")
    print("  exit: Выйти из программы")

    while True:
        command = input("Введите команду: ").strip().lower()
        if command.startswith("resistor"):
            parts = command.split()
            if len(parts) != 4:
                print("Ошибка: неверный формат команды. Пример: resistor A B 100")
                continue
            _, node1, node2, resistance = parts
            try:
                resistance = float(resistance)
                circuit.add_resistor(node1, node2, resistance)
            except ValueError:
                print("Ошибка: сопротивление должно быть числом.")
        elif command.startswith("voltage"):
            parts = command.split()
            if len(parts) != 4:
                print("Ошибка: неверный формат команды. Пример: voltage A B 5")
                continue
            _, node1, node2, voltage = parts
            try:
                voltage = float(voltage)
                circuit.add_voltage_source(node1, node2, voltage)
            except ValueError:
                print("Ошибка: напряжение должно быть числом.")
        elif command.startswith("remove"):
            parts = command.split()
            if len(parts) != 2:
                print("Ошибка: неверный формат команды. Пример: remove 0")
                continue
            try:
                _, index = parts
                index = int(index)
                circuit.remove_element(index)
            except ValueError:
                print("Ошибка: индекс должен быть целым числом.")
        elif command.startswith("ground"):
            parts = command.split()
            if len(parts) != 2:
                print("Ошибка: неверный формат команды. Пример: ground A")
                continue
            _, ground_node = parts
            circuit.set_ground_node(ground_node)
        elif command == "solve":
            try:
                potentials, currents = circuit.solve()
                print("\nПотенциалы узлов:")
                for node, potential in potentials.items():
                    print(f"{node}: {potential:.2f} В")

                print("\nТоки в элементах:")
                for current in currents:
                    print(
                        f"{current['type'].capitalize()} между {current['nodes'][0]} и {current['nodes'][1]}: {current['current']:.2f} А")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif command == "show":
            circuit.print_circuit()
        elif command == "exit":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()