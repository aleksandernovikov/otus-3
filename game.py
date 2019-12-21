from log import loto_logger
from loto.exceptions import EndOfTheGame
from loto.game_master import GameMaster
from loto.player import HumanPlayer, AIPlayer

players = [
    HumanPlayer(name='Человек'),
    AIPlayer(name='Компьютер')
]

master = GameMaster(players_list=players)

print('Раздаем карточки игрокам')

for player in players:
    random_card = master.get_card()
    loto_logger.debug(f'Игрок {player.name} получает карту {random_card.numbers}')
    player.get_a_card(random_card)

master.start_game()

while True:
    try:
        loto_logger.info('---')
        master.game_cycle()
    except EndOfTheGame as e:
        print(e)
        loto_logger.exception(e)
        break
    except Exception as e:
        loto_logger.exception(e)
