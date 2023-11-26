import secrets
from typing import List
import random
import json

from websockets import Data, WebSocketClientProtocol
from .encryption import symencrypt
from poker_dapp_backend.enums import ClientResponse, WebSocketStatus, DealerResponse


class PlayerBase:
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

    def encrypt_decrypt(self):
        """
        Decrypt the entire deck of cards with the given key & encrypt them again
        with the list of keys
        """
        # Decrypt Cards
        key = self.stage_1_key.encode()
        self.output = [symencrypt(key, card.encode()).decode() for card in self.input]

        # Encrypt with keys
        self.output = [
            symencrypt(key.encode(), card.encode()).decode()
            for key, card in zip(self.stage_2_keys, self.output)
        ]

    async def reply(self, message: dict):
        """
        Reply to the server with the correct response
        """
        if message is None:
            raise ValueError("No message received")

        # string to json
        try:
            command = message["command"]
            self.input = message["content"]
            print(command)
            print(self.input)
            if command == DealerResponse.SHUFFLE:
                self.shuffle_encrypt()
                await self.send_to_server(ClientResponse.SHUFFLED)
            elif command == DealerResponse.DECRYPT:
                self.encrypt_decrypt()
                await self.send_to_server(ClientResponse.DECRYPTED)
            elif command == DealerResponse.DEAL:
                # Implement deal logic if required
                pass
            elif command == DealerResponse.KEYS:
                # Implement keys handling logic if required
                pass
            else:
                # Handle unknown or unsupported commands
                pass
        except KeyError:
            # TODO: Replace this with error handler
            raise KeyError("Invalid data format")

    async def send_to_server(self, response_type: ClientResponse):
        """
        Send a message to the server with the given response type
        """
        message = json.dumps(
            {
                "status": WebSocketStatus.SUCCESS.value,
                "response": response_type.value,
                "content": self.output
            }
        )
        await self.websocket.send(message)
