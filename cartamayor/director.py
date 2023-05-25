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
