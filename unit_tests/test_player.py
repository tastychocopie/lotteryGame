import pytest
from cardGenerator import Card
from player import Player

# в терминале "python -m pytest --cov ." для запуска всех тестов с coverage
class TestPlayer:
    """Тесты для класса Player"""

    @pytest.fixture
    def sample_card(self):
        """Фикстура для создания тестовой карточки"""
        # Создаем mock карточки с известными числами
        card = Card()
        # Переопределяем somelist для тестовых данных
        card.somelist = [
            [' 1', '  ', ' 3', '  ', ' 5', '  ', '  ', ' 8', '  '],
            ['  ', '11', '  ', '13', '  ', '  ', '16', '  ', '18'],
            ['  ', '  ', '23', '  ', '25', '  ', '  ', '28', '  ']
        ]
        return card

    @pytest.fixture
    def test_player(self, sample_card):
        """Фикстура для создания тестового игрока"""
        return Player("TestPlayer", sample_card)

    @pytest.fixture
    def test_bot(self, sample_card):
        """Фикстура для создания тестового бота"""
        return Player("TestBot", sample_card, is_bot=True)

    def test_player_initialization(self, test_player, sample_card):
        """Тест инициализации игрока"""
        assert test_player.name == "TestPlayer"
        assert test_player.card == sample_card
        assert test_player.is_bot == False
        assert test_player.marked_numbers == 0
        assert test_player.lost == False

    def test_player_mark_number_true(self, test_player, sample_card):
        result = test_player.mark_number(1)
        assert result == True

    def test_player_mark_number_false(self, test_player, sample_card):
        result = test_player.mark_number(0)
        assert result == False

    def test_player_has_number_true(self, test_player, sample_card):
        result = test_player.has_number(1)
        assert result == True

    def test_player_has_number_false(self, test_player, sample_card):
        result = test_player.has_number(0)
        assert result == False

    def test_is_winner_true(self, test_player, sample_card):
        test_player.marked_numbers = 15
        result = test_player.is_winner()
        assert result == True

    def test_is_winner_false(self, test_player, sample_card):
        # По умолчанию marked_numbers = 0
        result = test_player.is_winner()
        assert result == False

    def test_check_magic_method(self, test_player):
        # Тестируем магический метод __str__
        assert str(test_player) == "Player initialized: TestPlayer"