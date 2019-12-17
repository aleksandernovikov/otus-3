from random import shuffle, randrange

from loto.card import Card
from .exceptions import NoCardError, NoBarrelError, EndOfTheGame


class Base:
    numbers = [i for i in range(1, 91)]

    def __init__(self):
        shuffle(self.numbers)


class Bag(Base):
    """
    Мешок с бочонками
    """

    def get_barrel(self):
        try:
            return self.numbers.pop()
        except IndexError as e:
            raise NoBarrelError from e


class CardStack(Base):
    """
    Колода карточек для лото
    """

    def get_card(self) -> Card:
        """
        Получить карту из стопки
        :return:
        """
        if self.numbers:
            draft = [randrange(1, 10) for d in range(15)]
            card = Card(draft)
            # self.numbers = list(set(self.numbers) - set(card.used_numbers()))
            # shuffle(self.numbers)
            return card
        raise NoCardError
