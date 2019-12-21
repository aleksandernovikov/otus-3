from loto.card import Card
from loto.game_master import Bag, CardStack, GameMaster
from loto.player import AIPlayer, Player


class TestBag:
    """
    Тестирование мешка с бочонками
    """

    def setup(self):
        """
        Создание мешка
        :return:
        """
        self.bag = Bag()

    def test_shake_the_bag(self):
        """
        Тестирование метода перемешивания мешка
        """
        bag_numbers = self.bag.numbers[:]
        self.bag.shake_the_bag()
        new_numbers = self.bag.numbers[:]
        assert bag_numbers != new_numbers

    def test_barrels_count(self):
        """
        Тестирование количества бочонков в мешке
        """
        assert len(self.bag.numbers) == 90
        init_len = len(self.bag.numbers)
        self.bag.get_barrel()
        assert len(self.bag.numbers) == init_len - 1

    def test_get_barrel(self):
        """
        Тестирование метода когда ведущий достает бочонок
        """
        number = self.bag.get_barrel()
        assert number not in self.bag.numbers

    def test_return_barrel(self):
        """
        Тестирование метода когда ведущий возвращает бочонок в мешок
        """
        number = self.bag.get_barrel()
        assert number not in self.bag.numbers
        self.bag.return_barrel(number)
        assert number in self.bag.numbers


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
    def setup(self):
        players = [
            AIPlayer(name='Компьютер 1'),
            AIPlayer(name='Компьютер 2')
        ]
        master = GameMaster(players_list=players)

        for player in players:
            player.get_a_card(master.get_card())

        master.start_game()
