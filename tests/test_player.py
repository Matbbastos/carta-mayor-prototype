import pytest
from dataclasses import FrozenInstanceError

from cartamayor.common.classes import Card, Pile, Player
from cartamayor.common.types import Suit


def test_player_immutability() -> None:
    player = Player("First Name")
    with pytest.raises(FrozenInstanceError) as _:
        player.name = "Second Name"   # type: ignore


def test_player_print(player_with_cards: Player) -> None:
    assert str(player_with_cards) == (
        "Player One: (PRIVATE) Pile[♣2, ♢3, ♡10, ♠A, ♣4], "
        "(OPEN)    Pile[♢4, ♢5, ♡6, ♠7], "
        "(HIDDEN)  Pile[♡4, ♢8, ♠10, ♠K]")

    assert repr(player_with_cards) == (
        "Player(name='Player One', private_cards=Pile(PileLocation.PRIVATE, ["
        "Card(label='2', suit=Suit.CLUBS), Card(label='3', suit=Suit.DIAMONDS), "
        "Card(label='10', suit=Suit.HEARTS), Card(label='A', suit=Suit.SPADES), "
        "Card(label='4', suit=Suit.CLUBS)]), open_cards=Pile(PileLocation.OPEN, ["
        "Card(label='4', suit=Suit.DIAMONDS), Card(label='5', suit=Suit.DIAMONDS), "
        "Card(label='6', suit=Suit.HEARTS), Card(label='7', suit=Suit.SPADES)]), "
        "hidden_cards=Pile(PileLocation.HIDDEN, ["
        "Card(label='4', suit=Suit.HEARTS), Card(label='8', suit=Suit.DIAMONDS), "
        "Card(label='10', suit=Suit.SPADES), Card(label='K', suit=Suit.SPADES)]))")


def test_source_definition(player_with_cards: Player) -> None:
    assert player_with_cards.get_source() == player_with_cards.private_cards
    player_with_cards.private_cards.clear()
    assert player_with_cards.get_source() == player_with_cards.open_cards
    player_with_cards.open_cards.clear()
    assert player_with_cards.get_source() == player_with_cards.hidden_cards


def test_playability_of_player_cards(player_with_cards: Player, table_pile: Pile) -> None:
    assert player_with_cards.has_playable_cards(table_pile)
    player_with_cards.private_cards.clear()
    assert player_with_cards.has_playable_cards(table_pile)

    table_pile.append(Card("9", Suit.CLUBS))
    assert not player_with_cards.has_playable_cards(table_pile)
    player_with_cards.open_cards.clear()
    assert player_with_cards.has_playable_cards(table_pile)

    table_pile.append(Card("A", Suit.CLUBS))
    assert player_with_cards.has_playable_cards(table_pile)
    player_with_cards.hidden_cards.remove(Card("10", Suit.SPADES))
    assert not player_with_cards.has_playable_cards(table_pile)
