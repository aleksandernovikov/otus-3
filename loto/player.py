import termtables as tt

from loto.card import Card
from loto.exceptions import EndOfTheGame


class Player:
    card = None

    def __init__(self, name, *args, **kwargs):
        self.name = name

    def get_a_card(self, card: Card):
        self.card = card

    def is_number_on_card(self, number: int):
        pass

    def mark_number_on_card(self, number):
        self.card.mark_number(number)
        print(f'{self.name}={len(self.card.found)}')

        if len(self.card.found) == 15:
            raise EndOfTheGame(f'{self.name} победил')


class HumanPlayer(Player):
    answers = {
        'y': True, 'yes': True, 1: True, 'да': True,
        'n': False, 'no': False, 0: False, 'нет': False
    }

    def show_card(self) -> None:
        print(f'Карта игрока {self.name}')
        print(tt.to_string(
            data=self.card.preview(),
            header=[],
            alignment='c',
            style=tt.styles.rounded_double
        ))

    def is_number_on_card(self, number: int) -> bool:
        self.show_card()
        answer = input(f'У вас на карте есть номер {number}? ')
        return self.answers.get(answer, False)


class AIPlayer(Player):
    def is_number_on_card(self, number):
        return number in self.card.numbers
