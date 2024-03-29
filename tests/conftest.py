import pytest
from collections import deque

from cartamayor.common.classes import Card, Pile, Player
from cartamayor.common.types import PileLocation, Suit, GameMode
from cartamayor.director import Director
from cartamayor.match import Match


PLAYER_STATE_TEST = [
    (
        Player(
            "Sample1",
            private_cards=Pile(
                PileLocation.PRIVATE, [
                    Card("2", Suit.CLUBS),
                    Card("3", Suit.DIAMONDS),
                    ]),
            open_cards=Pile(
                PileLocation.OPEN, [
                    Card("4", Suit.DIAMONDS),
                ]
            ),
            hidden_cards=Pile(PileLocation.HIDDEN, [
                Card("2", Suit.DIAMONDS),
                Card("3", Suit.DIAMONDS),
                Card("4", Suit.DIAMONDS),
                Card("5", Suit.DIAMONDS),
            ])),
        (
            "Source: PRIVATE\n"
            "│     OPEN: ♢4\n"
            "│   HIDDEN:  ▇  ▇  ▇  ▇\n"
            "│  PRIVATE: ♣2, ♢3\n"
            "└───────────────────────┘\n")
    ),
    (
        Player(
            "Sample2",
            private_cards=Pile(
                PileLocation.PRIVATE, [
                    Card("A", Suit.CLUBS),
                    Card("2", Suit.DIAMONDS),
                    Card("3", Suit.SPADES),
                    Card("4", Suit.HEARTS),
                    Card("5", Suit.CLUBS),
                    Card("6", Suit.DIAMONDS),
                    Card("7", Suit.SPADES),
                    Card("8", Suit.HEARTS),
                    Card("9", Suit.CLUBS),
                    Card("10", Suit.DIAMONDS),
                    ]),
            open_cards=Pile(PileLocation.OPEN, []),
            hidden_cards=Pile(PileLocation.HIDDEN, [
                Card("2", Suit.DIAMONDS),
                Card("3", Suit.DIAMONDS),
                Card("4", Suit.DIAMONDS),
                Card("5", Suit.DIAMONDS),
            ])),
        (
            "Source: PRIVATE\n"
            "│     OPEN:\n"
            "│   HIDDEN:  ▇  ▇  ▇  ▇\n"
            "│  PRIVATE: ♣A, ♢2, ♠3, ♡4, ♣5, ♢6, ♠7, ♡8, ♣9, ♢10\n"
            "└───────────────────────────────────────────────────┘\n")
    ),
    (
        Player(
            "Sample3",
            private_cards=Pile(PileLocation.PRIVATE, []),
            open_cards=Pile(PileLocation.OPEN, []),
            hidden_cards=Pile(PileLocation.HIDDEN, [Card("5", Suit.DIAMONDS),])),
        (
            "Source: HIDDEN\n"
            "│     OPEN:\n"
            "│   HIDDEN:  ▇\n"
            "│  PRIVATE:\n"
            "└──────────────┘\n")
    ),
    (
        Player(
            "Sample4",
            private_cards=Pile(PileLocation.PRIVATE, []),
            open_cards=Pile(
                PileLocation.OPEN, [
                    Card("A", Suit.CLUBS),
                    Card("2", Suit.DIAMONDS),
                    Card("4", Suit.HEARTS),
                ]
            ),
            hidden_cards=Pile(PileLocation.HIDDEN, [
                Card("2", Suit.DIAMONDS),
                Card("3", Suit.DIAMONDS),
                Card("4", Suit.DIAMONDS),
                Card("5", Suit.DIAMONDS),
            ])),
        (
            "Source: OPEN\n"
            "│     OPEN: ♣A, ♢2, ♡4\n"
            "│   HIDDEN:  ▇  ▇  ▇  ▇\n"
            "│  PRIVATE:\n"
            "└───────────────────────┘\n")
    ),
    (
        Player(
            "Sample5",
            private_cards=Pile(
                PileLocation.PRIVATE, [
                    Card("A", Suit.CLUBS),
                    Card("2", Suit.DIAMONDS),
                    Card("3", Suit.SPADES),
                    Card("4", Suit.HEARTS),
                    Card("5", Suit.CLUBS),
                    Card("6", Suit.DIAMONDS),
                    Card("7", Suit.SPADES),
                    Card("8", Suit.HEARTS),
                    Card("9", Suit.CLUBS),
                    Card("10", Suit.DIAMONDS),
                    ]),
            open_cards=Pile(PileLocation.OPEN, []),
            hidden_cards=Pile(PileLocation.HIDDEN, [])),
        (
            "Source: PRIVATE\n"
            "│     OPEN:\n"
            "│   HIDDEN:\n"
            "│  PRIVATE: ♣A, ♢2, ♠3, ♡4, ♣5, ♢6, ♠7, ♡8, ♣9, ♢10\n"
            "└───────────────────────────────────────────────────┘\n")
    ),
]


