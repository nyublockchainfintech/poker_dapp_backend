import json
from poker_dapp_backend.base import Card
from enum import Enum

class Status(Enum):
    ACTIVE = 0
    FOLDED = 1
    ALL_IN = 2
    SITTING_OUT = 3

class Player:
    def __init__(self, name=None, balance=0):
        self.name = name
        self.balance = balance
        self.hand = []
        self.status = None

    def receive_card(self, card: Card) -> None:
        """
        Adds a card to the player's hand
        
        Args:
            card (Card): Card to be added to player's hand
        """
        assert len(self.hand) < 2, "Player cannot have more than 2 cards"
        self.hand.append(card)

    def hand_to_string(self) -> str:
        """
        Converts the player's hand to a string
        
        Returns:
            str: String representation of the player's hand
        """
        # if the player has no cards, return an empty string
        if len(self.hand) == 0:
            return ""
        # if the player has 1 card, return the card
        elif len(self.hand) == 1:
            return self.hand[0].encode()
        # if the player has 2 cards, return the cards separated by a space
        else:
            return self.hand[0].encode() + " " + self.hand[1].encode()

    def set_status(self, status: Status) -> None:
        """
        Sets the player's current status
        
        Args:
            status (Status): Status to be set
        """
        self.status = status

    def bet(self, amount: int) -> None:
        """
        Bets the given amount from the player's balance

        Args:
            amount (int): Amount to bet
        """
        assert amount > 0, "Amount must be greater than 0"
        assert self.balance >= amount, "Player does not have enough money to bet that amount"
        self.balance -= amount
        if self.balance == 0:
            self.set_status(Status.ALL_IN)
            
    
    def fold(self) -> None:
        """
        Folds the player's hand
        """
        self.set_status(Status.FOLDED)
        self.hand = []

    def check(self) -> None:
        """
        Checks the player's hand
        """
        pass

    def sit_out(self) -> None:
        """
        Sits out the player
        """
        self.set_status(Status.SITTING_OUT)

    def rejoin(self) -> None:
        """
        Rejoins the player
        """
        self.set_status(Status.ACTIVE)

    def serialize(self) -> str:
        """
        Serializes the player's data

        Returns:
            str: Serialized player data in JSON format
        """
        to_json = {
            "name": self.name,
            "balance": self.balance,
            #"hand": [card.encode() for card in self.hand],
            "status": self.status.name if self.status else None,
        }
        # jsonify the data
        return json.dumps(to_json)
    
    def __str__(self) -> str:
        return f"{self.name} with ${self.balance} and hand {self.hand} is {self.status.name}"


