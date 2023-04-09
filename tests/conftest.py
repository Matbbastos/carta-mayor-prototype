import pytest
from collections import deque

from cartamayor.common.classes import Card, Pile, Player
from cartamayor.common.types import PileLocation, Suit
from cartamayor.director import build_deck


@pytest.fixture
def full_deck() -> deque[Card]:
    return build_deck()


@pytest.fixture
def private_pile() -> Pile:
    private_pile = Pile(PileLocation.PRIVATE)
    private_pile.extend([
        Card("2", Suit.CLUBS),
        Card("3", Suit.DIAMONDS),
        Card("10", Suit.HEARTS),
        Card("A", Suit.SPADES),
        Card("4", Suit.CLUBS)])
    return private_pile


@pytest.fixture
def open_pile() -> Pile:
    open_pile = Pile(PileLocation.OPEN)
    open_pile.extend([
        Card("4", Suit.DIAMONDS),
        Card("5", Suit.DIAMONDS),
        Card("6", Suit.HEARTS),
        Card("7", Suit.SPADES)])
    return open_pile


@pytest.fixture
def hidden_pile() -> Pile:
    hidden_pile = Pile(PileLocation.HIDDEN)
    hidden_pile.extend([
        Card("4", Suit.HEARTS),
        Card("8", Suit.DIAMONDS),
        Card("10", Suit.SPADES),
        Card("K", Suit.SPADES)])
    return hidden_pile


@pytest.fixture
def table_pile() -> Pile:
    table_pile = Pile(PileLocation.TABLE)
    table_pile.extend([
        Card("3", Suit.HEARTS),
        Card("4", Suit.SPADES),
        Card("6", Suit.SPADES),
        Card("J", Suit.CLUBS),
        Card("Q", Suit.HEARTS),
        Card("10", Suit.DIAMONDS),
        Card("5", Suit.SPADES)])
    return table_pile


@pytest.fixture
def player_with_cards() -> Player:
    player = Player("Player One")
    player.private_cards.extend([
        Card("2", Suit.CLUBS),
        Card("3", Suit.DIAMONDS),
        Card("10", Suit.HEARTS),
        Card("A", Suit.SPADES),
        Card("4", Suit.CLUBS)])
    player.open_cards.extend([
        Card("4", Suit.DIAMONDS),
        Card("5", Suit.DIAMONDS),
        Card("6", Suit.HEARTS),
        Card("7", Suit.SPADES)])
    player.hidden_cards.extend([
        Card("4", Suit.HEARTS),
        Card("8", Suit.DIAMONDS),
        Card("10", Suit.SPADES),
        Card("K", Suit.SPADES)])
    return player
