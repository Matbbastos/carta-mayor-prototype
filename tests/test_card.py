import math
from collections import deque

from cartamayor.common.classes import Card
from cartamayor.common.types import Suit


def test_card_print() -> None:
    assert str(Card("2", Suit.CLUBS)) == "♣2"
    assert str(Card("5", Suit.HEARTS)) == "♡5"
    assert str(Card("J", Suit.SPADES)) == "♠J"
    assert str(Card("A", Suit.DIAMONDS)) == "♢A"

    assert repr(Card("2", Suit.CLUBS)) == "Card(label='2', suit=Suit.CLUBS)"
    assert repr(Card("5", Suit.HEARTS)) == "Card(label='5', suit=Suit.HEARTS)"
    assert repr(Card("J", Suit.SPADES)) == "Card(label='J', suit=Suit.SPADES)"
    assert repr(Card("A", Suit.DIAMONDS)) == "Card(label='A', suit=Suit.DIAMONDS)"


def test_deck_length(full_deck: deque[Card]) -> None:
    assert len(full_deck) == 52


def test_deck_power(full_deck: deque[Card]) -> None:
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


def test_deck_resistance(full_deck: deque[Card]) -> None:
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


def test_card_playability() -> None:
    assert Card("2", Suit.CLUBS).is_playable_on(Card("3", Suit.DIAMONDS))
    assert Card("2", Suit.CLUBS).is_playable_on(Card("K", Suit.SPADES))
    assert Card("2", Suit.CLUBS).is_playable_on(Card("A", Suit.CLUBS))
    assert Card("2", Suit.CLUBS).is_playable_on(Card("10", Suit.HEARTS))
    assert Card("2", Suit.CLUBS).is_playable_on(Card("2", Suit.DIAMONDS))

    assert not Card("3", Suit.CLUBS).is_playable_on(Card("A", Suit.CLUBS))
    assert not Card("3", Suit.CLUBS).is_playable_on(Card("4", Suit.DIAMONDS))
    assert Card("3", Suit.CLUBS).is_playable_on(Card("10", Suit.HEARTS))
    assert Card("3", Suit.CLUBS).is_playable_on(Card("3", Suit.HEARTS))

    assert not Card("K", Suit.CLUBS).is_playable_on(Card("A", Suit.DIAMONDS))
    assert Card("K", Suit.CLUBS).is_playable_on(Card("Q", Suit.HEARTS))
    assert Card("K", Suit.CLUBS).is_playable_on(Card("2", Suit.SPADES))
    assert Card("K", Suit.CLUBS).is_playable_on(Card("K", Suit.CLUBS))

    assert Card("10", Suit.CLUBS).is_playable_on(Card("3", Suit.HEARTS))
    assert Card("10", Suit.CLUBS).is_playable_on(Card("A", Suit.DIAMONDS))
    assert Card("10", Suit.CLUBS).is_playable_on(Card("2", Suit.HEARTS))
    assert Card("10", Suit.CLUBS).is_playable_on(Card("10", Suit.CLUBS))

    assert not Card("7", Suit.CLUBS).is_playable_on(Card("8", Suit.HEARTS))
    assert Card("7", Suit.CLUBS).is_playable_on(Card("5", Suit.DIAMONDS))
    assert Card("7", Suit.CLUBS).is_playable_on(Card("10", Suit.SPADES))
    assert Card("7", Suit.CLUBS).is_playable_on(Card("2", Suit.CLUBS))
    assert Card("7", Suit.CLUBS).is_playable_on(Card("7", Suit.DIAMONDS))


def test_card_equalities() -> None:
    assert Card("2", Suit.CLUBS) == Card("2", Suit.CLUBS)
    assert Card("10", Suit.SPADES) == Card("10", Suit.SPADES)
    assert Card("A", Suit.HEARTS) == Card("A", Suit.HEARTS)
    assert Card("7", Suit.SPADES) == Card("7", Suit.SPADES)
    assert Card("3", Suit.CLUBS) == Card("3", Suit.CLUBS)


def test_card_inequalities() -> None:
    assert Card("2", Suit.CLUBS) != Card("2", Suit.SPADES)
    assert Card("10", Suit.SPADES) != Card("10", Suit.HEARTS)
    assert Card("A", Suit.HEARTS) != Card("K", Suit.HEARTS)
    assert Card("7", Suit.SPADES) != Card("8", Suit.SPADES)
    assert Card("4", Suit.CLUBS) != Card("3", Suit.CLUBS)


def test_cards_from_diferent_suits() -> None:
    assert Card("2", Suit.CLUBS).label == Card("2", Suit.HEARTS).label
    assert Card("10", Suit.CLUBS).power == Card("10", Suit.SPADES).power
    assert Card("A", Suit.CLUBS).resistance == Card("A", Suit.DIAMONDS).resistance
    assert Card("3", Suit.CLUBS).suit == Card("7", Suit.CLUBS).suit
