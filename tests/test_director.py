import pytest

from cartamayor.common.classes import Card
from cartamayor.common.types import Suit
from cartamayor.director import Director
from cartamayor.match import Match


def test_deck_build() -> None:
    d = Director()
    full_deck = d.build_deck()
    assert len(full_deck) == 52
    assert len([card for card in full_deck if card.suit.name == 'CLUBS']) == 13
    assert len([card for card in full_deck if card.suit.name == 'DIAMONDS']) == 13
    assert len([card for card in full_deck if card.suit.name == 'HEARTS']) == 13
    assert len([card for card in full_deck if card.suit.name == 'SPADES']) == 13

    assert len([card for card in full_deck if card.label == "2"]) == 4
    assert len([card for card in full_deck if card.label == "3"]) == 4
    assert len([card for card in full_deck if card.label == "4"]) == 4
    assert len([card for card in full_deck if card.label == "5"]) == 4
    assert len([card for card in full_deck if card.label == "6"]) == 4
    assert len([card for card in full_deck if card.label == "7"]) == 4
    assert len([card for card in full_deck if card.label == "8"]) == 4
    assert len([card for card in full_deck if card.label == "9"]) == 4
    assert len([card for card in full_deck if card.label == "10"]) == 4
    assert len([card for card in full_deck if card.label == "J"]) == 4
    assert len([card for card in full_deck if card.label == "Q"]) == 4
    assert len([card for card in full_deck if card.label == "K"]) == 4
    assert len([card for card in full_deck if card.label == "A"]) == 4


def test_game_mode_selection(monkeypatch) -> None:
    d = Director()
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "FM")
        assert d._select_game_mode().name == 'FULL_MONTY'


def test_FM_match_creation(monkeypatch) -> None:
    d = Director()
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "FM")
        m.setattr("cartamayor.interface.prompt_for_FM_teams", lambda: {
            "Invictus": ("Firas", "Matheus"),
            "Second": ("Andrei", "Matthieu")})
        d.start_match()
    assert d.match.game_mode.name == 'FULL_MONTY'


def test_check_match_decorator() -> None:
    d = Director()
    with pytest.raises(ValueError, match="Match must be set before using this function"):
        d.get_next_player()


def test_table_pile_display(match_FM: Match, multiple_plays: tuple) -> None:
    d = Director(match=match_FM)
    d.match.table_pile.extend(multiple_plays[0])
    assert d.get_table_pile_display(multiple_plays[0]) == (6, [
        Card("2", Suit.HEARTS),
        Card("2", Suit.CLUBS),
        None, None, None, None])
    d.match.control_flags["show_previous_play"] = True

    d.match.table_pile.extend(multiple_plays[1])
    assert d.get_table_pile_display(multiple_plays[1]) == (7, [
        Card("3", Suit.CLUBS),
        Card("2", Suit.HEARTS),
        Card("2", Suit.CLUBS),
        None, None, None])
    d.match.control_flags["show_previous_play"] = False

    d.match.table_pile.extend(multiple_plays[2])
    assert d.get_table_pile_display(multiple_plays[2]) == (8, [
        Card("4", Suit.HEARTS),
        None, None, None, None, None])

    d.match.table_pile.extend(multiple_plays[3])
    assert d.get_table_pile_display(multiple_plays[3]) == (10, [
        Card("10", Suit.DIAMONDS),
        Card("10", Suit.CLUBS),
        None, None, None, None])

    d.match.table_pile.extend(multiple_plays[4])
    assert d.get_table_pile_display(multiple_plays[4]) == (13, [
        Card("Q", Suit.DIAMONDS),
        Card("Q", Suit.SPADES),
        Card("Q", Suit.CLUBS),
        None, None, None])

    d.match.table_pile.extend(multiple_plays[5])
    assert d.get_table_pile_display(multiple_plays[5]) == (15, [
        Card("2", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
        None, None, None, None])
    d.match.control_flags["show_previous_play"] = True

    d.match.table_pile.extend(multiple_plays[6])
    assert d.get_table_pile_display(multiple_plays[6]) == (17, [
        Card("9", Suit.HEARTS),
        Card("9", Suit.CLUBS),
        Card("2", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
        None, None])
    d.match.control_flags["show_previous_play"] = False


def test_table_pile_display_same_cards(match_FM: Match, multiple_plays: tuple) -> None:
    d = Director(match=match_FM)
    d.match.table_pile.extend(multiple_plays[3])
    assert d.get_table_pile_display(multiple_plays[3]) == (6, [
        Card("10", Suit.DIAMONDS),
        Card("10", Suit.CLUBS),
        None, None, None, None])

    d.match.table_pile.extend(multiple_plays[1])
    assert d.get_table_pile_display(multiple_plays[1]) == (7, [
        Card("3", Suit.CLUBS),
        None, None, None, None, None])

    d.match.table_pile.extend(multiple_plays[7])
    assert d.get_table_pile_display(multiple_plays[7]) == (9, [
        Card("3", Suit.DIAMONDS),
        Card("3", Suit.HEARTS),
        Card("3", Suit.CLUBS),
        None, None, None])

    d.match.table_pile.extend(multiple_plays[5])
    assert d.get_table_pile_display(multiple_plays[5]) == (11, [
        Card("2", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
        None, None, None, None])
    d.match.control_flags["show_previous_play"] = True

    d.match.table_pile.extend(multiple_plays[8])
    assert d.get_table_pile_display(multiple_plays[8]) == (12, [
        Card("2", Suit.CLUBS),
        Card("2", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
        None, None, None])
    d.match.control_flags["show_previous_play"] = True

    d.match.table_pile.extend(multiple_plays[9])
    assert d.get_table_pile_display(multiple_plays[9]) == (15, [
        Card("9", Suit.SPADES),
        Card("9", Suit.HEARTS),
        Card("9", Suit.CLUBS),
        Card("2", Suit.CLUBS),
        Card("2", Suit.DIAMONDS),
        Card("2", Suit.SPADES)])
    d.match.control_flags["show_previous_play"] = False
