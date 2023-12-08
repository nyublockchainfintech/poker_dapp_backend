
from poker_dapp_backend.server.ranking import Ranker
from poker_dapp_backend.server.dealer import Card
from pokerlib.enums import Rank, Suit

def test_ranker():
    """
    Tests the ranker method of a Ranker object
    """
    ranker = Ranker()
    # test ranking a royal flush
    hand = [
        Card(Rank.ACE, Suit.SPADE),
        Card(Rank.KING, Suit.SPADE),
    ]
    community_cards = [
        Card(Rank.QUEEN, Suit.SPADE),
        Card(Rank.JACK, Suit.SPADE),
        Card(Rank.TEN, Suit.SPADE),
    ]
    assert ranker.rank(hand, community_cards) == 1
    # test ranking a straight flush (9 to K)
    hand = [
        Card(Rank.NINE, Suit.SPADE),
        Card(Rank.KING, Suit.SPADE),
    ]
    community_cards = [
        Card(Rank.QUEEN, Suit.SPADE),
        Card(Rank.JACK, Suit.SPADE),
        Card(Rank.TEN, Suit.SPADE),
    ]
    assert ranker.rank(hand, community_cards) == 2

    hand_1 = [
        Card(Rank.ACE, Suit.SPADE),
        Card(Rank.KING, Suit.SPADE),
    ]
    hand_2 = [
        Card(Rank.ACE, Suit.HEART),
        Card(Rank.KING, Suit.HEART),
    ]
    community_cards = [
        Card(Rank.QUEEN, Suit.SPADE),
        Card(Rank.JACK, Suit.SPADE),
        Card(Rank.TEN, Suit.SPADE),
    ]
    best_hand = ranker.best_hand([hand_1, hand_2], community_cards)
    assert best_hand == 0

    hand_1 = [
        Card(Rank.ACE, Suit.SPADE),
        Card(Rank.KING, Suit.SPADE),
    ]
    hand_2 = [
        Card(Rank.ACE, Suit.HEART),
        Card(Rank.KING, Suit.HEART),
    ]
    hand_3 = [
        Card(Rank.ACE, Suit.DIAMOND),
        Card(Rank.KING, Suit.DIAMOND),
    ]
    # community card for 3 to get a flush
    community_cards = [
        Card(Rank.QUEEN, Suit.DIAMOND),
        Card(Rank.JACK, Suit.DIAMOND),
        Card(Rank.TEN, Suit.DIAMOND),
    ]
    best_hand = ranker.best_hand([hand_1, hand_2, hand_3], community_cards)
    assert best_hand == 2
