from pprint import pprint
from random import sample, randrange, choice, shuffle

from loto.exceptions import EndOfTheGame


class Card:
    """
    Карта для лото
    """
    line_slices = (slice(0, 9), slice(9, 18), slice(18, 27))

    # def prn(self, lst):
    #     for islice in self.line_slices:
    #         print(lst[islice])
    #     print()

    def __init__(self, numbers: list) -> None:
        # self.numbers = [i for i in range(3 * 9)]
        self.found = []
        placeholders = []
        for sl in self.line_slices:
            for i in range(9):
                r = range(i * 10, i * 10 + 9)
                r = [num for num in r if num not in placeholders]
                placeholders.append(choice(r))

        # self.prn(placeholders)

        for islice in self.line_slices[:-1]:
            to_be_nulled = sample(placeholders[islice], 4)

            for n in to_be_nulled:
                indx = placeholders.index(n)
                placeholders[indx] = 0

        # self.prn(placeholders)

        neutral = []
        for it in range(9):
            f = placeholders[self.line_slices[0]][it]
            s = placeholders[self.line_slices[1]][it]
            t = placeholders[self.line_slices[2]][it]
            indx = placeholders.index(t)

            if f > 0 and s > 0:
                # print(f'{f} и {s}, обнуляем')
                placeholders[indx] = 0
            elif f > 0 or s > 0:
                # print(f'{f}, {s} не ясно')
                neutral.append(t)

        # self.prn(placeholders)
        empty_count = placeholders[self.line_slices[2]].count(0)

        if empty_count < 4:
            shuffle(neutral)
            for i in range(4 - empty_count):
                # print(neutral[i])
                # print(placeholders.index(neutral[i]))
                indx = placeholders.index(neutral[i])
                # print(indx)
                placeholders[indx] = 0

        # self.prn(placeholders)
        # self.numbers = [num for num in placeholders if num != 0]
        self.numbers = placeholders

    def preview_line(self, num):
        visual = {
            0: '  '
        }
        visual.update({f: 'XX' for f in self.found})
        return [visual.get(slot, slot) for slot in self.numbers[num]]

    def preview(self) -> list:
        # res = []
        # for sl in self.line_slices:
        #     res.append(self.preview_line(sl))
        # return res
        return [self.preview_line(sl) for sl in self.line_slices]

    def __contains__(self, item) -> bool:
        return item in self.numbers

    def mark_number(self, number):
        if number in self.numbers:
            self.found.append(number)
        else:
            raise EndOfTheGame('Вы проиграли')

        if len(self.found) == 15:
            raise EndOfTheGame('Вы выиграли')

    def used_numbers(self):
        return self.numbers
