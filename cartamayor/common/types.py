from collections import namedtuple
from enum import Enum, auto


CARD_STATS = namedtuple("STATS", ("power", "resistance"))


class Suit(Enum):
    CLUBS = "♣"
    HEARTS = "♡"
    SPADES = "♠"
    DIAMONDS = "♢"


class SideEffect(Enum):
    """
    STALL_INITIATIVE_QUEUE: for preventing the initiative queue to roll once
    REVERSE_INITIATIVE_QUEUE: for reversing the direction of the initiative queue
    """
    STALL_INITIATIVE_QUEUE = auto()
    REVERSE_INITIATIVE_QUEUE = auto()


class CardType(Enum):
    HAND = auto()
    OPEN = auto()
    HIDDEN = auto()
    TABLE = auto()
    DEAD = auto()


class GameMode(Enum):
    """
    FULL_MONTY: player by 2 teams of 2 players
    FATAL_THREE_WAY: played by 3 people with no teams
    """
    FULL_MONTY = auto()
    FATAL_THREE_WAY = auto()
