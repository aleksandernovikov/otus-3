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
    player.get_a_card(random_card)

while True:
    try:
        master.game_cycle()
    except EndOfTheGame as e:
        print(e)
