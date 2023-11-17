from dealer import Card
from enum import Enum


class Blind(Enum):
    NO_BLIND = 0
    SMALL_BLIND = 1
    BIG_BLIND = 2


class Status(Enum):
    ACTIVE = 0
    FOLDED = 1
    ALL_IN = 2
    SITTING_OUT = 3


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.current_blind = None
        self.status = None

    def receive_card(self, card: Card) -> None:
        """
        Adds a card to the player's hand
        
        Args:
            card (Card): Card to be added to player's hand
        """
        assert len(self.hand) < 2, "Player cannot have more than 2 cards"
        self.hand.append(card)

    def set_blind(self, blind: Blind) -> None:
        """
        Sets the player's current blind
        
        Args:
            blind (Blinds): Blind to be set
        """
        self.current_blind = blind

    def set_status(self, status: Status) -> None:
        """
        Sets the player's current status
        
        Args:
            status (Status): Status to be set
        """
        self.status = status

    def bet(self, amount: int) -> bool:
        """
        Bets the given amount from the player's balance

        Args:
            amount (int): Amount to bet

        Returns:
            bool: True if bet was successful, False if not
        """
        if self.balance >= amount:
            self.balance -= amount
            if self.balance == 0:
                self.set_status(Status.ALL_IN)
            return True
        return False
    
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
