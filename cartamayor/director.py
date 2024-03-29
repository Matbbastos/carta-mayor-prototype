from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass

from cartamayor.common.classes import Card, Pile, Player, Team
from cartamayor.common.constants import CARD_LABELS, MAX_VISIBLE_CARDS
from cartamayor.common.types import GameMode, PileLocation, Suit
from cartamayor.interface import prompt_for_game_mode, prompt_for_FTW_players, prompt_for_FM_teams
from cartamayor.match import Match


def check_match(func):
    def wrapper(director, *args, **kwargs):
        if director.match is None:
            logging.error(
                f"Attempted to call function '{func.__name__}' with no proper Match object")
            raise ValueError("Match must be set before using this function")
        return func(*args, **kwargs)
    return wrapper


@dataclass
class Director:
    """
    Define the actions taken by the game Director in order for the match to unfold as
    expected.

    Parameters:
        match (Match): match object to be controlled. Usually created after the Director.
        teams (tuple[Team, Team] | None): teams that will play (only for FULL_MONTY games).
        players (list[Player] | None): players that will play (not in teams, only for
            FATAL_THREE_WAY).
    """
    match: Match | None = None
    teams: tuple[Team, Team] | None = None
    players: list[Player] | None = None

    @classmethod
    def build_deck(cls) -> list[Card]:
        """Build the deck of cards to be used during the match.

        Returns:
            list[Card]: deck of 52 cards, ace to king from all 4 suits.
        """
        deck = []
        for suit in Suit:
            for label in CARD_LABELS:
                deck.append(Card(label, suit))
        logging.debug(f"Successfully generated deck with {len(deck)} card(s)")
        return deck

    def _select_game_mode(self) -> GameMode:
        """Use interface to define the game mode (Full Monty or Fatal Three Way).

        Raises:
            ValueError: If invalid game mode is selected.

        Returns:
            GameMode: Either FULL_MONTY or FATAL_THREE_WAY.
        """
        game_mode = prompt_for_game_mode()
        if game_mode == "FTW":
            logging.critical(
                "Fatal Three Way game mode hasn't been implemented yet, exiting")
            # TODO: implement FTW and return it here
            raise SystemExit
        elif game_mode == "FM":
            logging.info("Full Monty game mode selected")
            return GameMode.FULL_MONTY
        else:
            raise ValueError("Invalid Game Mode selected")

    def _create_teams_and_players(self, game_mode: GameMode) -> None:
        """
        Use interface to set team and player names, in order. Values are stored as
        Director attributes.

        Args:
            game_mode (GameMode): Selected game mode for the game.

        Raises:
            AttributeError: If game mode is not correctly set.
        """
        if game_mode == GameMode.FATAL_THREE_WAY:
            self.teams = None
            self.players = [Player(name) for name in prompt_for_FTW_players()]
        elif game_mode == GameMode.FULL_MONTY:
            self.players = None
            self.teams = tuple(
                Team(team_name, (Player(players[0]), Player(players[1])))
                for team_name, players in prompt_for_FM_teams().items())
        else:
            logging.warning("Attempted to create teams and players with no game mode set")
            raise AttributeError("Game Mode doesn't have a valid value")

    def _generate_initiative_queue(self) -> deque[Player]:
        """Use the team or players to create the initiative queue (relative positions).

        Raises:
            AttributeError: If both Players and Teams are None.

        Returns:
            deque[Player]: Deque of players, in order (intercalated teams, if any).
            Note: Absolute position is irrelevant until bam-bam is completed.
        """
        if self.players is not None:
            return deque(*self.players)
        elif self.teams is not None:
            return deque([
                self.teams[0].players[0],
                self.teams[1].players[0],
                self.teams[0].players[1],
                self.teams[1].players[1]])
        else:
            logging.warning("Attempted to generate initiative queue without proper setup")
            raise AttributeError("No valid Teams or Players found, both are None")

    def _create_match(self) -> Match:
        """Create a match after selecting a game mode, players/teams and builing a deck.

        Returns:
            Match: New match to be controlled by the Director.
        """
        game_mode = self._select_game_mode()
        self._create_teams_and_players(game_mode)
        return Match(
            game_mode,
            self._generate_initiative_queue(),
            self.build_deck(),
            Pile(PileLocation.TABLE),
            Pile(PileLocation.DEAD))

    def start_match(self) -> None:
        """Create the match object, then start it."""
        self.match = self._create_match()
        self.match.start()

    @check_match
    def get_next_player(self) -> Player:
        return self.match.initiative_queue[0]

    def get_table_pile_display(
            self, latest_play: list[Card | None]) -> tuple[int, list[Card | None]]:
        """
        Compute which cards from the table pile should be visible and the pile size, for
        diplay purposes.

        This function considers MAX_VISIBLE_CARDS constant for the maximum number of cards
        that can be displayed on the table at any point. This means that if less cards than
        that are to be displayed, the remaining will be filled with a "None" for each
        previous card in the pile (if any), until MAX_VISIBLE_CARDS is achieved (if
        possible).

        Note: This function assumes the pile was killed if that was supposed to happen. That
        is, the function assumes no grouping of 4 equally labeled cards are present in the
        pile.

        Args:
            latest_play (list[Card]): All cards that were played in the latest turn, in
            order of play.
            Note: it should only have more than 1 card if they have the same label.

        Returns:
            tuple[int, list[Card | None]]: length of the table pile and a list of the cards
            that should be visible. "None" replaces cards not visible that are below the
            MAX_VISIBLE_CARDS limit.
        """
        visible_cards: list[Card | None]
        visible_cards = latest_play[::-1]
        table_without_last_play = list(self.match.table_pile)[:-len(latest_play)]
        if self.match.control_flags["show_previous_play"]:
            for card in table_without_last_play[-1:-4:-1]:
                if card.label == "2":
                    visible_cards.append(card)
                else:
                    break
        else:
            for card in table_without_last_play[-1:-3:-1]:
                if card.label == visible_cards[0].label:
                    visible_cards.append(card)
        visibility = len(visible_cards)
        masked_table = list(self.match.table_pile)[:-visibility]
        if visibility < MAX_VISIBLE_CARDS:
            visible_cards.extend(
                [None]*min(len(masked_table), MAX_VISIBLE_CARDS-visibility))
        return (len(self.match.table_pile), visible_cards)

    def play_turn(self) -> None:
        """Play a turn of actions and apply the changes to the match."""
        pass

