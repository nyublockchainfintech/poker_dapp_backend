import treys
import cards
import random

deck = cards.Deck()

board = []
for _ in range(5):
    board.append(random.choice(deck.cards))

hand = []
for _ in range(2):
    hand.append(random.choice(deck.cards))

print(f"Board: {board[0]}, {board[1]}, {board[2]}, {board[3]}, {board[4]}\n")
print(f"Hand: {hand[0]}, {hand[1]}")
STR_RANKS: str = '23456789TJQKA'
STR_SUITS: str = 'shdc'
class Ranker:
    def __init__(self):
        self.evaluator = treys.Evaluator()
        # dictionaries to convert from pokerlib to treys format
        self.rankDict = {
            'TWO': '2',
            'THREE': '3',
            'FOUR': '4',
            'FIVE': '5',
            'SIX': '6',
            'SEVEN': '7',
            'EIGHT': '8',
            'NINE': '9',
            'TEN': 'T',
            'JACK': 'J',
            'QUEEN': 'Q',
            'KING': 'K',
            'ACE': 'A',
        }
        self.suitDict = {
            'SPADE': 's',
            'CLUB': 'c',
            'DIAMOND': 'd',
            'HEART': 'h',
        }

    def convert(self, card: cards.Card) -> str:
        """
        Convert a card from pokerlib format to treys format.

        Args:
            card (Card): Card to convert

        Returns:
            str: Converted card
        """
        # NOTE: might have issue here since some pokerlib versions use value instead of rank
        return self.rankDict[card.value.name] + self.suitDict[card.suit.name]
    
    def rank(self, hand: list[cards.Card], board: list[cards.Card]) -> int:
        """
        Rank the hand given the board. Takes in a list of pokerlib format cards.

        Returns:
            int: Rank of the hand
        """
        # convert the hand into treys card objects
        hand = [treys.Card.new(self.convert(card)) for card in hand]
        # convert the board from pokerlib to treys
        board = [treys.Card.new(self.convert(card)) for card in board]
        
        # return the rank
        return self.evaluator.evaluate(board, hand)
