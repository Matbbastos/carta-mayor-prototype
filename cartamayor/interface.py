def welcome_users() -> None:
    print("Hello there, stranger! Ready to play?")


def prompt_for_game_mode() -> str:
    print(
        """Type "FTW" for a Fatal Three Way match, or "FM" for a Full Monty, """
        """then hit "Enter""")
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
