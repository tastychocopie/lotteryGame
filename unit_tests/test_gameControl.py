import pytest
from unittest.mock import patch, MagicMock, call
import random
import sys
from io import StringIO

from gameControl import Game

class MockPlayer:
    def __init__(self, name, is_bot=False, has_numbers=None, will_win_after=999):
        self.name = name
        self.is_bot = is_bot
        self.lost = False
        self.card = MagicMock()
        self.marked_numbers = set()
        self.has_numbers = has_numbers or []
        self.will_win_after = will_win_after
        self.mark_count = 0

    def has_number(self, number):
        return number in self.has_numbers

    def mark_number(self, number):
        self.marked_numbers.add(number)
        self.mark_count += 1

    def is_winner(self):
        return self.mark_count >= self.will_win_after


class TestGame:

    @pytest.fixture
    def game(self):
        return Game()

    @pytest.fixture
    def human_player(self):
        return MockPlayer("Human Player", is_bot=False, has_numbers=[1, 3, 5])

    @pytest.fixture
    def bot_player(self):
        return MockPlayer("Bot Player", is_bot=True, has_numbers=[2, 4, 6])

    @pytest.fixture
    def winning_player(self):
        return MockPlayer("Winner", is_bot=False, has_numbers=[1, 2, 3], will_win_after=3)

    def test_game_initialization(self, game):
        assert len(game.bag) == 90
        assert len(game.used_numbers) == 0
        assert all(num in game.bag for num in range(1, 91))

    def test_pullout_number_normal(self, game):
        initial_bag_size = len(game.bag)
        initial_used_size = len(game.used_numbers)

        number = game.pullout_number()

        assert number is not None
        assert 1 <= number <= 90
        assert len(game.bag) == initial_bag_size - 1
        assert len(game.used_numbers) == initial_used_size + 1
        assert number in game.used_numbers

    def test_pullout_number_empty_bag(self, game):
        game.bag = []
        number = game.pullout_number()

        assert number is None

    @patch('builtins.print')
    def test_pullout_number_output(self, mock_print, game):
        with patch.object(random, 'shuffle'):
            game.bag = [5, 15]
            game.used_numbers = set()

            number1 = game.pullout_number()
            number2 = game.pullout_number()
        assert mock_print.call_count >= 2

    @patch('time.sleep')
    def test_provide_options_bot_has_number(self, mock_sleep, game, bot_player):
        bot_player.has_numbers = [5]
        current_number = 5

        choice = game.provide_options(bot_player, current_number)

        assert choice == '1'
        mock_sleep.assert_called_once()

    @patch('time.sleep')
    def test_provide_options_bot_no_number(self, mock_sleep, game, bot_player):
        bot_player.has_numbers = [1, 2, 3]
        current_number = 5

        choice = game.provide_options(bot_player, current_number)

        assert choice == '2'
        mock_sleep.assert_called_once()

    @patch('builtins.input')
    def test_provide_options_human_valid_choice(self, mock_input, game, human_player):
        mock_input.return_value = '1'
        current_number = 5

        choice = game.provide_options(human_player, current_number)

        assert choice == '1'
        mock_input.assert_called_once()

    @patch('builtins.input')
    def test_provide_options_human_invalid_then_valid(self, mock_input, game, human_player):
        mock_input.side_effect = ['3', 'invalid', '2']
        current_number = 5

        choice = game.provide_options(human_player, current_number)

        assert choice == '2'
        assert mock_input.call_count == 3

    def test_check_choice_correct_mark(self, game, human_player):
        human_player.has_numbers = [5]
        current_number = 5

        result = game.check_choice(human_player, '1', current_number)

        assert result is True
        assert 5 in human_player.marked_numbers
        assert human_player.lost is False

    def test_check_choice_incorrect_mark(self, game, human_player):
        human_player.has_numbers = [1, 2, 3]
        current_number = 5

        result = game.check_choice(human_player, '1', current_number)

        assert result is False
        assert human_player.lost is True

    def test_check_choice_correct_continue(self, game, human_player):
        human_player.has_numbers = [1, 2, 3]
        current_number = 5

        result = game.check_choice(human_player, '2', current_number)

        assert result is True
        assert human_player.lost is False

    def test_check_choice_incorrect_continue(self, game, human_player):
        human_player.has_numbers = [5]
        current_number = 5

        result = game.check_choice(human_player, '2', current_number)

        assert result is False
        assert human_player.lost is True

    @patch('builtins.input')
    def test_start_game_player_loses(self, mock_input, game, human_player, bot_player):
        # Setup - human will make wrong choice
        game.bag = [5]  # Only one number
        human_player.has_numbers = [1, 2, 3]  # Doesn't have 5
        mock_input.return_value = '1'  # Tries to mark number they don't have

        game.start_game(human_player, bot_player)

        assert human_player.lost is True

    @patch('builtins.input')
    def test_start_game_empty_bag(self, mock_input, game, human_player, bot_player):
        game.bag = []
        mock_input.return_value = '1'

        game.start_game(human_player, bot_player)

    def test_bag_shuffling(self, game):
        bags = []
        for _ in range(5):
            test_game = Game()
            bags.append(test_game.bag.copy())
        different_bags = any(bags[i] != bags[j] for i in range(len(bags)) for j in range(i + 1, len(bags)))
        assert different_bags is True

    @patch('random.shuffle')
    def test_bag_initialization(self, mock_shuffle, game):
        test_game = Game()
        mock_shuffle.assert_called_once()

    def test_used_numbers_tracking(self, game):
        numbers_pulled = []
        for _ in range(5):
            num = game.pullout_number()
            if num is not None:
                numbers_pulled.append(num)
        for num in numbers_pulled:
            assert num in game.used_numbers
        assert len(numbers_pulled) == len(set(numbers_pulled))

    @patch('builtins.input')
    def test_game_flow_complete(self, mock_input, game, human_player, bot_player):
        game.bag = [1, 2, 3, 4, 5]
        human_player.has_numbers = [1, 3, 5]
        bot_player.has_numbers = [2, 4, 6]
        mock_input.return_value = '1'

        game.start_game(human_player, bot_player)
        assert True

    def test_edge_case_numbers(self, game):
        for num in range(1, 91):
            assert num in game.bag

class TestNumberOutput:


    @patch('builtins.print')
    def test_single_digit_output(self, mock_print):

        game = Game()
        game.bag = [5]

        with patch('sys.stdout', new_callable=StringIO):
            game.pullout_number()

        assert any("Цифра" in str(call) for call in mock_print.call_args_list)

    @patch('builtins.print')
    def test_double_digit_output(self, mock_print):
        game = Game()
        game.bag = [15]

        with patch('sys.stdout', new_callable=StringIO):
            game.pullout_number()
        assert any("Число" in str(call) for call in mock_print.call_args_list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])