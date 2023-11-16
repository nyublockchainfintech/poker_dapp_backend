from typing import List
import json
from pokerlib.enums import Rank, Suit
from poker_dapp_backend.enums import ShuffleStage, WebSocketStatus


class Card:
    RANKS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A")
    SUITS = ("s", "c", "d", "h")

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

    def __str__(self) -> str:
        return self.rank.name + " of " + self.suit.name


class Dealer:
    def __init__(self) -> None:
        self.decoded_cards = []
        self.encoded_cards = []
        self.build()
        self.encode()

    # TODO: This deck initialization should use smart contracts
    def build(self) -> None:
        """
        Build a deck of Card objects
        """
        for suit in Suit:
            for rank in Rank:
                self.decoded_cards.append(Card(rank, suit))

    def encode(self):
        """Encode the deck of cards to a list of strings"""
        for cards in self.decoded_cards:
            self.encoded_cards.append(cards.encode())

    def serialize(self) -> str:
        """
        Serialize the deck of cards to a dictionary

        Returns:
            dict: Dictionary representation of the deck of cards
        """
        message = {
            "command": ShuffleStage.START,
            "data": self.encoded_cards,
        }
        return json.dumps(message)

    def __str__(self) -> str:
        return "".join(self.encoded_cards)


if __name__ == "__main__":
    # 1. Init dealer class and pass serialized deck to player
    # 2. Player receives deck and deserializes it
    # 3. Player encrypts deck with key
    # 4. Player shuffles deck
    # 5. Player serializes and sends deck to dealer
    pass
