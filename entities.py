from random import shuffle, sample


class Base:
    numbers = [i for i in range(1, 91)]

    def __init__(self):
        shuffle(self.numbers)

    def pop_random_number(self):
        return self.numbers.pop()


class Bag(Base):
    """
    Мешок с бочонками
    """

    def get_barrel(self):
        return self.pop_random_number()


class Card:
    line_slices = (slice(0, 9), slice(9, 18), slice(18, 27))

    def __init__(self, numbers: list):
        self.numbers = [i for i in range(3 * 9)]
        placeholders = [sample(self.numbers[sl], 5) for sl in self.line_slices]
        placeholders = sum(placeholders, [])
        for slot in self.numbers:
            self.numbers[slot] = numbers.pop() if slot in placeholders else 0

    def preview(self):
        return [self.numbers[sl] for sl in self.line_slices]


class CardStack(Base):
    """
    Колода карточек
    """

    def get_card(self):
        nums = sample(self.numbers, 15)
        self.numbers = list(set(self.numbers) - set(nums))
        shuffle(self.numbers)
        return Card(nums)
