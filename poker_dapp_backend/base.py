from typing import List
from pokerlib.enums import Rank, Suit
from itertools import product


class CardBase:
    RANKS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A")
    SUITS = ("s", "c", "d", "h")

    def init_deck(self) -> List[str]:
        """
        Return a list of a deck of cards
        """

        return [f"{rank}{suit}" for rank, suit in product(self.RANKS, self.SUITS)]


class Card(CardBase):
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def encode(self) -> str:
        """
        Convert the card to a binary string

        Returns:
            str: Encoded card
        """
        return self.RANKS[self.rank.value] + self.SUITS[self.suit.value]
    
    @classmethod
    def init_deck(cls):
        """
        Return a list of a deck of cards
        """
        return [Card(rank, suit) for rank, suit in product(Rank, Suit)]

    def __str__(self) -> str:
        return f"{self.rank.name} of {self.suit.name}"
