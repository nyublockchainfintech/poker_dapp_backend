from enum import Enum


class ShuffleStage(Enum):
    START = 0
    SHUFFLE = 1
    DECRYPT = 2


class WebSocketStatus(Enum):
    SUCCESS = 0
    ERROR = 1
