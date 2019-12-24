import pytest

from loto.card import Card
from loto.exceptions import NoBarrelError, EndOfTheGame
from loto.game_master import Bag, CardStack, GameMaster
from loto.player import AIPlayer, Player


class TestBag:
    """
    Тестирование мешка с бочонками
    """

    def test_shake_the_bag(self):
        """
        Тестирование метода перемешивания мешка
        """
        bag = Bag()
        bag_numbers = bag.numbers[:]
        bag.shake_the_bag()
        new_numbers = bag.numbers[:]
        assert bag_numbers != new_numbers

    def test_barrels_count(self):
        """
        Тестирование количества бочонков в мешке
        """
        bag = Bag()
        assert len(bag.numbers) == 90
        init_len = len(bag.numbers)
        bag.get_barrel()
        assert len(bag.numbers) == init_len - 1

    def test_get_barrel(self):
        """
        Тестирование метода когда ведущий достает бочонок
        """
        bag = Bag()
        number = bag.get_barrel()
        assert number not in bag.numbers

    def test_get_more_barrels(self):
        bag = Bag()
        with pytest.raises(NoBarrelError):
            for i in range(100):
                bag.get_barrel()

    def test_return_barrel(self):
        """
        Тестирование метода когда ведущий возвращает бочонок в мешок
        """
        bag = Bag()
        number = bag.get_barrel()
        assert number not in bag.numbers
        bag.return_barrel(number)
        assert number in bag.numbers


class TestCardStack:
    def setup(self):
        self.stack = CardStack()

    def test_get_card(self):
        for i in range(10):
            card = self.stack.get_random_card()
            assert isinstance(card, Card)
            assert len(card.numbers) == 27
            card_numbers = [num for num in card.numbers if num is not 0]
            assert len(card_numbers) == 15


class TestPlayer:
    def test_get_a_card(self):
        test_player = Player(name='Test')
        stack = CardStack()
        card = stack.get_random_card()
        test_player.get_a_card(card)
        assert card == test_player.card


class TestGameMaster:
    master = None

    def setup(self):
        players = [
            AIPlayer(name='Компьютер 1'),
            AIPlayer(name='Компьютер 2')
        ]
        self.master = GameMaster(players_list=players)

        for player in self.master.players:
            player.get_a_card(self.master.get_card())

        self.master.start_game()

    def test_game_cycle_player_answer(self):
        barrel_number = self.master.get_barrel()
        wrong_player_answer = not self.master.players[0].is_number_on_card(barrel_number)
        master_answer = barrel_number in self.master.players[0].card
        assert wrong_player_answer != master_answer

    def test_more_barrels_in_bag(self):
        with pytest.raises(NoBarrelError):
            for i in range(100):
                self.master.get_barrel()
