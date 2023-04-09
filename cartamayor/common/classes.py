from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from cartamayor.common.constants import LABEL_TO_STATS
from cartamayor.common.types import GameMode, PileLocation, Suit


@dataclass(frozen=True)
class Player:
    """
    Represents a player, who is identified by their name, which cannot be changed after
    creation.
    """
    name: str


@dataclass(frozen=True)
class Team:
    """
    Represents a team of 2 Players, and contains a name. Members and name cannot be changed
    after creation.
    """
    name: str
    players: list[Player]


@dataclass
class Card:
    """Represents a playing Card, which is identified by label and suit.

    Parameters:
        label (str): label of the card, representing its rank.
        suit (Suit): suit of the card, from french standard deck.
        power (float): value to determine on top of which cards this card can be played.
        resistance (float): value to determine which cards cannot be played on top of this
            card.
    """
    label: str
    suit: Suit
    power: Optional[float] = None
    resistance: Optional[float] = None

    def __post_init__(self) -> None:
        """Assigns power and resistance to the card based on its label."""
        self.power, self.resistance = LABEL_TO_STATS[self.label]

    def __str__(self) -> str:
        return f'{self.suit.value}{self.label}'


class Pile(deque):
    """
    Represents a pile of cards, in a specific location of the game, possibly belonging to a
    player.
    """
    def __init__(
            self, cards: set[Card], location: PileLocation, owner: Optional[Player]
            ) -> None:
        """
        Initializes pile with cards, location and owner.

        Args:
            cards (set[Card]): set of cards to initialize the Pile.
            location (PileLocation): location of the pile in the game.
            owner (Optional[Player]): player that owns the pile, if any.

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
    """
    game_mode: GameMode
    initiative_queue: deque[Player]
    deck: deque[Card]
    table_pile: Pile
    dead_pile: Pile

    def __post_init__(self) -> None:
        self.started_at = datetime.now(timezone.utc)
