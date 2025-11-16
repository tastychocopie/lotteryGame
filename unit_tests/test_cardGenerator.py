import pytest
from cardGenerator import Card  # Импортируем класс Card


@pytest.fixture
def card():
    """Фикстура для создания экземпляра карточки"""
    return Card()


def test_card_has_three_rows(card):
    """Тест: карточка имеет 3 строки"""
    assert len(card.somelist) == 3


def test_each_row_has_nine_cells(card):
    """Тест: каждая строка имеет 9 клеток"""
    for row in card.somelist:
        assert len(row) == 9


def test_each_row_has_five_numbers(card):
    """Тест: в каждой строке ровно 5 чисел"""
    for row in card.somelist:
        # Считаем непустые клетки (числа)
        numbers_count = sum(1 for cell in row if cell.strip())
        assert numbers_count == 5


def test_card_has_fifteen_unique_numbers(card):
    """Тест: всего в карточке 15 уникальных чисел от 1 до 90"""
    # Собираем все числа из карточки
    all_numbers = []
    for row in card.somelist:
        for cell in row:
            if cell.strip():  # Если клетка не пустая
                all_numbers.append(int(cell))

    # Проверяем количество чисел
    assert len(all_numbers) == 15

    # Проверяем, что числа в правильном диапазоне
    for number in all_numbers:
        assert 1 <= number <= 90

    # Проверяем уникальность
    assert len(set(all_numbers)) == 15


def test_card_string_representation(card):
    """Тест: проверяем строковое представление карточки"""
    card_str = str(card)

    # Проверяем, что вывод содержит разделители
    assert '--------------------------' in card_str

    # Проверяем, что вывод содержит все строки
    lines = card_str.strip().split('\n')
    assert len(lines) == 5  # 3 строки + 2 разделителя

    # Проверяем, что числа присутствуют в выводе
    assert any(cell.strip() in card_str for row in card.somelist for cell in row if cell.strip())


def test_card_numbers_are_sorted():
    """Тест: числа в карточке отсортированы по возрастанию"""
    card = Card()

    # Собираем все числа из карточки
    all_numbers = []
    for row in card.somelist:
        for cell in row:
            if cell.strip():
                all_numbers.append(int(cell))

    # Проверяем, что числа отсортированы
    assert all_numbers == sorted(all_numbers)


def test_card_empty_cells_are_spaces(card):
    """Тест: пустые клетки содержат два пробела"""
    for row in card.somelist:
        for cell in row:
            if not cell.strip():  # Если клетка пустая
                assert cell == '  '


def test_card_numbers_are_formatted(card):
    """Тест: числа правильно отформатированы (выравнивание)"""
    for row in card.somelist:
        for cell in row:
            if cell.strip():  # Если клетка содержит число
                number = int(cell)
                # Проверяем, что число занимает 2 символа
                assert len(cell) == 2
                # Проверяем выравнивание
                if number < 10:
                    assert cell == f' {number}'
                else:
                    assert cell == str(number)