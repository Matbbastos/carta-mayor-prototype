from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from common.types import GameMode, SideEffect, PileLocation, Suit
from common.mappings import LABEL_TO_STATS


class Player:
    pass


class Team:
    pass


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


@dataclass
class Stack:
    card_value: str


class Pile:
    strength: str


class Match:
    pass


class Director:
    pass
