import treys
from dealer import Card

class Ranker:
    def __init__(self):
        self.evaluator = treys.Evaluator()
        # dictionaries to convert from pokerlib to treys format
        self.rank_dict = {
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
        self.suit_dict = {
            'SPADE': 's',
            'CLUB': 'c',
            'DIAMOND': 'd',
            'HEART': 'h',
        }

    def _convert(self, card: Card) -> str:
        """
        Convert a card from pokerlib format to treys format.

        Args:
            card (Card): Card to convert

        Returns:
            str: Converted card
        """
        return self.rank_dict[card.rank.name] + self.suit_dict[card.suit.name]
    
    def rank(self, hand: list[Card], board: list[Card]) -> int:
        """
        Rank the hand given the board. Takes in a list of pokerlib format cards.

        Args:
            hand (list[cards.Card]): Hand to rank
            board (list[cards.Card]): Board to rank against

        Returns:
            int: Rank of the hand
        """
        # convert the hand into treys card objects
        hand = [treys.Card.new(self._convert(card)) for card in hand]
        # convert the board from pokerlib to treys
        board = [treys.Card.new(self._convert(card)) for card in board]
        
        # return the rank
        return self.evaluator.evaluate(board, hand)
    
    def best_hand(self, hands: list[list[Card]], board: list[int]) -> int:
        """
        Find the best hand given a list of hands and a board. Takes in a list of pokerlib format cards.
        
        Args:
            hands (list[list[card.Cards]]): Hands to rank
            board (list[int]): Board to rank against
            
        Returns:
            int: Index of the best hand
        """
        # create list with ranks of each hand
        ranks = [self.rank(hand, board) for hand in hands]

        # return the index of the best hand
        return ranks.index(min(ranks))
