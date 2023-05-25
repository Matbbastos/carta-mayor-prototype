from enum import Enum, auto
from typing import NamedTuple


class CardStats(NamedTuple):
    """Simple structure to hold stats from a card."""
    power: float
    resistance: int


class Suit(Enum):
    """Standard french playing card suits."""
    CLUBS = "♣"
    HEARTS = "♡"
    SPADES = "♠"
    DIAMONDS = "♢"


class PileLocation(Enum):
    """
    PRIVATE: cards belonging to a specific player that only they can see (hand).
    OPEN: cards belonging to a specific player that are visible to everyone.
    HIDDEN: cards belonging to a specific player that are not visible to anyone.
    TABLE: cards that don't belong to a player but are still in the game.
    DEAD: cards that don't belong to a player and were removed from the game.
    """
    PRIVATE = auto()
    OPEN = auto()
    HIDDEN = auto()
    TABLE = auto()
    DEAD = auto()


class GameMode(Enum):
    """
    FULL_MONTY: played by 2 teams of 2 players.
    FATAL_THREE_WAY: played by 3 people with no teams.
    """
    FULL_MONTY = auto()
    FATAL_THREE_WAY = auto()

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return Enum.__hash__(self)
