import math

from common.types import CARD_STATS


LABEL_TO_STATS = {
    "2": CARD_STATS(power=math.inf, resistance=0),
    "3": CARD_STATS(power=3, resistance=3),
    "4": CARD_STATS(power=4, resistance=4),
    "5": CARD_STATS(power=5, resistance=5),
    "6": CARD_STATS(power=6, resistance=6),
    "7": CARD_STATS(power=7, resistance=7),
    "8": CARD_STATS(power=8, resistance=8),
    "9": CARD_STATS(power=9, resistance=9),
    "10": CARD_STATS(power=math.inf, resistance=0),
    "J": CARD_STATS(power=11, resistance=11),
    "Q": CARD_STATS(power=12, resistance=12),
    "K": CARD_STATS(power=13, resistance=13),
    "A": CARD_STATS(power=14, resistance=14)
}
