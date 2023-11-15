import random
import json
from pokerlib.enums import Value, Suit


class Card:
    def __init__(self, value: Value, suit: Suit) -> None:
        self.value = value
        self.suit = suit

    def serialize(self) -> dict:
        """
        Return a dictionary of the card object
        """
        return {"value": self.value.value, "suit": self.suit.value}

    def deserialize(self, data: dict) -> None:
        """
        Deserialize a card from a dictionary
        """
        self.value = Value(data["value"])
        self.suit = Suit(data["suit"])

    def encrypt(self, key):
        """
        Encrypt the card
        """
        pass

    def encode(self) -> str:
        """
        Convert the card to a binary string

        Returns:
            str: Binary string representation of the card
        """
        value = bin(self.value.value)[2:].zfill(4)
        suit = bin(self.suit.value)[2:].zfill(2)
        return value + suit  # Length of 6

    def __str__(self) -> str:
        return self.value.name + " of " + self.suit.name


class Deck:
    def __init__(self) -> None:
        self.cards = []
        self.build()

    def build(self) -> None:
        """
        Build a deck of cards from Suit and Value enums
        """
        for suit in Suit:
            for value in Value:
                self.cards.append(Card(value, suit))

    def encode(self) -> str:
        """
        Convert the deck of cards to a binary string

        Returns:
            str: Binary string representation of the deck of cards
        """
        return "".join([card.encode() for card in self.cards])

    def decode(self, data: str) -> None:
        """
        Decode a deck of cards from a binary string

        Args:
            data (str): Binary string representation of the deck of cards
        """
        self.cards = []
        for i in range(0, len(data), 6):
            card = Card(
                Value(int(data[i : i + 4], 2)), Suit(int(data[i + 4 : i + 6], 2))
            )
            self.cards.append(card)

    def encrypt(self):
        """
        Encrypt the deck of cards
        """
        # TODO: Implement encryption
        pass

    def shuffle(self, seed: int) -> None:
        """
        Shuffle the deck of cards with a seed

        Args:
            seed (int): Seed for the random number generator
        """
        random.seed(seed)
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """
        Draw a card from the deck
        """
        return self.cards.pop()

    # TODO: Change this to use the encoded value
    def serialize(self) -> dict:
        """
        Return a dictionary of the deck of cards
        """
        return {"cards": [card.serialize() for card in self.cards]}

    def deserialize(self, data: dict) -> None:
        """
        Deserialize a deck of cards from a dictionary
        """
        self.cards = []
        for card in data["cards"]:
            new_card = Card(Value(card["value"]), Suit(card["suit"]))
            self.cards.append(new_card)

    def __str__(self) -> str:
        return "\n".join([str(card) for card in self.cards])


if __name__ == "__main__":
    deck = Deck()
    print(deck)
    deck.shuffle(42)
    print(deck.encode())
