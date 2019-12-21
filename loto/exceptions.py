class NoBarrelError(Exception):
    """
    Исключение выдается когда в мешке не осталось бочонков
    """
    pass


class EndOfTheGame(Exception):
    """
    Исключение для конца игры
    """
    pass
