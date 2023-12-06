from poker_dapp_backend.server.dealer import Deck, Card
from pokerlib.enums import Rank, Suit
from poker_dapp_backend.server.ranking import Ranker

import random
import sys
from pathlib import Path

# Add the parent directory to sys.path to import modules from the parent directory
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)


deck = Deck()

board = [random.choice(deck.cards) for _ in range(5)]
hand = [random.choice(deck.cards) for _ in range(2)]
print(f"Board: {board[0]}, {board[1]}, {board[2]}, {board[3]}, {board[4]}\n")
print(f"Hand: {hand[0]}, {hand[1]}")

rank = Ranker().rank(hand, board)
print(f"Rank: {rank}")

# generate royal flush and assert it is the highest rank
royal_flush = [
    Card(Rank.ACE, Suit.SPADE),
    Card(Rank.KING, Suit.SPADE),
    Card(Rank.QUEEN, Suit.SPADE),
]
hand = [
    Card(Rank.JACK, Suit.SPADE),
    Card(Rank.TEN, Suit.SPADE),
]
rank = Ranker().rank(hand, royal_flush)
print(f"Royal flush rank: {rank}")
assert rank == 1, f"Royal flush should be rank 1, got {rank}"

# generate straight flush (nine to queen) and assert it is the second highest rank
straight_flush = [
    Card(Rank.NINE, Suit.SPADE),
    Card(Rank.TEN, Suit.SPADE),
    Card(Rank.JACK, Suit.SPADE),
]
hand = [
    Card(Rank.QUEEN, Suit.SPADE),
    Card(Rank.KING, Suit.SPADE),
]
rank = Ranker().rank(hand, straight_flush)
print(f"Straight flush rank: {rank}")
assert rank == 2, f"Straight flush should be rank 2, got {rank}"

# generate four of a kind (aces) and assert it is the 11th highest rank (while it is third best hand, treys includes all possible straight flushes (of which there are 9) as ranks 2-10))
four_of_a_kind = [
    Card(Rank.ACE, Suit.SPADE),
    Card(Rank.ACE, Suit.CLUB),
    Card(Rank.KING, Suit.DIAMOND),
]
hand = [
    Card(Rank.ACE, Suit.HEART),
    Card(Rank.ACE, Suit.DIAMOND),
]
rank = Ranker().rank(hand, four_of_a_kind)
print(f"Four of a kind rank: {rank}")
assert rank == 11, f"Four of a kind should be rank 3, got {rank}"

# generate multiple hands and assert that the right hand is chosen as the best hand
hand1 = [
    Card(Rank.ACE, Suit.SPADE),
    Card(Rank.ACE, Suit.CLUB),
]
hand2 = [
    Card(Rank.KING, Suit.DIAMOND),
    Card(Rank.KING, Suit.HEART),
]
hand3 = [
    Card(Rank.QUEEN, Suit.DIAMOND),
    Card(Rank.QUEEN, Suit.HEART),
]
hand4 = [
    Card(Rank.JACK, Suit.DIAMOND),
    Card(Rank.JACK, Suit.HEART),
]
# create board with 2 aces, a five, a six, and a eight
board = [
    Card(Rank.ACE, Suit.HEART),
    Card(Rank.ACE, Suit.DIAMOND),
    Card(Rank.FIVE, Suit.DIAMOND),
    Card(Rank.SIX, Suit.HEART),
    Card(Rank.EIGHT, Suit.CLUB),
]
hands = [hand1, hand2, hand3, hand4]
best_hand = Ranker().best_hand(hands, board)
print(f"Best hand: {best_hand}")
assert best_hand == 0, f"Best hand should be hand1, got {best_hand}"

# generate multiple hands and assert that the right hand is chosen as the best hand
hand1 = [
    Card(Rank.ACE, Suit.SPADE),
    Card(Rank.ACE, Suit.CLUB),
]
hand2 = [
    Card(Rank.KING, Suit.DIAMOND),
    Card(Rank.KING, Suit.HEART),
]
hand3 = [
    Card(Rank.QUEEN, Suit.DIAMOND),
    Card(Rank.QUEEN, Suit.HEART),
]
hand4 = [
    Card(Rank.JACK, Suit.DIAMOND),
    Card(Rank.JACK, Suit.HEART),
]
# create board with two kings, a five, a six, and a eight
board = [
    Card(Rank.KING, Suit.HEART),
    Card(Rank.KING, Suit.DIAMOND),
    Card(Rank.FIVE, Suit.DIAMOND),
    Card(Rank.SIX, Suit.HEART),
    Card(Rank.EIGHT, Suit.CLUB),
]
hands = [hand1, hand2, hand3, hand4]
best_hand = Ranker().best_hand(hands, board)
print(f"Best hand: {best_hand}")
assert best_hand == 1, f"Best hand should be hand2, got {best_hand}"

print("All tests passed!")
