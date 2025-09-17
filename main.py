from cardGenerator import Card
from gameControl import Game
from player import Player

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
            game = Game()

            print("\nВаша карточка: ")
            playerCard = Card()
            player = Player("Игрок", playerCard)
            print(playerCard)

            print("\nКарточка бота: ")
            botCard = Card()
            bot = Player("Бот", botCard, is_bot=True)
            print(botCard)

            game.start_game(player, bot)

        case '2':
            print("Запуск игры с другом...")
            game = Game()

            print("\nКарточка игрока 1: ")
            player1Card = Card()
            player1 = Player("Игрок 1", player1Card)
            print(player1Card)

            print("\nКарточка игрока 2: ")
            player2Card = Card()
            player2 = Player("Игрок 2", player2Card)
            print(player2Card)

            game.start_game(player1, player2)

        case '3':
            print("Выход из игры...")
            break

        case _:
            print('Выберите валидный пункт')