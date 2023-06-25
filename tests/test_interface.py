from cartamayor.common.classes import Player, Card
from cartamayor.interface import (
    clear_viewport,
    get_table_display_details,
    prompt_for_game_mode,
    prompt_for_FM_teams,
    prompt_for_FTW_players,
    show_player_state,
    show_table,
    welcome_users,
    )


def test_welcome_screen(capsys) -> None:
    welcome_users()
    captured = capsys.readouterr()
    assert captured.out == "Hello there, stranger! Ready to play?\n"


def test_game_mode_prompt(monkeypatch, capsys) -> None:
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "FM")
        game_mode = prompt_for_game_mode()
    captured = capsys.readouterr()
    assert captured.out == (
        """Type "FTW" for a Fatal Three Way match, or "FM" for a Full Monty, """
        """then hit "Enter"\n""")
    assert game_mode == "FM"

    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "FTW")
        game_mode = prompt_for_game_mode()
    assert game_mode == "FTW"


def test_prompt_FTW_players(monkeypatch) -> None:
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "Test")
        players = prompt_for_FTW_players()
    assert players == ["Test", "Test Duplus", "Test Tertius"]


def test_prompt_FM_players(monkeypatch) -> None:
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "Test")
        players = prompt_for_FM_teams()
    assert players == {
        "Test": ("Test", "Test Duplus"),
        "Test (1)": ("Test", "Test Duplus")}


def test_clear_viewport(monkeypatch, capsys) -> None:
    with monkeypatch.context() as m:
        m.setattr("os.get_terminal_size", lambda: (120, 100))
        clear_viewport()
    captured = capsys.readouterr()
    assert captured.out == "\n"*120 + "\n"

    with monkeypatch.context() as m:
        m.setattr("os.get_terminal_size", lambda: (120, 100))
        clear_viewport(clearance=2)
    captured = capsys.readouterr()
    assert captured.out == "\n"*200 + "\n"

    with monkeypatch.context() as m:
        m.setattr("os.get_terminal_size", lambda: (120, 15))
        clear_viewport(clearance=0.5)
    captured = capsys.readouterr()
    assert captured.out == "\n"*15 + "\n"

    with monkeypatch.context() as m:
        m.setattr("os.get_terminal_size", lambda: (120, 45))
        clear_viewport(clearance=1.753)
    captured = capsys.readouterr()
    assert captured.out == "\n"*79 + "\n"


def test_show_player_state(capsys, player_with_cards: Player) -> None:
    show_player_state(player_with_cards)
    captured = capsys.readouterr()
    assert captured.out == (
        "(OPEN)    Pile[♢4, ♢5, ♡6, ♠7]\n"
        "(HIDDEN)  Pile[▇, ▇, ▇, ▇]\n"
        "(PRIVATE) Pile[♣2, ♢3, ♡10, ♠A, ♣4]\n")


def test_show_table(
        capsys,
        multiple_table_details: list[tuple[int, list[Card | None]]]) -> None:
    show_table(multiple_table_details[0], 0)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (=3): ♣3       │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (=0)\n")

    show_table(multiple_table_details[1], 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (=4): ♣3       │\n"
        "│         ┆         ♡2       │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (=1)\n")

    show_table(multiple_table_details[2], 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (=5): ♢10      │\n"
        "│         ┆         ♣10      │\n"
        "│         ┆         ♡2       │\n"
        "│         ┆         ♣2       │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (=2)\n")

    show_table(multiple_table_details[3], 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (+5): ♢10      │\n"
        "│         ┆         ♣10      │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (=3)\n")

    show_table(multiple_table_details[4], 4)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (+5): ♣3       │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (=4)\n")

    show_table(multiple_table_details[5], 5)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (+5): ♢3       │\n"
        "│         ┆         ♡3       │\n"
        "│         ┆         ♣3       │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (=5)\n")

    show_table(multiple_table_details[6], 6)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (+5): ♢2       │\n"
        "│         ┆         ♠2       │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (+5)\n")

    show_table(multiple_table_details[7], 7)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (+5): ♣2       │\n"
        "│         ┆         ♢2       │\n"
        "│         ┆         ♠2       │\n"
        "│         ┆         ▇        │\n"
        "│         ┆         ▇        │\n"
        "│         └         ▇        │\n"
        "└────────────────────────────┘\n"
        "           DEAD (+5)\n")

    show_table(multiple_table_details[8], 8)
    captured = capsys.readouterr()
    assert captured.out == (
        "┌────────────────────────────┐\n"
        "│       TABLE (+5): ♠9       │\n"
        "│         ┆         ♡9       │\n"
        "│         ┆         ♣9       │\n"
        "│         ┆         ♣2       │\n"
        "│         ┆         ♢2       │\n"
        "│         └         ♠2       │\n"
        "└────────────────────────────┘\n"
        "           DEAD (+5)\n")


def test_table_display_details(
        multiple_table_details: list[tuple[int, list[Card | None]]]) -> None:
    assert get_table_display_details(multiple_table_details[0], 0) == (
        "=3", ["♣3", "▇", "▇"], "=0")
    assert get_table_display_details(multiple_table_details[1], 1) == (
        "=4", ["♣3", "♡2", "▇", "▇"], "=1")
    assert get_table_display_details(multiple_table_details[2], 2) == (
        "=5", ["♢10", "♣10", "♡2", "♣2", "▇"], "=2")
    assert get_table_display_details(multiple_table_details[3], 3) == (
        "+5", ["♢10", "♣10", "▇", "▇", "▇", "▇"], "=3")
    assert get_table_display_details(multiple_table_details[4], 4) == (
        "+5", ["♣3", "▇", "▇", "▇", "▇", "▇"], "=4")
    assert get_table_display_details(multiple_table_details[5], 5) == (
        "+5", ["♢3", "♡3", "♣3", "▇", "▇", "▇"], "=5")
    assert get_table_display_details(multiple_table_details[6], 6) == (
        "+5", ["♢2", "♠2", "▇", "▇", "▇", "▇"], "+5")
    assert get_table_display_details(multiple_table_details[7], 7) == (
        "+5", ["♣2", "♢2", "♠2", "▇", "▇", "▇"], "+5")
    assert get_table_display_details(multiple_table_details[8], 8) == (
        "+5", ["♠9", "♡9", "♣9", "♣2", "♢2", "♠2"], "+5")
