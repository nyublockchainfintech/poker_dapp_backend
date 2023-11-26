from typing import List
from pokerlib.enums import Rank, Suit
from itertools import product


class Cards:
    RANKS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A")
    SUITS = ("s", "c", "d", "h")

    def init_deck(self) -> List[str]:
        """
        Return a list of a deck of cards
        """

        return [f"{rank}{suit}" for rank, suit in product(self.RANKS, self.SUITS)]
