from poker_dapp_backend.server.player import Player, Blind, Status
from pokerlib.enums import Rank, Suit
from poker_dapp_backend.server.dealer import Card
import json


def test_player_init():
    """
    Tests the initialization of a Player object
    """
    player = Player(name="test", balance=100)
    assert player.name == "test"
    assert player.balance == 100
    assert player.hand == []
    assert player.current_blind == None
    assert player.status == None


def test_player_receive_card():
    """
    Tests the receive_card method of a Player object
    """
    player = Player(name="test", balance=100)
    # test adding a card to an empty hand
    player.receive_card(Card(Rank.ACE, Suit.SPADE))
    assert len(player.hand) == 1
    assert player.hand[0].rank == Rank.ACE
    assert player.hand[0].suit == Suit.SPADE
    # test adding a card to a hand with 1 card
    player.receive_card(Card(Rank.KING, Suit.SPADE))
    assert len(player.hand) == 2
    assert player.hand[1].rank == Rank.KING
    assert player.hand[1].suit == Suit.SPADE
    # test adding a card to a hand with 2 cards (make sure it throws an error)
    try:
        player.receive_card(Card(Rank.QUEEN, Suit.SPADE))
    except AssertionError:
        assert True
    else:
        assert False


def test_player_set_blind():
    """
    Tests the set_blind method of a Player object
    """
    player = Player(name="test", balance=100)
    # test setting a blind
    player.set_blind(Blind.SMALL_BLIND)
    assert player.current_blind == Blind.SMALL_BLIND
    # test setting a different blind
    player.set_blind(Blind.BIG_BLIND)
    assert player.current_blind == Blind.BIG_BLIND


def test_player_set_status():
    """
    Tests the set_status method of a Player object
    """
    player = Player(name="test", balance=100)
    # test setting a status
    player.set_status(Status.ACTIVE)
    assert player.status == Status.ACTIVE
    # test setting a different status
    player.set_status(Status.FOLDED)
    assert player.status == Status.FOLDED


def test_player_hand_to_string():
    """
    Tests the hand_to_string method of a Player object
    """
    player = Player(name="test", balance=100)
    # test converting an empty hand to a string
    assert player.hand_to_string() == ""
    # test converting a hand with 1 card to a string
    player.receive_card(Card(Rank.ACE, Suit.SPADE))
    assert player.hand_to_string() == "As"
    # test converting a hand with 2 cards to a string
    player.receive_card(Card(Rank.KING, Suit.SPADE))
    assert player.hand_to_string() == "As Ks"


def test_bet():
    """
    Tests the bet method of a Player object
    """
    player = Player(name="test", balance=100)
    # test betting an amount less than the player's balance
    player.bet(50)
    assert player.balance == 50
    # test betting an amount equal to the player's balance
    player.bet(50)
    assert player.balance == 0
    assert player.status == Status.ALL_IN
    # test betting an amount greater than the player's balance (make sure it throws an error)
    try:
        player.bet(1)
    except AssertionError:
        assert True
    else:
        assert False


def test_fold():
    """
    Tests the fold method of a Player object
    """
    player = Player(name="test", balance=100)
    # test folding
    player.fold()
    assert player.status == Status.FOLDED
    # set status back to active
    player.set_status(Status.ACTIVE)
    # deal cards and test to make sure the player's hand is empty after folding
    player.receive_card(Card(Rank.ACE, Suit.SPADE))
    player.receive_card(Card(Rank.KING, Suit.SPADE))
    player.fold()
    assert player.hand == []


def test_serialize():
    """
    Tests the serialize method of a Player object
    """
    player = Player(name="test", balance=100)
    # test serializing a player with no cards
    serialized_player = player.serialize()
    print(serialized_player)
    serialized_player = json.loads(serialized_player)
    assert serialized_player["name"] == "test"
    assert serialized_player["balance"] == 100
    assert serialized_player["hand"] == []
    assert serialized_player["current_blind"] == None
    assert serialized_player["status"] == None
    # test serializing a player with 1 card
    player.receive_card(Card(Rank.ACE, Suit.SPADE))
    serialized_player = player.serialize()
    print(serialized_player)
    serialized_player = json.loads(serialized_player)
    assert serialized_player["name"] == "test"
    assert serialized_player["balance"] == 100
    assert serialized_player["hand"] == ["As"]
    assert serialized_player["current_blind"] == None
    assert serialized_player["status"] == None
    # test serializing a player with 2 cards
    player.receive_card(Card(Rank.KING, Suit.SPADE))
    serialized_player = player.serialize()
    print(serialized_player)
    serialized_player = json.loads(serialized_player)
    assert serialized_player["name"] == "test"
    assert serialized_player["balance"] == 100
    assert serialized_player["hand"] == ["As", "Ks"]
    assert serialized_player["current_blind"] == None
    assert serialized_player["status"] == None
    # test serializing a player with a blind
    player.set_blind(Blind.SMALL_BLIND)
    serialized_player = player.serialize()
    print(serialized_player)
    serialized_player = json.loads(serialized_player)
    assert serialized_player["name"] == "test"
    assert serialized_player["balance"] == 100
    assert serialized_player["hand"] == ["As", "Ks"]
    assert serialized_player["current_blind"] == "SMALL_BLIND"
    assert serialized_player["status"] == None
    # test serializing a player with a status
    player.set_status(Status.ACTIVE)
    serialized_player = player.serialize()
    print(serialized_player)
    serialized_player = json.loads(serialized_player)
    assert serialized_player["name"] == "test"
    assert serialized_player["balance"] == 100
    assert serialized_player["hand"] == ["As", "Ks"]
    assert serialized_player["current_blind"] == "SMALL_BLIND"
    assert serialized_player["status"] == "ACTIVE"


# run this test by running the following command in the terminal:
# python -m pytest tests/server/test_player.py
