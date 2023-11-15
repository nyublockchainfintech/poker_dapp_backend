import treys
import cards

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

    def _convert(self, card: cards.Card) -> str:
        """
        Convert a card from pokerlib format to treys format.

        Args:
            card (Card): Card to convert

        Returns:
            str: Converted card
        """
        # NOTE: might have issue here since some pokerlib versions use value instead of rank
        return self.rank_dict[card.value.name] + self.suit_dict[card.suit.name]
    
    def rank(self, hand: list[cards.Card], board: list[cards.Card]) -> int:
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
