from enum import Enum


class DealerResponse(str, Enum):
    DOING_NOTHING = "doing_nothing"
    WAIT = "waiting"
    SHUFFLE = "shuffle"
    DECRYPT = "decrypt"
    DEAL = "deal"
    KEYS = "keys"


class ClientResponse(str, Enum):
    DOING_NOTHING = "doing_nothing"
    JOIN = "join"
    SHUFFLED = "shuffled"
    DECRYPTED = "decrypted"


class WebSocketStatus(Enum):
    SUCCESS = 0
    ERROR = 1

class BettingRound(Enum):
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4

    def next_round(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            raise ValueError("No next round available.")
        return members[index]
