from collections import deque
from datetime import datetime

from cartamayor.common.classes import Card, Player, Pile
from cartamayor.common.types import GameMode, PileLocation, Suit
from cartamayor.match import Match


def test_match_print(
        initiative_queue: deque[Player], full_deck: list[Card], table_pile: Pile) -> None:
    full_monty = Match(
        GameMode.FULL_MONTY,
        initiative_queue,
        full_deck,
        table_pile,
        Pile(PileLocation.DEAD, []),
        datetime(year=2023, month=4, day=12, hour=21, minute=13))
    fatal_three_way = Match(
        GameMode.FATAL_THREE_WAY,
        initiative_queue,
        full_deck,
        table_pile,
        Pile(PileLocation.DEAD, [Card("2", Suit.CLUBS), Card("3", Suit.DIAMONDS)]),
        datetime(year=2022, month=7, day=15, hour=11, minute=59))
    not_started = Match(
        GameMode.FULL_MONTY,
        initiative_queue,
        full_deck,
        table_pile,
        Pile(PileLocation.DEAD, []))

    assert str(full_monty) == (
        "FULL MONTY started at 2023-04-12 21h13 - "
        "[Player One, Player 2, Third Player, 4th Player] - Top table card: ♠5 - # Dead: 0")
    assert str(fatal_three_way) == (
        "FATAL THREE WAY started at 2022-07-15 11h59 - "
        "[Player One, Player 2, Third Player, 4th Player] - Top table card: ♠5 - # Dead: 2")
    assert str(not_started) == (
        "FULL MONTY not started - "
        "[Player One, Player 2, Third Player, 4th Player] - Top table card: ♠5 - # Dead: 0")
