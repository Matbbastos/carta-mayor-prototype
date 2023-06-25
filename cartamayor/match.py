from __future__ import annotations

import logging
import random
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime

from common.classes import Card, Pile, Player, PileLocation
from common.constants import INITIAL_PILE_SIZES
from common.types import GameMode


@dataclass
class Match:
    """
    A match which has a Game Mode, players (in teams or not), a deck of Cards, start and end
    times and is controlled by the Director module.

    Parameters:
        game_mode (GameMode): Game mode, as detailed in 'types' module.
        initiative_queue (deque[Player]): queue of players to control order of play.
        deck (list[Card]): full deck of cards to be used for the game.
        table_pile (Pile): pile of cards in the table for the match.
        dead_pile (Pile): pile of dead cards, removed from the game.
        control_flags (dict[str, bool]): control flags used for the Match.
        started_at (datetime | None): starting timestamp of the match, naive datetime.
        ended_at (datetime | None): ending timestamp of the match, naive datetime.
    """
    game_mode: GameMode
    initiative_queue: deque[Player]
    deck: list[Card]
    table_pile: Pile
    dead_pile: Pile
    started_at: datetime | None = None
    ended_at: datetime | None = None
    control_flags: dict[str, bool] = field(
        default_factory=lambda: dict(show_previous_play=False))

    def __str__(self) -> str:
        started_str = "not started"
        if self.started_at is not None:
            started_str = f"""started at {self.started_at.strftime("%Y-%m-%d %Hh%M")}"""
        return (
            f"{' '.join(self.game_mode.name.split('_'))} {started_str} - "
            f"[{', '.join(player.name for player in self.initiative_queue)}] - "
            f"Top table card: {self.table_pile[-1]} - # Dead: {len(self.dead_pile)}")

    def deal(self) -> Match:
        """
        Shuffle deck, then deal cards to the players (private, open and hidden), according
        to the game mode.

        Fatal Three Way: 7 private, 5 open and 5 hidden
        Full Monty: 5 private, 4 open and 4 hidden.
        Note: Deck is not emptied for shuffling.
        """
        random.shuffle(self.deck)
        logging.debug(f"Initial deck order: {', '.join(str(card) for card in self.deck)}")

        last_hidden_index = 0
        for index, player in enumerate(self.initiative_queue):
            last_private_index = index + INITIAL_PILE_SIZES[
                self.game_mode][PileLocation.PRIVATE]
            last_open_index = last_private_index + INITIAL_PILE_SIZES[
                self.game_mode][PileLocation.OPEN]
            last_hidden_index = last_open_index + INITIAL_PILE_SIZES[
                self.game_mode][PileLocation.HIDDEN]

            player.private_cards.extend(self.deck[index:last_private_index])
            player.open_cards.extend(self.deck[last_private_index:last_open_index])
            player.hidden_cards.extend(self.deck[last_open_index:last_hidden_index])

        last_dead_index = last_hidden_index + INITIAL_PILE_SIZES[
            self.game_mode].get(PileLocation.DEAD, 0)
        self.dead_pile.extend(self.deck[last_hidden_index:last_dead_index])

        return self

    def auto_bambam(self) -> Match:
        """
        Perform an automatic bam-bam phase and thus set the starting initiative queue for
        the match.
        """
        # TODO: implement, really
        return self

    def start(self) -> Match:
        """
        Set starting attributes and execute auto-bambam.
        """
        # TODO: implement starting function
        self.started_at = datetime.now()
        self.auto_bambam()
        return self
