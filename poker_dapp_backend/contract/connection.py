from typing import Dict, Tuple
from web3 import Web3
from web3.contract.contract import Contract


class GameTable(Contract):
    def __init__(self, web3, address, abi):
        self.contract = web3.eth.contract(address=address, abi=abi)

    @classmethod
    def connect_to_contract(cls, rpc_url, contract_address, contract_abi):
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        address = web3.to_checksum_address(contract_address)
        return cls(web3, address, contract_abi)

    def get_table(self, table_number):
        return self.contract.functions.getTable(table_number).call()

    @staticmethod
    def serialize_game_table(data: Tuple) -> Dict:
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
