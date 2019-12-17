import termtables as tt

from loto.base import Bag, CardStack
from loto.exceptions import EndOfTheGame
from loto.settings import answers


def branching_answers(msg, yes, no):
    answer_result = input(msg)
    selected_action = yes if answers.get(answer_result, False) else no
    selected_action()


def player_check(card, number):
    if number in card:
        print('Отмечаем номер')
        card.mark_number(number)
    else:
        raise EndOfTheGame('Такого номера у вас нет')


def computer_check(card, number):
    if number in card:
        print('У компьютера есть такой номер')
        card.mark_number(number)
    else:
        print('У компьютера нет такого номера')


bag = Bag()
stack = CardStack()

player_card = stack.get_card()
print('Вам досталась карта')
print(tt.to_string(
    data=player_card.preview(),
    header=[],
    alignment='c',
    style=tt.styles.rounded_double
))

computer_card = stack.get_card()
branching_answers('Хотите посмотреть карту компьютера? ',
                  lambda: print(
                      tt.to_string(
                          data=computer_card.preview(),
                          header=[],
                          alignment='c',
                          style=tt.styles.rounded_double
                      )),
                  lambda: print('Продолжаем')
                  )
print('-' * 20)
while True:
    current_number = bag.get_barrel()
    player_has_number = current_number in player_card
    computer_has_number = current_number in computer_card

    print(f'\nВедущий вытянул боченок с номером {current_number}')
    try:
        branching_answers('У вас есть такой номер? ',
                          yes=lambda: player_check(player_card, current_number),
                          no=lambda: computer_check(computer_card, current_number))
    except EndOfTheGame as e:
        print(e)
        break
    except Exception as e:
        print(e)
    else:
        print(tt.to_string(
            data=player_card.preview(),
            header=[],
            alignment='c',
            style=tt.styles.rounded_double
        ))
