from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from common.types import GameMode, SideEffect, PileLocation, Suit
from common.mappings import LABEL_TO_STATS


@dataclass(frozen=True)
class Player:
    """
    Represents a player, who is identified by their name, which cannot be changed after
    creation
    """
    name: str


@dataclass(frozen=True)
class Team:
    """
    Represents a team of 2 Players, and contains a name. Members and name cannot be changed
    after creation
    """
    name: str
    players: list[Player]


@dataclass
class Card:
    """Represents a playing Card, which is identified by label and suit

    Parameters:
        label (str): label of the card, representing its rank
        suit (Suit): suit of the card, from french standard deck
        power (float): value to determine on top of which cards this card can be played
        resistance (float): value to determine which cards cannot be played on top of this
            card
        side_effect (list[SideEffect], optional): list of effects the card has in the
            initiative queue
    """
    label: str
    suit: Suit
    power: float
    resistance: float
    side_effect: Optional[list[SideEffect]] = None

    def __post_init__(self) -> None:
        """Assigns power, resistance and side effects to the card, based on its label"""
        self.power, self.resistance = LABEL_TO_STATS[self.label]
        if self.label == "2":
            self.side_effect = [
                SideEffect.STALL_INITIATIVE_QUEUE, SideEffect.REVERSE_INITIATIVE_QUEUE]

    def __str__(self) -> str:
        return f'{self.suit.value}{self.label}'


class Pile(deque):
    """
    Represents a pile of cards, in a specific location of the game, possibly belonging to a
    player
    """
    def __init__(
            self, cards: set[Card], location: PileLocation, owner: Optional[Player]
            ) -> None:
        """
        Initializes pile with cards, location and owner

        Args:
            cards (set[Card]): set of cards to initialize the Pile
            location (PileLocation): location of the pile in the game
            owner (Optional[Player]): player that owns the pile, if any

        Raises:
            ValueError: if set of Cards is empty on construction
        """
        if not cards:
            raise ValueError("Pile cannot be empty")
        super().__init__(cards)
        self.location = location
        self.owner = owner


class Director:
    """
    Defines the actions taken by the game Director in order for the match to unfold as
    expected
    """
    pass


@dataclass
class Match:
    """
    Represents a match which has a Game Mode, players (in teams or not), a deck of Cards,
    start and end times and is controlled by the Director
    """
    game_mode: GameMode
    initiative_queue: deque[Player]
    director: Director
    deck: deque[Card]
    started_at: datetime
    ended_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.started_at = datetime.now(timezone.utc)
