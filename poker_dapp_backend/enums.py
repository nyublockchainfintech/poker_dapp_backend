from enum import Enum


class DealerResponse(str, Enum):
    WAIT = "waiting"
    SHUFFLE = "shuffle"
    DECRYPT = "decrypt"
    DEAL = "deal"
    KEYS = "keys"


class ClientResponse(str, Enum):
    JOIN = "join"
    SHUFFLED = "shuffled"
    DECRYPTED = "decrypted"


class WebSocketStatus(Enum):
    SUCCESS = 0
    ERROR = 1
