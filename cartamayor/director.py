from __future__ import annotations

import logging
from collections import deque

from common.classes import Card, Pile, Player, Team
from common.constants import CARD_LABELS
from common.types import GameMode, PileLocation, Suit
from interface import prompt_for_game_mode, prompt_for_FTW_players, prompt_for_FM_teams
from match import Match


class Director:
    """
    Defines the actions taken by the game Director in order for the match to unfold as
    expected.
    """
    match: Match
    game_mode: GameMode
    teams: tuple[Team, Team] | None
    players: list[Player] | None

    @classmethod
    def build_deck(cls) -> list[Card]:
        """Builds the deck of cards to be used during the match.

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
        """Uses interface to define the game mode (Full Monty or Fatal Three Way).

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

    def _create_teams_and_players(self) -> None:
        """
        Uses interface to set team and player names, in order. Values are stored as
        Director attributes.

        Raises:
            AttributeError: If game mode is not correctly set.
        """
        if self.game_mode == GameMode.FATAL_THREE_WAY:
            self.teams = None
            self.players = [Player(name) for name in prompt_for_FTW_players()]
        elif self.game_mode == GameMode.FULL_MONTY:
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
        """Creates a match after selecting a game mode, players/teams and builing a deck.

        Returns:
            Match: New match to be controlled by the Director.
        """
        self.game_mode = self._select_game_mode()
        self._create_teams_and_players()
        return Match(
            self.game_mode,
            self._generate_initiative_queue(),
            self.build_deck(),
            Pile(PileLocation.TABLE),
            Pile(PileLocation.DEAD))

