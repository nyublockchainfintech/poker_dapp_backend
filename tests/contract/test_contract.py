from typing import Dict, List, Tuple

from poker_dapp_backend.contract.connection import PokerGameTables


def test_connect_to_contract(contract_connection: PokerGameTables):
    """
    Check that connecting to a contract returns a contract object
    """
    assert isinstance(contract_connection, PokerGameTables)


def test_call_getTable(contract_connection:PokerGameTables):
    """
    Check the getTable function returns the correct result
    """
    table_number = 1
    output = contract_connection.get_table(table_number)
    assert isinstance(output, Tuple)
    assert len(output) == 8
    assert isinstance(output[7], List)
    assert len(output[7]) == output[2]  # Length of players list == player count

def test_call_getAllTables(contract_connection:PokerGameTables):
    """
    Check the getTable function returns the correct result
    """
    output = contract_connection.get_all_tables()
    print(output)


def test_serialize_game_table(contract_connection: PokerGameTables):
    """
    Check the getTable function returns the correct result
    """
    table_number = 1
    game_table = contract_connection
    data = game_table.get_table(table_number)
    output = game_table.game_tuple_to_dict(data)
    assert isinstance(output, Dict)
    assert len(output) == 8
    assert isinstance(players := output.get("players"), List)
    assert len(players) == output.get("playerLimit")
