from poker_dapp_backend.base import Card
from poker_dapp_backend.client.players import ShufflePlayer


def test_shuffle_encrypt(two_player_game):
    """
    Test the first stage of mental poker where:
    1. For each player in the game
    -  Encrypt the deck with one key
    -  Shuffle the deck
    -  Send the encrypted deck to the next player
    """
    ws1, ws2, _, p2_msg1 = two_player_game

    p2 = ShufflePlayer(ws2)
    p1 = ShufflePlayer(ws1)

    # SHUFFLE & ENCRYPT

    p2.deserialize(p2_msg1)
    initial_cards = p2.cards
    p2.encrypt_deck()
    p2.shuffle_deck()
    msg = p2.serialize()

    p1.deserialize(msg)
    p1.encrypt_deck()
    p1.shuffle_deck()
    msg = p1.serialize()

    # DECRYPT & ENCRYPT

    p2.deserialize(msg)
    p2.decrypt_deck()
    p2.encrypt_deck(individually=True)
    msg = p2.serialize()

    p1.deserialize(msg)
    p1.decrypt_deck()
    p1.encrypt_deck(individually=True)
    msg = p1.serialize()

    # DEAL CARDS
    p2.deserialize(msg)
    p2.decrypt_deck(individually=True)
    msg = p2.serialize()

    p1.deserialize(msg)
    p1.decrypt_deck(individually=True)
    print(p1.cards)
    msg = p1.serialize()

    assert set(p1.cards) == set(initial_cards)
