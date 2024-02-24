import os
from collections import deque
from datetime import datetime

from cartamayor.common.classes import Card, Player
from cartamayor.common.constants import PILE_COUNTER_LIMIT
from cartamayor.common.types import GameMode


def welcome_users() -> None:
    print("Hello there, stranger! Ready to play?")


def prompt_for_game_mode() -> str:
    print(
        '''Type "FTW" for a Fatal Three Way match, or "FM" for a Full Monty, '''
        '''then hit "Enter"''')
    game_mode = input("> ")
    if game_mode not in {"FTW", "FM"}:
        print("Oops, let's try that again..")
        return prompt_for_game_mode()
    return game_mode


def prompt_for_FTW_players() -> list[str]:
    player_names = []
    print("Please, provide the name of the first player")
    player_names.append(input("> "))

    print("Please, provide a different name for the second player")
    new_name = input("> ")
    if new_name == player_names[0]:
        print(f"Now that's not different, is it? We'll save it as '{new_name} Duplus'")
    player_names.append(f"{new_name} Duplus")

    print("Please, provide a different name for the third player")
    new_name = input("> ")
    if new_name in player_names:
        print(f"Now that's not different, is it? We'll save it as '{new_name} Tertius'")
    player_names.append(f"{new_name} Tertius")

    return player_names


def prompt_for_FM_teams() -> dict[str, tuple[str, str]]:
    teams = {}
    print("Please, provide the name of the 1st team")
    first_team_name = input("> ")

    player_names = []
    print(f"Please, provide the name of the 1st player from team '{first_team_name}'")
    player_names.append(input("> "))

    print(
        f"Please, provide a different name for the 2nd player from team "
        f"'{first_team_name}'")
    new_name = input("> ")
    if new_name == player_names[0]:
        print(f"Now that's not different, is it? We'll save it as '{new_name} Duplus'")
        new_name = f"{new_name} Duplus"
    player_names.append(new_name)

    teams[first_team_name] = tuple(player_names[0:2])

    print("Please, provide the name of the 2nd team")
    second_team_name = input("> ")
    if second_team_name == first_team_name:
        print(
            f"The teams can't have the same name, you know that, right? We'll save it as "
            f"'{second_team_name} (1)'")
        second_team_name = f"{second_team_name} (1)"

    print(f"Please, provide the name of the 1st player from team '{second_team_name}'")
    player_names.append(input("> "))

    print(
        f"Please, provide a different name for the 2nd player from team "
        f"'{second_team_name}'")
    new_name = input("> ")
    if new_name == player_names[2]:
        print(f"Now that's not different, is it? We'll save it as '{new_name} Duplus'")
        new_name = f"{new_name} Duplus"
    player_names.append(new_name)

    teams[second_team_name] = tuple(player_names[2:])

    print(
        f"""So we'll have a match between teams '{first_team_name}' ("""
        f"""{" & ".join(str(name) for name in teams[first_team_name])}) and """
        f"""'{second_team_name}' """
        f"""({" & ".join(str(name) for name in teams[second_team_name])}), """
        f"""is that right? (Y/n)""")
    confirmation = input("> ")
    if confirmation.casefold() == "n":
        print(
            "No problem, let's try it again from the top.. "
            "(it's your time we're wasting, anyway)\n")
        return prompt_for_FM_teams()
    return teams


def clear_viewport(clearance=1.2) -> None:
    """
    Attempt to clear the current terminal window by printing linebreaks to equal the
    current window height.

    Args:
        clearance (float, optional): Enlarging factor to provide more clearance of the
        viewport. Defaults to 1.2. Values smaller than 1 will be set to 1.
    """
    clearance = max(1, clearance)
    terminal_height = os.get_terminal_size()[1]
    print("\n"*round(terminal_height*clearance))


def show_player_state(player: Player) -> None:
    print(player.open_cards)
    print(player.hidden_cards.masked())
    print(player.private_cards)


def detailed_player_state(player: Player) -> None:
    """
    Display a detailed state for the player, with all piles and their cards.

    Result will be similar to:

    Source: OPEN
    │     OPEN: ♢4, ♢5, ♡6, ♠7
    │   HIDDEN:  ▇  ▇  ▇  ▇
    │  PRIVATE: ♡4, ♣5, ♠6, ♡7, ♠10, ♣7
    └───────────────────────────────────┘

    Args:
        player (Player): Player who owns the cards.
    """
    source_name = player.get_source().location.name.upper()
    rows_to_print = {
        "SOURCE": f"Source: {source_name}",
        "OPEN": "│     OPEN: ",
        "HIDDEN": "│   HIDDEN:  ",
        "PRIVATE": "│  PRIVATE: ",
        "BOTTOM_RULE": "└───────────",
    }
    rows_to_print["OPEN"] += ", ".join(str(card) for card in player.open_cards)
    rows_to_print["HIDDEN"] += "  ".join("▇" for _ in player.hidden_cards)
    rows_to_print["PRIVATE"] += ", ".join(str(card) for card in player.private_cards)

    extra_rulers = (
        max([
            len(rows_to_print["SOURCE"]),
            len(rows_to_print["OPEN"]),
            len(rows_to_print["HIDDEN"]),
            len(rows_to_print["PRIVATE"])])
        - len(rows_to_print["BOTTOM_RULE"]) + 1)
    rows_to_print["BOTTOM_RULE"] += "─"*extra_rulers + "┘"
    for row in rows_to_print.values():
        print(row.rstrip())


