import random

class Card:

    # отбор уникальных случайных чисел
    def __init__(self):
        numbers = random.sample(range(1, 90),15)  # 15 чисел тк 3 строки из 9 клеток, где в каждой строке 5 заполненных - 15 чисел
        # создаем 3 списка из 9 пустых клеток
        for row in range(3):
            """
            somelist = []
somelist.append(list(range(1, 10)))
somelist.append(list(range(1,10)))
somelist.append(list(range(1,10)))
print(somelist)
for row in somelist:
    print(row)
            """