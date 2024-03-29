from cartamayor.common.classes import Card, Pile
from cartamayor.common.types import PileLocation, Suit


def test_pile_print(open_pile: Pile, private_pile: Pile) -> None:
    assert str(open_pile) == "(OPEN)    Pile[♢4, ♢5, ♡6, ♠7]"
    assert str(private_pile) == "(PRIVATE) Pile[♣2, ♢3, ♡10, ♠A, ♣4]"

    assert repr(open_pile) == (
        """Pile(PileLocation.OPEN, [Card(label='4', suit=Suit.DIAMONDS), """
        """Card(label='5', suit=Suit.DIAMONDS), """
        """Card(label='6', suit=Suit.HEARTS), """
        """Card(label='7', suit=Suit.SPADES)])""")
    assert repr(private_pile) == (
        """Pile(PileLocation.PRIVATE, [Card(label='2', suit=Suit.CLUBS), """
        """Card(label='3', suit=Suit.DIAMONDS), """
        """Card(label='10', suit=Suit.HEARTS), """
        """Card(label='A', suit=Suit.SPADES), """
        """Card(label='4', suit=Suit.CLUBS)])""")


def test_pile_locations(private_pile: Pile, open_pile: Pile, hidden_pile: Pile) -> None:
    assert private_pile.pop() == Card("4", Suit.CLUBS)
    assert open_pile.popleft() == Card("4", Suit.DIAMONDS)
    assert hidden_pile.pop() == Card("K", Suit.SPADES)


def test_pile_equality() -> None:
    open_pile = Pile(PileLocation.OPEN, [Card("4", Suit.CLUBS), Card("K", Suit.SPADES)])
    private_pile = Pile(
        PileLocation.PRIVATE, [Card("4", Suit.CLUBS), Card("K", Suit.SPADES)])
    assert open_pile != private_pile

    another_open_pile = Pile(
        PileLocation.OPEN, [Card("4", Suit.CLUBS), Card("K", Suit.SPADES)])
    assert open_pile == another_open_pile


def test_pile_playability(private_pile: Pile, open_pile: Pile, table_pile: Pile) -> None:
    assert private_pile.contains_playable_card(table_pile)
    assert open_pile.contains_playable_card(table_pile)

    table_pile.append(Card("7", Suit.DIAMONDS))
    assert open_pile.contains_playable_card(table_pile)

    table_pile.append(Card("8", Suit.CLUBS))
    assert not open_pile.contains_playable_card(table_pile)

    empty_pile = Pile(PileLocation.TABLE)
    assert private_pile.contains_playable_card(empty_pile)
    assert open_pile.contains_playable_card(empty_pile)


def test_playable_cards_from_pile(
        private_pile: Pile, open_pile: Pile, table_pile: Pile) -> None:
    assert private_pile.get_playable_cards(table_pile) == {
        Card("2", Suit.CLUBS),
        Card("10", Suit.HEARTS),
        Card("A", Suit.SPADES)}

    assert open_pile.get_playable_cards(table_pile) == {
        Card("5", Suit.DIAMONDS),
        Card("6", Suit.HEARTS),
        Card("7", Suit.SPADES)}


def test_card_removal(private_pile: Pile) -> None:
    private_pile.remove_cards([Card("2", Suit.CLUBS), Card("3", Suit.DIAMONDS)])
    assert private_pile == Pile(PileLocation.PRIVATE, [
        Card("10", Suit.HEARTS), Card("A", Suit.SPADES), Card("4", Suit.CLUBS)])

    private_pile.remove_cards([Card("10", Suit.HEARTS), Card("A", Suit.SPADES)])
    assert private_pile == Pile(PileLocation.PRIVATE, [Card("4", Suit.CLUBS)])


def test_masking(hidden_pile: Pile, dead_pile: Pile) -> None:
    assert str(hidden_pile) == "(HIDDEN)  Pile[♡4, ♢8, ♠10, ♠K]"
    assert str(dead_pile) == "(DEAD)    Pile[♡2, ♠2, ♣9, ♡9, ♠9, ♢9]"

    assert str(hidden_pile.masked()) == "(HIDDEN)  Pile[▇, ▇, ▇, ▇]"
    assert str(dead_pile.masked()) == "(DEAD)    Pile[▇, ▇, ▇, ▇, ▇, ▇]"


def test_sorted_pile() -> None:
    p = Pile(
        PileLocation.PRIVATE,
        [
            Card("10", Suit.HEARTS),
            Card("3", Suit.DIAMONDS),
            Card("A", Suit.SPADES),
            Card("2", Suit.SPADES),
            Card("4", Suit.CLUBS)],
        sorted=True)
    assert str(p) == "(PRIVATE) Pile[♢3, ♣4, ♠A, ♡10, ♠2]"


def test_add_cards_to_sorted_pile() -> None:
    p = Pile(
        PileLocation.PRIVATE,
        [
            Card("10", Suit.HEARTS),
            Card("4", Suit.CLUBS)],
        sorted=True)
    p.add_cards([
        Card("3", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
        Card("A", Suit.SPADES),
    ])
    assert str(p) == "(PRIVATE) Pile[♢3, ♣4, ♠A, ♡10, ♠2]"
