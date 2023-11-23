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

    # TODO: Replace this with a secure random number generator
    def shuffle_encrypt(self, seed: int) -> None:
        """
        Encrypt the entire deck of cards and shuffle them

        Args:
            seed (int): Seed for the random number generator
        """
        # Encrypt Cards
        key = self.stage_1_key.encode()
        self.ouput = [symencrypt(key, card.encode()).decode() for card in self.input]

        # Shuffle with seed
        random.seed(seed)
        random.shuffle(self.output)

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
