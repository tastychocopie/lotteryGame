class Player:
    def __init__(self, name, card, is_bot=False):
        self.name = name
        self.card = card
        self.is_bot = is_bot
        self.marked_numbers = 0
        self.lost = False

    def mark_number(self, number):
        """Пометить число на карточке"""
        for row in self.card.somelist:
            for i, cell in enumerate(row):
                if cell.strip() == str(number):
                    row[i] = ' X'
                    self.marked_numbers += 1
                    return True
        return False

    def has_number(self, number):
        """Проверить, есть ли число на карточке"""
        for row in self.card.somelist:
            for cell in row:
                if cell.strip() == str(number):
                    return True
        return False

    def is_winner(self):
        """Проверить, выиграл ли игрок"""
        return self.marked_numbers == 15

    def __str__(self):
        return f"Player initialized: {self.name}"