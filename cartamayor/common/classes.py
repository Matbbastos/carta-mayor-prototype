from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Iterable

from cartamayor.common.constants import LABEL_TO_STATS
from cartamayor.common.types import PileLocation, Suit


@dataclass(unsafe_hash=True, slots=True)
class Card:
    """A playing Card, which is identified by label and suit. Objects from this class are
    logically immutable, even though the class is not a frozen dataclasse.

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
        """Assign power and resistance to the card based on its label."""
        self.power, self.resistance = LABEL_TO_STATS[self.label]

    def __str__(self) -> str:
        return f"{self.suit.value}{self.label}"

    def __repr__(self) -> str:
        return f"Card(label='{self.label}', suit={self.suit})"

    def is_playable_on(self, other: Card) -> bool:
        """A card is considered playable (on top of another) if its power is greater than
        or equal to the other's resistance.

        Args:
            other (Card): Reference card on top of which the current would be played.

        Returns:
            bool: True if the card has a power greater or equal to the other's resistance,
            False otherwise.
        """
        if self.power >= other.resistance:
            return True
        return False


class Pile(deque):
    """
    A pile of cards, in a specific location of the game.
    """
    def __init__(
            self,
            location: PileLocation, cards: list[Card] | None = None, /,
            sorted: bool = False) -> None:
        """
        Initialize pile with cards, location and owner.

        Args:
            location (PileLocation): location of the pile in the game.
            cards (list[Card] | None): List of cards to initialize the Pile.
            Defaults to None.
            sorted (bool): Whether or not the pile should be sorted based on card power.
            Sorting is applied whenever adding cards as well. Defaults to False.
        """
        if cards is None:
            cards = []
        self.location = location
        self.sorted = sorted
        if self.sorted:
            cards.sort(key=lambda card: card.power)
        super().__init__(cards)

    def __eq__(self, other: Pile) -> bool:
        """Define equality of Pile based on content and location.

        Args:
            other (Pile): Other Pile for comparison.

        Returns:
            bool: True if location is the same and underlying content is the same (deque
            equality), False otherwise.
        """
        if self.location == other.location:
            return super().__eq__(other)
        return False

    def __ne__(self, other: Pile) -> bool:
        """Implement the "not equals" operation to avoid fallback to deque's operation
        (which doesn't take the 'location' into account)

        Args:
            other (Pile): Other Pile for comparison.

        Returns:
            bool: Inverse of self == other.
        """
        return not self == other

    def __repr__(self) -> str:
        content = ", ".join(repr(item) for item in self)
        return f"Pile({self.location}, [{content}])"

    def __str__(self) -> str:
        return self._build_display_str(str(item) for item in self)

    def _build_display_str(self, pack: Iterable[str]) -> str:
        """
        Abstract the construction of a display string to get any iterable string input.

        Args:
            pack (Iterable[str]): Packed content to be placed inside the "Pile[]" section.

        Returns:
            str: Pile representation of the content inside 'pack', along with its location.
        """
        content = ", ".join(pack)
        location = f"({self.location.name})"
        return f"{location:<9} Pile[{content}]"

    def get_display_length(self) -> str:
        if len(self) > 5:
            return "5+"
        return str(len(self))

    def add_cards(self, cards: list[Card]) -> Pile:
        """
        Add cards to the pile, keeping sorting order if relevant.

        Args:
            cards (list[Card]): New cards to add to the pile.

        Returns:
            Pile: Pile after addition of all cards to it.
        """
        if not self.sorted:
            self.extend(cards)
        else:
            index_to_insert = 0
            for new_card in sorted(cards, key=lambda c: c.power):
                for card in self:
                    if new_card.power > card.power:
                        index_to_insert += 1
                self.insert(index_to_insert, new_card)
        return self

    def masked(self) -> str:
        """Provide a masked version of the content of the Pile.

        Returns:
            str: Pile representation but for any content in it, a ▇ is used in place of its
            original string representation.
        """
        return self._build_display_str("▇" for _ in self)

    def contains_playable_card(self, table_pile: Pile) -> bool:
        """Define whether or not a pile contains at least one playable card given the table
        pile.

        Args:
            table_pile (Pile): Pile of cards currently in the table.

        Returns:
            bool: True if the pile has a card with power greater than or equal to the
            resitance of the table pile's last/top card or if the table pile is empty.
        """
        if not table_pile:
            return True
        if max((card.power for card in self)) >= table_pile[-1].resistance:
            return True
        return False

    def get_playable_cards(self, table_pile: Pile) -> set:
        """Return a set of the playable cards contained in the pile.

        Args:
            table_pile (Pile): Pile of cards currently in the table.

        Returns:
            set: Set of cards that have a power greater than or equal to the table pile's
            last/top card.
        """
        if not table_pile:
            return set(self)
        return set(card for card in self if card.power >= table_pile[-1].resistance)

    def remove_cards(self, cards: Iterable[Card]) -> Pile:
        """Remove a collection of cards from the pile.

        Args:
            cards (Iterable[Card]): Collection of cards to be removed from the pile. If any
            card is not present in the Pile, ValueError is raised.

        Returns:
            Pile: Pile after removal of all cards from the collection.
        """
        for card in cards:
            self.remove(card)
        return self


@dataclass(frozen=True, slots=True)
class Player:
    """
    A player who is identified by their name, which cannot be changed after creation.

    Parameters:
        name (str): Name of the player.
        private_cards (Pile): Pile of private cards, only visible to the player.
        open_cards (Pile): Pile of open cards, visible to all players.
        hidden_cards (Pile): Pile of hidden cards, visible to no one.
    """
    name: str
    private_cards: Pile = field(default_factory=lambda: Pile(PileLocation.PRIVATE))
    open_cards: Pile = field(default_factory=lambda: Pile(PileLocation.OPEN))
    hidden_cards: Pile = field(default_factory=lambda: Pile(PileLocation.HIDDEN))

    def __str__(self) -> str:
        return f"{self.name}: {self.private_cards}, {self.open_cards}, {self.hidden_cards}"

    def get_source(self) -> Pile:
        """Get the current card source for the player, i.e. from where the player should
        play their cards.

        Returns:
            Pile: Private pile, if it has cards; otherwise Open pile if it has cards;
            else the Hidden pile.
        """
        return self.private_cards or self.open_cards or self.hidden_cards

    def get_playable_cards(self, table_pile: Pile) -> set[Card]:
        """Return the set of playable cards that the player has.

        Note: Hidden piles are always considered completely playable.

        Args:
            table_pile (Pile): Pile of cards currently in the table.

        Returns:
            set[Card]: Set of cards that from which the player can choose to play.
        """
        source = self.get_source()
        if source.location == PileLocation.HIDDEN:
            return {card for card in source}
        return source.get_playable_cards(table_pile)


@dataclass(frozen=True, slots=True)
class Team:
    """
    A team of 2 Players, containing a name. Members and name cannot be changed after
    creation.
    """
    name: str
    players: tuple[Player, Player]

    def __str__(self) -> str:
        return (
            f"{type(self).__name__} {self.name}: {self.players[0].name} | "
            f"{self.players[1].name}")
