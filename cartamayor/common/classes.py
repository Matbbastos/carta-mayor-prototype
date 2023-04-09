from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

from cartamayor.common.constants import LABEL_TO_STATS
from cartamayor.common.types import GameMode, PileLocation, Suit


@dataclass(unsafe_hash=True)
class Card:
    """Represents a playing Card, which is identified by label and suit. This class is
    logically immutable objects, even though they are not frozen dataclasses.

    Parameters:
        label (str): label of the card, representing its rank.
        suit (Suit): suit of the card, from french standard deck.
        power (float): value to determine on top of which cards this card can be played.
        resistance (float): value to determine which cards cannot be played on top of this
            card.
    """
    label: str
    suit: Suit
    power: float = field(default=0, compare=False)
    resistance: float = field(default=0, compare=False)

    def __post_init__(self) -> None:
        """Assigns power and resistance to the card based on its label."""
        self.power, self.resistance = LABEL_TO_STATS[self.label]

    def __str__(self) -> str:
        return f"{self.suit.value}{self.label}"

    def __repr__(self) -> str:
        return f"Card(label='{self.label}', suit={self.suit})"



class Pile(deque):
    """
    Represents a pile of cards, in a specific location of the game, possibly belonging to a
    player.
    """
    def __init__(
            self, location: PileLocation, cards: Iterable[Card] | None = None) -> None:
        """
        Initializes pile with cards, location and owner.

        Args:
            location (PileLocation): location of the pile in the game.
            cards (Iterable[Card] | None): Iterable of cards to initialize the Pile.

        Raises:
            ValueError: if set of Cards is empty on construction.
        """
        if not cards:
            raise ValueError("Pile cannot be empty")
        super().__init__(cards)
        self.location = location
        self.owner = owner


@dataclass
class Match:
    """
    Represents a match which has a Game Mode, players (in teams or not), a deck of Cards,
    start and end times and is controlled by the Director module.

    Parameters:
        game_mode (GameMode): Game mode, as detailed in 'types' module.
        initiative_queue (deque[Player]): queue of players to control order of play.
        deck (deque[Card]): full deck of cards to be used for the game.
        table_pile (Pile): pile of cards in the table for the match.
        dead_pile (Pile): pile of dead cards, removed from the game.
        started_at (datetime | None): starting timestamp of the match.
        ended_at (datetime | None): ending timestamp of the match.
    """
    game_mode: GameMode
    initiative_queue: deque[Player]
    deck: deque[Card]
    table_pile: Pile
    dead_pile: Pile
    started_at: datetime | None = None
    ended_at: datetime | None = None

    def __post_init__(self) -> None:
        self.started_at = datetime.now(timezone.utc)
