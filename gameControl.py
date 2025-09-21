import random


class Game:
    def __init__(self):
        print('\n' + '=' * 50)
        print('Обоим игрокам выдается случайная карточка из чисел, каждый ход выбирается один случайный бочонок (число)')
        print('и выводится на экран, пользователю предлагается зачеркнуть или продолжить.')
        print('! Побеждает тот, кто первый закроет все числа на своей карточке.')
        print('!! Будьте внимательны, если попытаетесь зачеркнуть несуществующее число, или продолжить при')
        print('наличии бочонка, то вы автоматически проигрываете.')
        print('=' * 50 + '\n')

        self.used_numbers = set()
        self.bag = list(range(1, 91))
        random.shuffle(self.bag)

    def pullout_number(self):
        """Достать случайный бочонок"""
        if not self.bag:
            return None

        number = self.bag.pop()
        self.used_numbers.add(number)

        if number < 10:
            unitType = 'Цифра'
        else:
            unitType = 'Число'
        print(f"{unitType} - {number}")
        return number

    def provide_options(self, player, current_number):
        """Предложить варианты действий игроку"""
        if player.is_bot:
            # Небольшая пауза для реалистичности хода бота
            import time
            time.sleep(1)

            # Логика для бота
            if player.has_number(current_number):
                print(f"{player.name} зачеркивает число {current_number}")
                return '1'
            else:
                print(f"{player.name} продолжает игру")
                return '2'
        else:
            print(f'\n{player.name}, что вы хотите сделать?')
            print('1. Зачеркнуть')
            print('2. Продолжить')

            while True:
                choice = input('Выберите пункт: ')
                if choice in ['1', '2']:
                    return choice
                print('Выберите валидный пункт (1 или 2)')

    def check_choice(self, player, choice, current_number):
        """Проверить правильность выбора игрока"""
        has_number = player.has_number(current_number)

        if choice == '1':  # Зачеркнуть
            if has_number:
                player.mark_number(current_number)
                print(f"{player.name} правильно зачеркнул число {current_number}")
                return True
            else:
                print(f"{player.name} пытался зачеркнуть несуществующее число {current_number}!")
                player.lost = True
                return False

        else:  # Продолжить
            if has_number:
                print(f"{player.name} не зачеркнул существующее число {current_number}!")
                player.lost = True
                return False
            else:
                print(f"{player.name} правильно продолжил игру")
                return True

    def display_cards(self, player1, player2):
        """Показать карточки игроков"""
        print(f"\n{player1.name}:")
        print(player1.card)
        print(f"\n{player2.name}:")
        print(player2.card)

    def start_game(self, player1, player2):
        """Начать игру"""
        input("\nНажмите Enter чтобы начать игру...")

        while self.bag and not (player1.lost or player2.lost):
            print('\n' + '=' * 30)
            print(f"Осталось бочонков: {len(self.bag)}")

            # Достаем новый бочонок
            current_number = self.pullout_number()
            if current_number is None:
                break

            # Ход первого игрока
            if not player1.lost:
                choice1 = self.provide_options(player1, current_number)
                if not self.check_choice(player1, choice1, current_number):
                    print(f"{player1.name} проиграл!")
                    break

                if player1.is_winner():
                    print(f"\n🎉 {player1.name} победил!")
                    break

            # Ход второго игрока (только если первый не проиграл и не выиграл)
            if not player1.lost and not player1.is_winner() and not player2.lost:
                choice2 = self.provide_options(player2, current_number)
                if not self.check_choice(player2, choice2, current_number):
                    print(f"{player2.name} проиграл!")
                    break

                if player2.is_winner():
                    print(f"\n🎉 {player2.name} победил!")
                    break

            # Показать текущее состояние карточек
            self.display_cards(player1, player2)

            # Проверяем, не закончилась ли игра
            if player1.is_winner() or player2.is_winner() or player1.lost or player2.lost:
                break

        # Конец игры
        if player1.lost and player2.lost:
            print("\nОба игрока проиграли! Ничья.")
        elif player1.lost:
            print(f"\n{player2.name} победил!")
        elif player2.lost:
            print(f"\n{player1.name} победил!")
        elif player1.is_winner():
            print(f"\n🎉 {player1.name} победил!")
        elif player2.is_winner():
            print(f"\n🎉 {player2.name} победил!")
        elif not self.bag:
            print("\nБочонки закончились! Ничья.")

        print("\nИгра завершена!")