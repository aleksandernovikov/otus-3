import termtables as tt

from entities import Bag, CardStack, WinTheGame

bag = Bag()

stack = CardStack()

card = stack.get_card()
print('Ваша карта')
print(tt.to_string(
    data=card.preview(),
    header=[],
    alignment='c',
    style=tt.styles.rounded_double
))

step = 0
while True:
    barrel = bag.get_barrel()
    step += 1
    print(f'\nШаг № {step}')
    print(f'Из мешка вытянули бочонок с номером {barrel}')
    try:
        print('Есть на карте' if barrel in card else 'Нет на карте')
    except WinTheGame:
        print('Карта собрана, вы победили')
        break
