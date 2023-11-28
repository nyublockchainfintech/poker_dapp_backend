import secrets
import base64
import random
from typing import Dict, List

from poker_dapp_backend.base import Cards
from .encryption import symencrypt
from poker_dapp_backend.enums import (
    ClientResponse,
    DealerResponse,
)


class PlayerBase(Cards):
    def seed_gen(self, size=1000000) -> int:
        """
        Generate a random seed of the given size

        Args:
            size (int): Size of the seed

        Returns:
            int: Random seed of the given size
        """
        return secrets.randbelow(size)

    def keygen1(self, length=256) -> str:
        """
        Generate a random key of the given length

        Args:
            length (int): Length of the key in bits

        Returns:
            str: Random key of the given length
        """
        # Generate a secure random number of the given bit length
        key = secrets.randbits(length)
        # Convert to binary format and remove the '0b' prefix
        binary_key = bin(key)[2:].zfill(length)
        return binary_key

    def keygen2(self, n=52, length=256) -> List[str]:
        """
        Generate n random keys of the given length

        Args:
            n (int): Number of keys to generate
            length (int): Length of each key in bits

        Returns:
            List[str]: List of random keys of the given length
        """
        keys = set()

        while len(keys) < n:
            new_key = self.keygen1(length)
            keys.add(new_key)

        return list(keys)


class Player(PlayerBase):
    def __init__(self, websocket_server) -> None:
        self.websocket = websocket_server
        self.command: ClientResponse | DealerResponse = ClientResponse.DOING_NOTHING
        self.cards: List[bytes] = []
        self.shuffle_seed = self.seed_gen(size=1000000)
        self.identical_keys = [self.keygen1(length=256)] * 52
        self.unique_keys = self.keygen2(length=256)

    def shuffle_deck(self):
        """
        Shuffle the entire deck of cards
        """
        # Shuffle with seed
        random.seed(self.shuffle_seed)
        random.shuffle(self.cards)

    def bytes_to_string_list(self) -> List[str]:
        """
        Convert deck of cards from List[bytes] to List[str]

        Returns:
            List[str]: List of cards converted to string
        """
        return [base64.b64encode(card).decode("utf-8") for card in self.cards]

    def string_to_bytes_list(self, cards: List[str]) -> List[bytes]:
        """
        Convert deck of cards from List[str] to List[bytes]

        Args:
            cards (List[str]): List of cards to convert

        Returns:
            List[bytes]: List of cards converted to bytes
        """
        if set(cards) == set(self.init_deck()):
            return [card.encode("utf-8") for card in cards]
        else:
            return [base64.b64decode(card) for card in cards]

    def serialize(self) -> Dict:
        """
        Serialize the entire deck of cards

        Args:
            command (ClientResponse): Command to send to the server

        Returns:
            Dict: Serialized deck of cards
        """
        return {
            "command": self.command,
            "content": self.bytes_to_string_list(),
        }

    def deserialize(self, data: Dict):
        """
        Deserialize the server response

        Args:
            data (Dict): Server response
        """
        try:
            self.command = data["command"]
            self.cards = self.string_to_bytes_list(data["content"])
        except KeyError as e:
            raise ValueError(f"Invalid data format: {e}")
        return self

    def encrypt_deck(self, cards=None, individually=False, keys=None) -> List[bytes]:
        """
        Encrypt the entire deck of cards with player key(s)

        Args:
            cards (List[bytes]): List of cards to encrypt
            individually (bool): Encrypt each card with a different key
            keys (List[str]): List of keys to use for encryption

        Returns:
            List[str]: List of encrypted cards
        """
        if not cards:
            cards = self.cards
        if not keys:
            keys = self.unique_keys if individually else self.identical_keys
        self.cards = [symencrypt(k.encode(), c) for k, c in zip(keys, cards)]
        return self.cards

    def decrypt_deck(self, cards=None, individually=False, keys=None) -> List[bytes]:
        """
        Decrypt the entire deck of cards with player key(s)

        Args:
            cards (List[bytes]): List of cards to decrypt
            individually (bool): Decrypt each card with a different key
            keys (List[str]): List of keys to use for decryption

        Returns:
            List[str]: List of decrypted cards
        """
        # NOTE: Symmetric encryption is reversible
        return self.encrypt_deck(individually=individually, keys=keys)

    # FIXME: Currently broken
    async def reply(self, message: dict):
        """
        Reply to the server with the correct response
        """
        if message is None:
            raise ValueError("No message received")

        # string to json
        try:
            command = message["command"]
            self.cards = message["content"]
            if command == DealerResponse.SHUFFLE:
                pass
            elif command == DealerResponse.DECRYPT:
                pass
            elif command == DealerResponse.DEAL:
                pass
            elif command == DealerResponse.KEYS:
                pass
            else:
                # Handle unknown or unsupported commands
                pass
        except KeyError:
            # TODO: Replace this with error handler
            raise KeyError("Invalid data format")

    # async def send_to_server(self, response_type: ClientResponse):
    #     """
    #     Send a message to the server with the given response type
    #     """
    #     message = json.dumps(
    #         {
    #             "status": WebSocketStatus.SUCCESS.value,
    #             "command": response_type.value,
    #             "content": self.output,
    #         }
    #     )
    #     await self.websocket.send(message)
