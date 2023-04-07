"""
Defines the actions taken by the game Director in order for the match to unfold as expected
"""

import logging
from collections import deque

from common.classes import Card
from common.constants import CARD_LABELS
from common.types import Suit


def build_deck() -> deque[Card]:
    deck = deque()
    for suit in Suit:
        for label in CARD_LABELS:
            deck.append(Card(label, suit))
    logging.info(f"Successfully generated deck with {len(deck)} card(s)")
    return deck
