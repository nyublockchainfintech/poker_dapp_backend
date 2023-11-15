import cards
from ranking import Ranker
import random

deck = cards.Deck()

# generate a random board and hand and print out the rank of the hand
board = []
for _ in range(5):
    board.append(random.choice(deck.cards))

hand = []
for _ in range(2):
    hand.append(random.choice(deck.cards))

print(f"Board: {board[0]}, {board[1]}, {board[2]}, {board[3]}, {board[4]}\n")
print(f"Hand: {hand[0]}, {hand[1]}")

rank = Ranker().rank(hand, board)
print(f"Rank: {rank}")

# generate royal flush and assert it is the highest rank
royal_flush = [cards.Card(cards.Value.ACE, cards.Suit.SPADE), cards.Card(cards.Value.KING, cards.Suit.SPADE), cards.Card(cards.Value.QUEEN, cards.Suit.SPADE)]
hand = [cards.Card(cards.Value.JACK, cards.Suit.SPADE), cards.Card(cards.Value.TEN, cards.Suit.SPADE)]
rank = Ranker().rank(hand, royal_flush)
print(f"Royal flush rank: {rank}")
assert rank == 1, f"Royal flush should be rank 1, got {rank}"

# generate straight flush (nine to queen) and assert it is the second highest rank
straight_flush = [cards.Card(cards.Value.NINE, cards.Suit.SPADE), cards.Card(cards.Value.TEN, cards.Suit.SPADE), cards.Card(cards.Value.JACK, cards.Suit.SPADE)]
hand = [cards.Card(cards.Value.QUEEN, cards.Suit.SPADE), cards.Card(cards.Value.KING, cards.Suit.SPADE)]
rank = Ranker().rank(hand, straight_flush)
print(f"Straight flush rank: {rank}")
assert rank == 2, f"Straight flush should be rank 2, got {rank}"

# generate four of a kind (aces) and assert it is the 11th highest rank (while it is third best hand, treys includes all possible straight flushes (of which there are 9) as ranks 2-10))
four_of_a_kind = [cards.Card(cards.Value.ACE, cards.Suit.SPADE), cards.Card(cards.Value.ACE, cards.Suit.CLUB), cards.Card(cards.Value.KING, cards.Suit.DIAMOND)]
hand = [cards.Card(cards.Value.ACE, cards.Suit.HEART), cards.Card(cards.Value.ACE, cards.Suit.DIAMOND)]
rank = Ranker().rank(hand, four_of_a_kind)
print(f"Four of a kind rank: {rank}")
assert rank == 11, f"Four of a kind should be rank 3, got {rank}"
