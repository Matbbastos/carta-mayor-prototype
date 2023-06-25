import os
from common.classes import Card, Player
from common.constants import PILE_COUNTER_LIMIT


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


