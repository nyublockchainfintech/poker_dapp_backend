from typing import Dict, List, Tuple
import collections
from web3 import Web3
from web3.contract.contract import Contract


class PokerGame:
    def __init__(
        self,
        id=None,
        minBuyIn=None,
        playerLimit=None,
        playerCount=None,
        inPlay=None,
        initiator=None,
        amountInPlay=None,
    ):
        self.id = id
        self.minBuyIn = minBuyIn
        self.playerLimit = playerLimit
        self.playerCount = playerCount
        self.inPlay = inPlay
        self.initiator = initiator
        self.amountInPlay = amountInPlay

    @classmethod
    def deserialize(cls, data):
        try:
            return cls(
                id=data["id"],
                minBuyIn=data["minBuyIn"],
                playerLimit=data["playerLimit"],
                playerCount=data["playerCount"],
                inPlay=data["inPlay"],
                initiator=data["initiator"],
                amountInPlay=data["amountInPlay"],
            )
        except KeyError as e:
            raise ValueError(f"Invalid game data: {data}") from e


class PokerGameTables(Contract):
    def __init__(self, web3, address, abi):
        self.contract = web3.eth.contract(address=address, abi=abi)
        self.room_to_players = collections.defaultdict(set)
        self.game_metadata = collections.defaultdict(PokerGame)
        self.player_to_room = collections.defaultdict(int)

    @classmethod
    def connect_to_contract(cls, rpc_url, contract_address, contract_abi):
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        address = web3.to_checksum_address(contract_address)
        return cls(web3, address, contract_abi)

    def get_table(self, table_number) -> Tuple:
        return self.contract.functions.getTable(table_number).call()

    def get_all_tables(self) -> List[Tuple]:
        return self.contract.functions.getAllTables().call()

    def deserialize_all_tables(self, tables: List[tuple]):
        """
        Deserialize all tables from the contract and store them in the class

        Args:
            tables (List[tuple]): List of tuples representing the game tables
        """
        for table in tables:
            data = self.game_tuple_to_dict(table)
            self._deserialize_table_players(data)
            self._deserialize_table_metadata(data)  # NOTE: Order matters here

    def _deserialize_table_players(self, data: Dict):
        """
        Assigns sets of players to room numbers and maps players to room numbers

        Args:
            data (Dict): Dictionary representing the game table
        """
        for player in data["players"]:
            self.player_to_room[player] = data["id"]
        self.room_to_players[data["id"]].update(data["players"])

    def _deserialize_table_metadata(self, data: Dict):
        """
        Deserialize a single game table from the contract

        Args:
            data (Dict): Dictionary representing the game table
        """
        self.game_metadata[data["id"]] = PokerGame.deserialize(data)

    def get_player_game_id(self, data: Dict) -> int:
        """
        Get the room number for a given player
        """
        return self.player_to_room[data["PLAYER_ADDRESS"]]

    @staticmethod
    def game_tuple_to_dict(data: Tuple) -> Dict:
        """
        Convert a tuple representing a game table to a dictionary

        Args:
            data (Tuple): Tuple representing a game table

        Returns:
            Dict: Dictionary representing a game table
        """
        field_names = (
            "id",
            "minBuyIn",
            "playerLimit",
            "playerCount",
            "inPlay",
            "initiator",
            "amountInPlay",
            "players",
        )
        return dict(zip(field_names, data))
