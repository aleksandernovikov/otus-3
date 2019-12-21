from random import shuffle

from log import loto_logger
from loto.card import Card
from loto.exceptions import NoBarrelError, EndOfTheGame


class Bag:
    """
    Мешок с бочонками
    """
    numbers = [i for i in range(1, 91)]

    def __init__(self):
        """
        Инициализация мешка
        """
        loto_logger.debug('Инициализация мешка')
        self.shake_the_bag()

    def shake_the_bag(self):
        """
        Перемешать содержимое мешка
        """
        print('Встряхнул мешок')
        loto_logger.debug('Встряхнул мешок')
        shuffle(self.numbers)

    def get_barrel(self):
        """
        Достать бочонок из мешка
        """
        try:
            barrel = self.numbers.pop()
            loto_logger.debug(f'Найден бочонок {barrel}')
            return barrel
        except IndexError as e:
            loto_logger.exception(e)
            raise NoBarrelError from e

    def return_barrel(self, number):
        """
        Вернуть бочонок в мешок
        """
        loto_logger.debug(f'Бочонок {number} вернулся в мешок')
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
        loto_logger.debug(f'Получили случайную карту')
        return Card()


class GameMaster:
    """
    Ведущий игры
    """
    stack = CardStack()
    bag = Bag()
    barrels_to_be_returned = []
    players = None

    def __init__(self, players_list):
        """
        Инициализация игры
        :param players_list: список игроков
        """
        self.players = players_list
        loto_logger.debug(f'Ведущий создает игру для {len(players_list)} игроков')
        print(f'В игре участвуют: {", ".join([player.name for player in self.players])}')

    def get_card(self):
        """
        Получить карту из стопки карт
        :return: вернет случайно сгенерированную карточку
        """
        loto_logger.debug(f'Ведущий достает случайную карту')
        return self.stack.get_random_card()

    def get_barrel(self):
        """
        Вынуть бочонок из мешка
        :return: бочонок с номером
        """
        barrel = self.bag.get_barrel()
        loto_logger.debug(f'Ведущий достает бочонок {barrel}')
        return barrel

    def check_barrel(self, barrel_number):
        """
        Проверка нужно ли вернуть бочонок назад в мешок
        :param barrel_number: номер бочонка
        """
        if barrel_number in self.barrels_to_be_returned:
            self.bag.return_barrel(barrel_number)
            self.barrels_to_be_returned.remove(barrel_number)
            print(f'Ведущий возвращает бочонок с номером {barrel_number} в мешок')
            self.bag.shake_the_bag()

    def start_game(self):
        """
        Начало игры
        выясняется какие бочонки нужно будет вернуть в мешок, чтобы все игроки могли выиграть
        :return:
        """
        all_numbers = [player.card.numbers for player in self.players]
        all_numbers = sum(all_numbers, [])
        self.barrels_to_be_returned = [num for num in set(all_numbers) if all_numbers.count(num) > 1 and num > 0]
        loto_logger.debug(
            f'Ведущий сформировал список бочонков которые нужно будет вернуть в мешок {self.barrels_to_be_returned}'
        )

    def game_cycle(self):
        """
        Игровой цикл
        тянем бочонок -> слушаем ответ игрока -> анализируем его верность -> выдаем результат анализа
        """
        barrel_number = self.get_barrel()
        print(f'\nТянем бочонок из мешка и это бочонок с номером {barrel_number}')

        for player in self.players:
            player_answer = player.is_number_on_card(barrel_number)
            master_answer = barrel_number in player.card and barrel_number not in player.card.found

            answer_translation = 'есть такой номер' if player_answer else 'нет такого номера'
            print(f'{player.name} говорит что у него {answer_translation}')

            if player_answer == master_answer:
                if player_answer is True:
                    player.mark_number_on_card(barrel_number)
                    self.check_barrel(barrel_number)
                    break
            else:
                raise EndOfTheGame(f'{player.name} ошибается и проигрывает в игре.')
