from typing import List
import json
from pokerlib.enums import Rank, Suit
from poker_dapp_backend.enums import DealerResponse, ClientResponse, WebSocketStatus


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
    """
    Dealer class that handles the deck of cards and shuffling
    """

    min_players = 2

    def __init__(self, connected_players: set) -> None:
        self.cards = []
        self.shuffle_players = set()
        self.connected_players = connected_players
        self.messsage = {}
        self.initialize_deck()

    def initialize_deck(self) -> None:
        """
        Build a deck of Card objects
        """
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit).encode())

    def start_shuffle(self):
        """
        Start the shuffle by sending the deck of cards to a random player
        """
        self.shuffle_players = set(self.connected_players)
        self.message = {
            "command": DealerResponse.SHUFFLE,
            "content": self.cards,
            "message": "Start shuffling",
        }

    def decrypt(self, data: dict, start=False):
        """
        Start the decrypt process by sending the deck of cards to a random player
        """
        if start:
            self.shuffle_players = set(self.connected_players)
        encrypted_cards = data["content"]
        self.message = {
            "command": DealerResponse.DECRYPT,
            "content": encrypted_cards,
            "message": "Decrypt and reencrypt the deck",
        }

    def waiting(self):
        """
        Wait for more players to join
        """
        self.message = {
            "command": DealerResponse.WAIT,
            "message": "Waiting for more players to join",
        }

    def deal(self, data: dict):
        """
        Deal the cards to all players
        """
        encrypted_cards = data["content"]
        self.message = {
            "command": DealerResponse.DEAL,
            "content": encrypted_cards,
            "message": "Deal the cards",
        }

    def shuffle(self, data: dict):
        """
        Given shuffled cards, send them to the next player
        """
        try:
            self.message = {
                "command": DealerResponse.SHUFFLE,
                "content": data["content"],
                "message": "Shuffle the deck",
            }
        except KeyError:
            # TODO: Handle error
            pass

    async def reply(self, message: dict):
        """
        Reply with the correct shuffle stage given a command
        """
        try:
            command = message["command"]
            if command == ClientResponse.JOIN:
                if len(self.connected_players) >= self.min_players:
                    self.start_shuffle()
                    await self.send_deck()
                else:
                    self.waiting()
                    await self.broadcast()
            elif command == ClientResponse.SHUFFLED:
                if len(self.shuffle_players) > 0:
                    self.shuffle(message)
                    await self.send_deck()
                else:
                    self.decrypt(message)
                    await self.send_deck()
            elif command == ClientResponse.DECRYPTED:
                if len(self.shuffle_players) > 0:
                    self.decrypt(message)
                    await self.send_deck()
                else:
                    self.deal(message)
                    await self.broadcast()
            else:
                await self.broadcast(
                    {
                        "status": WebSocketStatus.ERROR.value,
                        "message": "Unknown command",
                    }
                )
        except KeyError:
            await self.broadcast(
                {
                    "status": WebSocketStatus.ERROR.value,
                    "message": "Missing command",
                }
            )

    async def send_deck(self, message: dict | None = None):
        """
        Send a message to a random player
        """
        if message is None:
            message = self.message
        await self.shuffle_players.pop().send_json(message)

    async def broadcast(self, message: dict | None = None):
        """
        Broadcast a message to all connected clients.
        """
        if message is None:
            message = self.message

        disconnected_clients = set()
        for client in self.connected_players:
            try:
                await client.send_json(message)
            except Exception:
                disconnected_clients.add(client)
        for client in disconnected_clients:
            self.connected_players.remove(client)

    def serialize(self) -> dict:
        """
        Serialize the deck of cards to a JSON object
        """
        return self.messsage


# 0. Once all the clients join, we start the game
# 1. When the game starts, we send the deck of cards to a random player
# 2. The player shuffles the deck and sends it back to the dealer
# 3. The dealer sends the deck to the next player
# 4. After the last player shuffles the deck, the dealer starts the decrypt process
# 5. The dealer sends the deck to a random player to decrypt
# 6. After the last player decrypts, the dealer broadcasts the deck to all players
