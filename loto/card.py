from pprint import pprint
from random import sample, choice, shuffle, randrange

from log import loto_logger


class Card:
    """
    Карта для лото
    """
    line_slices = (slice(0, 9), slice(9, 18), slice(18, 27))

    @staticmethod
    def _generate_card(w=9, h=3):
        placeholders = [[0] * w for i in range(h)]

        def get_column_sum(column_number):
            return sum([placeholders[row_number][column_number] for row_number in range(h)])

        def select_places(places_count=5):
            places = sample(range(w), places_count)
            return [1 if i in places else 0 for i in range(w)]

        def check_columns():
            for column_number in range(w):
                if get_column_sum(column_number) not in range(1, 3):
                    return False
            return True

        for row in range(h - 1):
            placeholders[row] = select_places(5)

        while True:
            placeholders[2] = select_places()
            if check_columns():
                break

        for column in range(w):
            possible_values = list(range(column * 10, column * 10 + 10))

            if column == 0:
                possible_values.remove(0)
            elif column == 8:
                possible_values.append(90)

            shuffle(possible_values)
            for row in range(h):
                if placeholders[row][column] == 1:
                    placeholders[row][column] = possible_values.pop()

        return placeholders

    def __init__(self) -> None:
        """
        Инициализация карты и расположение номеров в соответствие с условиями

        Получилось довольно громоздко и не красиво
        в соответствие с условиями генерации https://infostart.ru/public/144326/
        будет время, переделаю
        """
        self.found = []
        placeholders = self._generate_card()
        placeholders = sum(placeholders, [])

        loto_logger.debug(placeholders)

        try:
            assert len(placeholders) == 27
            assert len([num for num in placeholders if num is not 0]) == 15
        except AssertionError:
            print([num for num in placeholders if num is not 0])

        self.numbers = placeholders

    def preview(self) -> list:
        """
        Предпросмотр карточки
        Закрытые числа помечаются XX
        """

        def preview_line(num: slice) -> list:
            visual = {
                0: '  '
            }
            visual.update({f: 'XX' for f in self.found})
            return [visual.get(slot, slot) for slot in self.numbers[num]]

        return [preview_line(sl) for sl in self.line_slices]

    def __contains__(self, item: int) -> bool:
        """
        Опеределение магического метода для класса Card
        :param item: число с бочонка
        :return: признак наличия числа на карточке True или False
        """
        return item in self.numbers

    def mark_number(self, number: int) -> None:
        """
        Число на карте помечается как найденное
        :param number: номер числа
        """
        loto_logger.debug(f'Пробуем отметить номер {number}')
        loto_logger.debug(f'Номера на карте {self.numbers}')

        if number in self.numbers:
            loto_logger.debug('Номер найден')
            self.found.append(number)
