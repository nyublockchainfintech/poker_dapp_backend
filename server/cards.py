from typing import List
import random
import json
from pokerlib.enums import Rank, Suit
from mapping import encode_rank, encode_suit
#from encryption import symencrypt


class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def encode(self) -> str:
        """
        Convert the card to a binary string

        Returns:
            str: Encoded card
        """
        return encode_rank(self.rank.value) + encode_suit(self.suit.value)

    def __str__(self) -> str:
        return self.rank.name + " of " + self.suit.name
    
class Deck:
    def __init__(self) -> None:
        self.cards = []
        self.build()

    def build(self) -> None:
        """
        Build a deck of cards from Suit and Rank enums
        """
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

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
                Rank(int(data[i : i + 4], 2)), Suit(int(data[i + 4 : i + 6], 2))
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
            new_card = Card(Rank(card["rank"]), Suit(card["suit"]))
            self.cards.append(new_card)

    def __str__(self) -> str:
        return "\n".join([str(card) for card in self.cards])

class Dealer:
    def __init__(self) -> None:
        self.decoded_cards = []
        self.encoded_cards = ""
        self.build()
        self.encode()

    def build(self) -> None:
        """
        Build a deck of encoded cards
        """
        for suit in Suit:
            for rank in Rank:
                self.decoded_cards.append(Card(rank, suit))

    def encode(self):
        """
        Encode the deck of cards to a list of binary strings

        Returns:
            List[bytes]: List of binary strings representing the deck of cards
        """
        self.encoded_cards = "".join(card.encode() for card in self.decoded_cards)

    def serialize(self) -> str:
        """
        Serialize the deck of cards to a dictionary

        Returns:
            dict: Dictionary representation of the deck of cards
        """
        return json.dumps({"encoded_deck": self.encoded_cards})

    def __str__(self) -> str:
        return "\n".join([str(card) for card in self.decoded_cards])


class Player:
    def __init__(self) -> None:
        self.input_cards = []
        self.encrypted_cards = []
        self.output_cards = []
        self.encoded_cards = ""
        self.shuffle_round = False
        self.decrypt_round = False

    def shuffle(self, seed: int) -> None:
        """
        Shuffle the deck of cards with a seed

        Args:
            seed (int): Seed for the random number generator
        """
        random.seed(seed)
        random.shuffle(self.encrypted_cards)

    def encrypt(self, key: bytes):
        """
        Encrypt the entire deck of cards
        """
        self.encrypted_cards = []
        for card in self.input_cards:
            self.encrypted_cards.append(symencrypt(card.encode("utf-8"), key))

    def decrypt(self, key: bytes):
        """
        Decrypt the entire deck of cards
        """
        self.encrypt(key)

    def encode(self):
        """
        Conver the list of bytes to a binary string
        """
        self.encoded_cards = "".join(
            [card.decode("utf-8") for card in self.encrypted_cards]
        )

    def decode(self):
        """
        Convert the binary string to a list of card bytes
        """
        pass


if __name__ == "__main__":
    dealer = Dealer()
    print(dealer.encoded_cards)
    player = Player()
    player.input_cards = dealer.encoded_cards
    player.encrypt(b"12345")
    print(player.encrypted_cards)
    player.shuffle(1)
    print(player.encrypted_cards)
    player.encode()
    # TODO: Finish this!
