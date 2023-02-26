from collections import namedtuple
from enum import Enum, auto


CARD_STATS = namedtuple("STATS", ("power", "resistance"))


class Suit(Enum):
    CLUBS = "♣"
    HEARTS = "♡"
    SPADES = "♠"
    DIAMONDS = "♢"


class Influence(Enum):
    ROLL_INITIATIVE_QUEUE = auto()
    REVERSE_INITIATIVE_QUEUE = auto()
    UPDATE_CARD_STRENGTH = auto()


class CardType(Enum):
    HAND = auto()
    OPEN = auto()
    HIDDEN = auto()
    TABLE = auto()
    DEAD = auto()


class Visibility(Enum):
    ALL = auto()
    NONE = auto()
    OWNER = auto()


class Ownership(Enum):
    PLAYER = auto()
    TABLE = auto()
