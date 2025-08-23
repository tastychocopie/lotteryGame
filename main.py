from cardGenerator import Card

"""
Программа использует match-case, что работает только с python 3.10+
Базовые требования для запуска - python 3.10+
"""

# Начало игры
print('Loto!')

# Меню игры
while True:
    print('1. Играть с компьютером')
    print('2. Играть с другом')
    print('3. Выход')

    # выбор пользователя
    choice = input('Выберите пункт: ')

    match choice:
        case '1':
            print("Запуск игры с компьютером...")
            print("\nВаша карточка: ")
            playerCard = Card()
            print(playerCard)

            print("\nКарточка бота: ")
            botCard = Card()
            print(botCard)

        case '2':
            # game start с другом
            print("Запуск игры с другом...")
            print("\nКарточка игрока 1: ")
            player1Card = Card()
            print(player1Card)

            print("\nКарточка игрока 2: ")
            player2Card = Card()
            print(player2Card)

        case '3':
            print("Выход из игры...")
            break

        case _:
            print('Выберите валидный пункт')