import pytest
from dataclasses import FrozenInstanceError

from cartamayor.common.classes import Player, Team


def test_team_immutability() -> None:
    team = Team("Invictus", (Player("Matheus"), Player("Firas")))
    with pytest.raises(FrozenInstanceError) as _:
        team.name = "Losers"   # type: ignore


def test_team_print() -> None:
    team = Team("Invictus", (Player("Matheus Bruhns"), Player("Firas Mourad")))
    assert str(team) == "Invictus: Matheus Bruhns | Firas Mourad"
    assert repr(team) == (
        "Team(name='Invictus', players=(Player(name='Matheus Bruhns', "
        "private_cards=Pile(PileLocation.PRIVATE, []), "
        "open_cards=Pile(PileLocation.OPEN, []), "
        "hidden_cards=Pile(PileLocation.HIDDEN, [])), Player(name='Firas Mourad', "
        "private_cards=Pile(PileLocation.PRIVATE, []), "
        "open_cards=Pile(PileLocation.OPEN, []), "
        "hidden_cards=Pile(PileLocation.HIDDEN, []))))")
