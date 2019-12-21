from random import sample, choice, shuffle

from log import loto_logger


class Card:
    """
    Карта для лото
    """
    line_slices = (slice(0, 9), slice(9, 18), slice(18, 27))

    def __init__(self) -> None:
        """
        Инициализация карты и расположение номеров в соответствие с условиями

        Получилось довольно громоздко и не красиво
        в соответствие с условиями генерации https://infostart.ru/public/144326/
        будет время, переделаю
        """
        self.found = []
        placeholders = []
        for sl in self.line_slices:
            for i in range(9):
                r = range(i * 10, i * 10 + 9)
                r = [num for num in r if num not in placeholders]
                placeholders.append(choice(r))

        for islice in self.line_slices[:-1]:
            to_be_nulled = sample(placeholders[islice], 4)

            for n in to_be_nulled:
                indx = placeholders.index(n)
                placeholders[indx] = 0

        neutral = []
        for it in range(9):
            f = placeholders[self.line_slices[0]][it]
            s = placeholders[self.line_slices[1]][it]
            t = placeholders[self.line_slices[2]][it]
            indx = placeholders.index(t)

            if f > 0 and s > 0:
                placeholders[indx] = 0
            elif f > 0 or s > 0:
                neutral.append(t)

        empty_count = placeholders[self.line_slices[2]].count(0)

        if empty_count < 4:
            shuffle(neutral)
            for i in range(4 - empty_count):
                indx = placeholders.index(neutral[i])
                placeholders[indx] = 0

        loto_logger.debug(placeholders)
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
