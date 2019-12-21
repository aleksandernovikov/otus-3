import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="game.log",
    level=logging.DEBUG
)
loto_logger = logging.getLogger("loto")
