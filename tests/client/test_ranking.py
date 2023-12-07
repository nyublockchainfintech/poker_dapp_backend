
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
