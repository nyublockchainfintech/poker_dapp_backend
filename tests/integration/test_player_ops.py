from poker_dapp_backend.base import CardBase
from poker_dapp_backend.client.players import ShufflePlayer


# TODO: Write tests for string_to_bytes_list and bytes_to_string_list
def test_join(two_player_game):
    """
    Test server returns the correct response when two players join
    """
    _, _, p1_msg1, p2_msg1 = two_player_game

    cards = CardBase()
    assert p1_msg1.get("command") == "waiting"
    assert p1_msg1.get("content") == []

    assert p2_msg1.get("content") == cards.init_deck()
    assert p2_msg1.get("command") == "shuffle"


def test_shuffle_deck(two_player_game):
    """
    Test that players can shuffle the deck
    """
    _, ws2, _, p2_msg1 = two_player_game
    p2 = ShufflePlayer(ws2)
    p2.deserialize(p2_msg1)
    unshuffled_cards = p2.cards
    p2.shuffle_deck()

    assert p2.init_deck() != p2.cards
    assert len(p2.init_deck()) == len(p2.cards)
    assert set(unshuffled_cards) == set(p2.cards)


def test_deserialize(two_player_game):
    _, ws2, _, p2_msg1 = two_player_game
    p2 = ShufflePlayer(ws2)
    p2.deserialize(p2_msg1)
    assert p2.command == p2_msg1.get("command")
    assert p2.cards == p2.string_to_bytes_list(p2_msg1["content"])


def test_serialize(two_player_game):
    _, ws2, _, p2_msg1 = two_player_game
    p2 = ShufflePlayer(ws2)
    p2.deserialize(p2_msg1)
    msg = p2.serialize()
    assert msg["command"] == p2_msg1["command"]
    assert msg["content"] == p2.bytes_to_string_list()


def test_encrypt_deck(two_player_game):
    ws1, ws2, _, p2_msg1 = two_player_game

    p1 = ShufflePlayer(ws1)
    p1.deserialize(p2_msg1)
    p1_encrypted_cards = p1.encrypt_deck()

    p2 = ShufflePlayer(ws2)
    p2.deserialize(p2_msg1)
    p2_encrypted_cards = p2.encrypt_deck()

    assert len(p1_encrypted_cards) == len(p2_encrypted_cards)
    assert p1_encrypted_cards != p2_encrypted_cards
    assert all(isinstance(card, bytes) for card in p1_encrypted_cards)


def test_decrypt_deck(two_player_game):
    ws1, _, _, p2_msg1 = two_player_game

    p1 = ShufflePlayer(ws1)
    p1.deserialize(p2_msg1)
    unencrypted_cards = p1.cards
    encrypted_cards = p1.encrypt_deck()
    decrypted_cards = p1.decrypt_deck(encrypted_cards)

    assert unencrypted_cards == decrypted_cards
