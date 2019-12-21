import termtables as tt

from log import loto_logger
from loto.card import Card
from loto.exceptions import EndOfTheGame


class Player:
    """
    Базовый класс игрока, который нужно наследовать
    """
    card: Card = None

    def __init__(self, name: str, *args, **kwargs) -> None:
        """
        Инициализируем класс с заданным именем игрока
        :param name: имя
        :param args:
        :param kwargs:
        """
        self.name = name

    def get_a_card(self, card: Card) -> None:
        """
        Получение карточки игроком
        :param card: карта выданная ведущим
        """
        self.card = card

    def is_number_on_card(self, number: int):
        """
        Метод который нужно будет переопределить в наследниках
        Определяет есть ли номер на карточке
        :param number: номер
        """
        pass

    def mark_number_on_card(self, number: int) -> None:
        """
        Номер на карте помечается как найденный
        :param number: номер на бочонке
        """
        self.card.mark_number(number)
        print(f'{self.name}={len(self.card.found)}')

        if len(self.card.found) == 15:
            raise EndOfTheGame(f'{self.name} победил')


class HumanPlayer(Player):
    """
    Дочерний класс игрока
    """
    # возможные ответы игрока и результат
    answers: dict = {
        'y': True, 'yes': True, 1: True, 'да': True,
        'n': False, 'no': False, 0: False, 'нет': False
    }

    def show_card(self) -> None:
        """
        Вывод карты в консоль
        :return:
        """
        print(f'Карта игрока {self.name}')
        print(tt.to_string(
            data=self.card.preview(),
            header=[],
            alignment='c',
            style=tt.styles.rounded_double
        ))

    def is_number_on_card(self, number: int) -> bool:
        """
        Проверка есть ли номер на карте
        :param number: номер
        :return: результат ответа True или False
        """
        self.show_card()
        answer = input(f'У вас на карте есть номер {number}? ')
        result = self.answers.get(answer, False)
        loto_logger.debug('Игрок {} говорит что у него {} {}'.format(self.name, number, 'есть' if result else 'нет'))

        return result


class AIPlayer(Player):
    """
    Вариант компьютерного игрока
    """

    def is_number_on_card(self, number):
        """
        Проверка есть ли номер на карте
        безхитростно говорит правду
        :param number:
        :return: результат ответа True или False
        """
        result = number in self.card.numbers
        loto_logger.debug('Игрок {} говорит что у него {} {}'.format(self.name, number, 'есть' if result else 'нет'))
        return result
