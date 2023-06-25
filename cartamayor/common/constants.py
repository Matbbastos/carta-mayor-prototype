import math
from common.types import CardStats, GameMode, PileLocation


MAX_VISIBLE_CARDS = 6

CARD_LABELS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

INITIAL_PILE_SIZES = {
    GameMode.FATAL_THREE_WAY: {
        PileLocation.PRIVATE: 7,
        PileLocation.OPEN: 5,
        PileLocation.HIDDEN: 5,
        PileLocation.DEAD: 1},
    GameMode.FULL_MONTY: {
        PileLocation.PRIVATE: 5,
        PileLocation.OPEN: 4,
        PileLocation.HIDDEN: 4}}


LABEL_TO_STATS = {
    "2": CardStats(power=math.inf, resistance=0),
    "3": CardStats(power=3, resistance=3),
    "4": CardStats(power=4, resistance=4),
    "5": CardStats(power=5, resistance=5),
    "6": CardStats(power=6, resistance=6),
    "7": CardStats(power=7, resistance=7),
    "8": CardStats(power=8, resistance=8),
    "9": CardStats(power=9, resistance=9),
    "10": CardStats(power=math.inf, resistance=0),
    "J": CardStats(power=11, resistance=11),
    "Q": CardStats(power=12, resistance=12),
    "K": CardStats(power=13, resistance=13),
    "A": CardStats(power=14, resistance=14)
}
