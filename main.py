from pprint import pprint

from entities import Bag, CardStack, WinTheGame

bag = Bag()

stack = CardStack()

card = stack.get_card()
pprint(card.preview())
step = 0
while True:
    barrel = bag.get_barrel()
    step += 1
    print(f'\nШаг № {step}')
    print(f'Из мешка вытянули {barrel}')
    try:
        print('Есть на карте' if barrel in card else 'Нет на карте')
    except WinTheGame:
        print('Карта собрана, вы победили')
        break
