from pprint import pprint

from entities import Bag, CardStack

b = Bag()

stack = CardStack()
card = stack.get_card()
pprint(card.preview())
