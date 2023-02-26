from dataclasses import dataclass

from common.types import Suit, Influence
from common.validations import is_valid_card_value


class Player:
    pass


class Team:
    pass


@dataclass
class Card:
    _value: str
    _strength: float
    suite: Suit
    influence: Influence

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if not is_valid_card_value(value):
            raise ValueError
        self._value = value


@dataclass
class Stack:
    card_value: str


class Pile:
    strength: str


class Match:
    pass


class Director:
    pass
