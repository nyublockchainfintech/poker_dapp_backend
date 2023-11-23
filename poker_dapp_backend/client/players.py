from typing import List
import random
import json
from .encryption import symencrypt
from poker_dapp_backend.enums import ClientResponse, WebSocketStatus


class Player:
    def __init__(self) -> None:
        self.input_cards = []
        self.encrypted_cards: List[str] = []
        self.output_cards = []
        self.encoded_cards = []
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
            encrypted_card = symencrypt(card.encode(), key)
            self.encrypted_cards.append(encrypted_card.decode())

    def decrypt(self, key: bytes):
        """
        Decrypt the entire deck of cards
        """
        pass

    def serialize(self):
        """
        Serialize the deck of cards to a dictionary
        """
        return json.dumps(
            {
                "status": WebSocketStatus.SUCCESS,
                "result": self.encrypted_cards,
            }
        )

    def deserialize(self, data: str):
        """
        Deserialize the deck of cards from a dictionary
        """
        try:
            self.input_cards = json.loads(data)["cards"]
        except KeyError:
            raise KeyError("Invalid data format")
