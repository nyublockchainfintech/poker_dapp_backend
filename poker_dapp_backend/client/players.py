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
    def __init__(self, websocket_server: WebSocketClientProtocol) -> None:
        self.websocket = websocket_server
        self.input = []
        self.output = []
        self.shuffle_seed = self.seed_gen()
        self.stage_1_key = self.keygen1()
        self.stage_2_keys = self.keygen2()

    def shuffle_encrypt(self) -> None:
        """
        Encrypt the entire deck of cards and shuffle them

        Args:
            seed (int): Seed for the random number generator
        """
        # Encrypt Cards
        key = self.stage_1_key.encode()
        self.ouput = [symencrypt(key, card.encode()).decode() for card in self.input]

        # Shuffle with seed
        random.seed(self.shuffle_seed)
        random.shuffle(self.output)

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
