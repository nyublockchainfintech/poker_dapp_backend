from poker_dapp_backend.base import Card
from poker_dapp_backend.enums import DealerResponse, ClientResponse, WebSocketStatus
from pokerlib.enums import Rank, Suit


class Deck:
    def __init__(self) -> None:
        self.cards= []
        self.build()

    def build(self) -> None:
        """
        Build a deck of from Suit and Rank enums
        """
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))


class Dealer(Card):
    """
    Dealer class that handles the deck of cards and shuffling
    """

    min_players = 2

    def __init__(self, connected_players: set) -> None:
        self.cards = self.init_deck()
        self.shuffle_players = set()
        self.connected_players = connected_players
        self.command: ClientResponse | DealerResponse = DealerResponse.DOING_NOTHING
        self.message = {}

    # TODO: Figure out a way to collect keys for the right cards
    def collect_keys(self):
        """
        Collect the keys from all players
        """
        self.message = {
            "command": DealerResponse.KEYS,
            # "content": encrypted_cards, # index of the card to decrypt
            "message": "Collect the keys from all players",
        }

    def build_message(
        self,
        command: str,
        content: dict | list | None = None,
        message: str | None = None,
    ):
        """
        Build a response message
        """
        self.message = {
            "command": command,
            "content": content,
            "message": message,
        }

    async def reply(self, message: dict):
        """
        Reply with the correct shuffle stage given a command.
        """
        try:
            command = message["command"]
            handler = self.command_handlers.get(command, self.handle_unknown_command)
            await handler(message)
        except KeyError:
            await self.handle_missing_command()

    async def handle_join(self, message):
        if len(self.connected_players) >= self.min_players:
            self.shuffle_players = set(self.connected_players)
            await self.send_response(
                DealerResponse.SHUFFLE,
                self.cards,
                "Start shuffling the deck",
                broadcast=True,  # TODO: True for now, but false in a real game
            )
        else:
            await self.send_response(
                DealerResponse.WAIT,
                [],
                "Waiting for more players to join",
                broadcast=True,
            )

    async def handle_shuffled(self, message):
        if len(self.shuffle_players) > 0:
            await self.send_response(
                DealerResponse.SHUFFLE, message["content"], "Shuffle the deck"
            )
        else:
            self.shuffle_players = set(self.connected_players)
            await self.send_response(
                DealerResponse.DECRYPT, message["content"], "Decrypt the deck"
            )

    async def handle_decrypted(self, message):
        if len(self.shuffle_players) > 0:
            await self.send_response(
                DealerResponse.DECRYPT, message["content"], "Decrypt the deck"
            )
        else:
            await self.send_response(
                DealerResponse.DEAL,
                message["content"],
                "Deal the cards",
                broadcast=True,
            )

    async def handle_unknown_command(self, message):
        await self.broadcast(
            {
                "status": WebSocketStatus.ERROR.value,
                "message": "Unknown command",
            }
        )

    async def handle_missing_command(self):
        await self.broadcast(
            {
                "status": WebSocketStatus.ERROR.value,
                "message": "Missing command",
            }
        )

    async def send_response(self, response_type, content, message, broadcast=False):
        self.build_message(response_type, content, message)
        if broadcast:
            await self.broadcast()
        else:
            await self.send_to_player()

    @property
    def command_handlers(self):
        return {
            ClientResponse.JOIN: self.handle_join,
            ClientResponse.SHUFFLED: self.handle_shuffled,
            ClientResponse.DECRYPTED: self.handle_decrypted,
        }

    async def send_to_player(self, message: dict | None = None):
        """
        Send a message to a random player
        """
        if message is None:
            message = self.message
        # TODO: Handle error when the player is disconnected
        await self.shuffle_players.pop().send_json(message)

    async def broadcast(self, message: dict | None = None):
        """
        Broadcast a message to all connected clients.
        """
        if not message:
            message = self.message
        disconnected_clients = set()
        for client in self.connected_players:
            try:
                await client.send_json(message)
            except Exception:
                disconnected_clients.add(client)
        for client in disconnected_clients:
            self.connected_players.remove(client)
