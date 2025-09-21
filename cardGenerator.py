import random

class Card:
    def __init__(self):
        # 15 уникальных чисел
        numbers = random.sample(range(1, 91), 15)
        numbers.sort()  # Сортируем числа по возрастанию

        # Создаем 3 строки с 9 клетками каждая
        self.somelist = []
        numbers_index = 0

        for row in range(3):
            # Создаем строку из 9 пустых клеток
            row_cells = ['  '] * 9

            # Выбираем 5 случайных позиций для заполнения
            filled_positions = random.sample(range(9), 5)
            filled_positions.sort()

            # Заполняем выбранные позиции числами (уже отсортированными)
            for pos in filled_positions:
                row_cells[pos] = str(numbers[numbers_index]).rjust(2)
                numbers_index += 1

            # Добавляем строку в карточку
            self.somelist.append(row_cells)

    def __str__(self):
        # Форматируем карточку для вывода
        result = '-' * 26 + '\n'
        for row in self.somelist:
            result += ' '.join(row) + '\n'
        result += '-' * 26
        return result