@pytest.fixture
def full_deck() -> list[Card]:
    return Director.build_deck()


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
def dead_pile() -> Pile:
    dead_pile = Pile(PileLocation.DEAD)
    dead_pile.extend([
        Card("2", Suit.HEARTS),
        Card("2", Suit.SPADES),
        Card("9", Suit.CLUBS),
        Card("9", Suit.HEARTS),
        Card("9", Suit.SPADES),
        Card("9", Suit.DIAMONDS)])
    return dead_pile


@pytest.fixture
def multiple_plays() -> tuple[list[Card], ...]:
    return (
        [Card("2", Suit.CLUBS), Card("2", Suit.HEARTS)],
        [Card("3", Suit.CLUBS)],
        [Card("4", Suit.HEARTS)],
        [Card("10", Suit.CLUBS), Card("10", Suit.DIAMONDS)],
        [Card("Q", Suit.CLUBS), Card("Q", Suit.SPADES), Card("Q", Suit.DIAMONDS)],
        [Card("2", Suit.SPADES), Card("2", Suit.DIAMONDS)],
        [Card("9", Suit.CLUBS), Card("9", Suit.HEARTS)],
        [Card("3", Suit.HEARTS), Card("3", Suit.DIAMONDS)],
        [Card("2", Suit.CLUBS)],
        [Card("9", Suit.CLUBS), Card("9", Suit.HEARTS), Card("9", Suit.SPADES)],
    )


@pytest.fixture
def multiple_table_details() -> list[tuple[int, list[Card | None]]]:
    return [
        (3, [Card("3", Suit.CLUBS), None, None]),
        (4, [Card("3", Suit.CLUBS), Card("2", Suit.HEARTS), None, None]),
        (5, [
            Card("10", Suit.DIAMONDS), Card("10", Suit.CLUBS),
            Card("2", Suit.HEARTS), Card("2", Suit.CLUBS), None]),
        (6, [Card("10", Suit.DIAMONDS), Card("10", Suit.CLUBS), None, None, None, None]),
        (7, [Card("3", Suit.CLUBS), None, None, None, None, None]),
        (9, [
            Card("3", Suit.DIAMONDS), Card("3", Suit.HEARTS), Card("3", Suit.CLUBS),
            None, None, None]),
        (11, [Card("2", Suit.DIAMONDS), Card("2", Suit.SPADES), None, None, None, None]),
        (12, [
            Card("2", Suit.CLUBS), Card("2", Suit.DIAMONDS), Card("2", Suit.SPADES),
            None, None, None]),
        (15, [
            Card("9", Suit.SPADES), Card("9", Suit.HEARTS), Card("9", Suit.CLUBS),
            Card("2", Suit.CLUBS), Card("2", Suit.DIAMONDS), Card("2", Suit.SPADES)]),
    ]


@pytest.fixture
def player_with_cards() -> Player:
    player = Player("Player One")
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
    player.private_cards.extend([
        Card("2", Suit.CLUBS),
        Card("3", Suit.DIAMONDS),
        Card("10", Suit.HEARTS),
        Card("A", Suit.SPADES),
        Card("4", Suit.CLUBS)])
    return player


@pytest.fixture
def match_FM(initiative_queue: deque[Player], full_deck: list[Card]) -> Match:
    return Match(
        GameMode.FULL_MONTY,
        initiative_queue,
        full_deck,
        Pile(PileLocation.TABLE, [
            Card("2", Suit.CLUBS),
            Card("3", Suit.CLUBS),
            Card("K", Suit.CLUBS),
            Card("K", Suit.DIAMONDS)]),
        Pile(PileLocation.DEAD, [
            Card("K", Suit.HEARTS),
            Card("9", Suit.DIAMONDS),
            Card("9", Suit.CLUBS),
            Card("9", Suit.HEARTS),
            Card("9", Suit.SPADES)]))


@pytest.fixture
def initiative_queue() -> deque[Player]:
    return deque([
        Player("Player One"), Player("Player 2"),
        Player("Third Player"), Player("4th Player")])


@pytest.fixture
def long_initiative_queue() -> deque[Player]:
    return deque([
        Player("Player One plus Cookies"), Player("Player 2 and their clone"),
        Player("Third Player and third wheel"), Player("May the 4th Player be with you")])
