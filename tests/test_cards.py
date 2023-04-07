import math
import pytest

from cartamayor.common.classes import Card
from cartamayor.common.constants import CARD_LABELS
from cartamayor.common.types import Suit


@pytest.fixture()
def full_deck() -> list[Card]:
    deck = []
    for suit in Suit:
        for label in CARD_LABELS:
            deck.append(Card(label, suit))
    return deck


def test_card_print() -> None:
    assert str(Card("2", Suit.CLUBS)) == "♣2"
    assert str(Card("5", Suit.HEARTS)) == "♡5"
    assert str(Card("J", Suit.SPADES)) == "♠J"
    assert str(Card("A", Suit.DIAMONDS)) == "♢A"


def test_deck_length(full_deck: list[Card]) -> None:
    assert len(full_deck) == 52


def test_deck_power(full_deck: list[Card]) -> None:
    for card in full_deck:
        if card.label in "3456789":
            assert card.power == int(card.label)
        elif card.label in "J":
            assert card.power == 11
        elif card.label in "Q":
            assert card.power == 12
        elif card.label in "K":
            assert card.power == 13
        elif card.label in "A":
            assert card.power == 14
        else:
            assert card.power == math.inf


def test_deck_resistance(full_deck: list[Card]) -> None:
    for card in full_deck:
        if card.label in "3456789":
            assert card.resistance == int(card.label)
        elif card.label in "J":
            assert card.resistance == 11
        elif card.label in "Q":
            assert card.resistance == 12
        elif card.label in "K":
            assert card.resistance == 13
        elif card.label in "A":
            assert card.resistance == 14
        else:
            assert card.resistance == 0
