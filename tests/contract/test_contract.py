from typing import Dict, List, Tuple

from poker_dapp_backend.contract.connection import GameTable


def test_connect_to_contract(contract_connection: GameTable):
    """
    Check that connecting to a contract returns a contract object
    """
    assert isinstance(contract_connection, GameTable)


def test_call_getTable(contract_connection):
    """
    Check the getTable function returns the correct result
    """
    table_number = 1
    output = contract_connection.get_table(table_number)
    assert isinstance(output, Tuple)
    assert len(output) == 8
    assert isinstance(output[7], List)
    assert len(output[7]) == output[2]  # Length of players list == player count


def test_serialize_game_table(contract_connection: GameTable):
    """
    Check the getTable function returns the correct result
    """
    table_number = 1
    game_table = contract_connection
    data = game_table.get_table(table_number)
    output = game_table.serialize_game_table(data)
    assert isinstance(output, Dict)
    assert len(output) == 8
    assert isinstance(players := output.get("players"), List)
    assert len(players) == output.get("playerLimit")