def get_table_display_details(
        table_details: tuple[int, list[Card | None]],
        dead_pile_length: int) -> tuple[str, list[str], str]:
    """
    Transform the table information into content ready to be displayed.

    Args:
        table_details (tuple[int, list[Card  |  None]]): Details from the current table pile
    coming from the Director.
        dead_pile_length (int): amount of cards in the dead pile.

    Returns:
        tuple[str, list[str], str]: Table pile length display string along with a list of
        the display string for each visible card, and the dead pile counter string.
    """
    table_pile_length, visible_cards = table_details
    table_pile_counter = f"={table_pile_length}"
    if table_pile_length > PILE_COUNTER_LIMIT:
        table_pile_counter = f"+{PILE_COUNTER_LIMIT}"
    dead_pile_counter = f"={dead_pile_length}"
    if dead_pile_length > PILE_COUNTER_LIMIT:
        dead_pile_counter = f"+{PILE_COUNTER_LIMIT}"
    result = [str(item) if item is not None else "▇" for item in visible_cards]
    return (table_pile_counter, result, dead_pile_counter)


def show_table(
        table_pile_details: tuple[int, list[Card | None]],
        dead_pile_length: int) -> None:
    table_pile_size, cards_to_display, dead_pile_size = get_table_display_details(
        table_pile_details, dead_pile_length)
    JUSTIFY_MARGIN = 9
    display_lines = [
        "┌────────────────────────────┐",
        f"│       TABLE ({table_pile_size}): {cards_to_display[0].ljust(JUSTIFY_MARGIN)}│"
        ]
    for card in cards_to_display[1:-1]:
        display_lines.append(f"│         ┆         {card.ljust(JUSTIFY_MARGIN)}│")
    display_lines.extend([
        f"│         └         {cards_to_display[-1].ljust(JUSTIFY_MARGIN)}│",
        "└────────────────────────────┘",
        f"           DEAD ({dead_pile_size})"
        ])
    print("\n".join(display_lines))


def trim_long_string(string: str, max_length: int) -> str:
    """
    Trims a string to a maximum length and adds trailing ellipsis (3 dots).
    Note: if max_length < 3, an empty string is returned (not enought space for ellipsis).

    Args:
        string (str): String to be trimmed.
        max_length (int): Final length after trimming and adding ellipsis.

    Returns:
        str: Original string trimmed to the maximum length, having the last 3 characters as
        an ellipsis.
    """
    if max_length < 3:
        return ""
    if len(string) > max_length:
        return f"{string[:max_length-3]}..."
    return string


def show_match_status(
        initiative_queue: deque[Player], game_mode: GameMode, start_time: datetime) -> None:
    """
    Print the status of the current match, with game mode, when it started and player queue.

    Result will be similar to:
    ┌────────────────────────────────────┐
    │            MATCH STATUS            │
    │ FULL MONTY                         │
    │   Started at 2023-12-31 23:59:59   │
    │                                    │
    │   Now playing:                     │
    │        ╰ Player One                │
    │   Next:  ╰ Player Two              │
    │            ╰ Player Three          │
    │              ╰ Player Four         │
    └────────────────────────────────────┘

    Args:
        initiative_queue (deque[Player]): Initiative queue of players from the match.
        game_mode (GameMode): Current game mode of the match.
        start_time (datetime): Time at which the match was started.
    """
    game_mode_str = ' '.join(game_mode.name.split('_'))
    display_lines = [
        "┌────────────────────────────────────┐",
        "│            MATCH STATUS            │",
        f"│ {game_mode_str.ljust(35)}│",
        f"│   Started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}   │",
        "│                                    │",
        "│   Now playing:                     │",
        f"│        ╰ {trim_long_string(initiative_queue[0].name, 25).ljust(26)}│",
        f"│   Next:  ╰ {trim_long_string(initiative_queue[1].name, 23).ljust(24)}│",
        f"│            ╰ {trim_long_string(initiative_queue[2].name, 21).ljust(22)}│"
    ]
    if game_mode == GameMode.FULL_MONTY:
        display_lines.append(
            f"│              ╰ {trim_long_string(initiative_queue[3].name, 19).ljust(20)}│")
    display_lines.append("└────────────────────────────────────┘")
    print("\n".join(display_lines))
