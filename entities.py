from random import shuffle, sample


class NoCardError(Exception):
    pass


class NoBarrelError(Exception):
    pass


class WinTheGame(Exception):
    pass


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


class Card:
    line_slices = (slice(0, 9), slice(9, 18), slice(18, 27))

    def __init__(self, numbers: list):
        self.numbers = [i for i in range(3 * 9)]
        self.found = []
        placeholders = [sample(self.numbers[sl], 5) for sl in self.line_slices]
        placeholders = sum(placeholders, [])
        for slot in self.numbers:
            self.numbers[slot] = numbers.pop() if slot in placeholders else 0

    def preview(self):
        return [self.numbers[sl] for sl in self.line_slices]

    def __contains__(self, item):
        found = item in self.numbers
        if found:
            self.found.append(item)
        if len(self.found) == 15:
            raise WinTheGame

        return found


class CardStack(Base):
    """
    Колода карточек
    """

    def get_card(self):
        if self.numbers:
            nums = sample(self.numbers, 15)
            self.numbers = list(set(self.numbers) - set(nums))
            shuffle(self.numbers)
            return Card(nums)
        raise NoCardError
