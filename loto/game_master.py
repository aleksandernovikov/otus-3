from random import shuffle

from loto.card import Card
from loto.exceptions import NoBarrelError, EndOfTheGame


class Bag:
    """
    Мешок с бочонками
    """
    numbers = [i for i in range(1, 91)]

    def __init__(self):
        self.shake_the_bag()

    def shake_the_bag(self):
        """
        Перемешать содержимое мешка
        """
        shuffle(self.numbers)

    def get_barrel(self):
        """
        Достать бочонок из мешка
        """
        try:
            return self.numbers.pop()
        except IndexError as e:
            raise NoBarrelError from e

    def return_barrel(self, number):
        """
        Вернуть бочонок в мешок
        """
        self.numbers.append(number)


class CardStack:
    """
    Колода карточек для лото
    """

    @staticmethod
    def get_random_card() -> Card:
        """
        Получить карту из стопки
        :return:
        """
        return Card()


class GameMaster:
    stack = CardStack()
    bag = Bag()
    players = None

    def __init__(self, players_list):
        self.players = players_list
        print(f'В игре участвуют: {", ".join([player.name for player in self.players])}')

    def get_card(self):
        return self.stack.get_random_card()

    def get_barrel(self):
        return self.bag.get_barrel()

    def game_cycle(self):
        barrel_number = self.get_barrel()
        print(f'\nТянем бочонок из мешка и это бочонок с номером {barrel_number}')

        for player in self.players:
            player_answer = player.is_number_on_card(barrel_number)
            master_answer = barrel_number in player.card

            answer_translation = 'есть такой номер' if player_answer else 'нет такого номера'
            print(f'{player.name} говорит что у него {answer_translation}')

            if player_answer == master_answer:
                if player_answer is True:
                    player.mark_number_on_card(barrel_number)
                    break
            else:
                raise EndOfTheGame(f'{player.name} ошибается и проигрывает в игре.')
