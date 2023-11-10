import random
import json
from pokerlib.enums import Rank, Suit


class Card:
    # Build a card class
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def serialize(self) -> dict:
        return {"rank": self.rank.value, "suit": self.suit.value}

    def deserialize(self, data: dict) -> None:
        self.rank = Rank(data["rank"])
        self.suit = Suit(data["suit"])


class Deck:
    # Build a deck class
    def __init__(self) -> None:
        self.cards = []
        self.build()

    def build(self) -> None:
        # Build a deck of cards
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        # Shuffle the deck
        random.shuffle(self.cards)

    def draw(self) -> Card:
        # Draw a card from the deck
        return self.cards.pop()

    def serialize(self) -> dict:
        return {"cards": [card.serialize() for card in self.cards]}

    def deserialize(self, data: dict) -> None:
        self.cards = []
        for card in data["cards"]:
            new_card = Card(Rank(card["rank"]), Suit(card["suit"]))
            self.cards.append(new_card)
