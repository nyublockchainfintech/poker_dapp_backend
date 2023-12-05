from poker_dapp_backend.base import Cards
from poker_dapp_backend.server.player import Player, Blind, Status
from poker_dapp_backend.server.ranking import Ranker
from poker_dapp_backend.enums import BettingRound
from random import shuffle as default_shuffle


"""
Game Attr:
- Players: list[Player]
- Blinds: tuple(small: int, big: int)
- Current Pot: int
- Current Betting Round: enum.Betting_Round

"""

class Game:

    def __init__(self, buy_in: int, blinds: tuple[int, int], players: list[Player] = None, max_players: int = 8):
        self.buy_in = buy_in
        self.players = players
        self.small_blind = blinds[0]
        self.big_blind = blinds[1]
        self.current_dealer = 0 
        self.current_small = 1
        self.current_big = 2
        self.active_player = 3
        self.current_round = 0
        self.current_pot = 0
        self.max_players = max_players
        self.deck = []
        self.ranker = Ranker()
        self.games_played = 0

    def add_player(self, name: str, balance: int) -> bool:
        """
        Adds a player to the game. 

        args:
            Player: player to add to game

        returns:
            bool: True if added
                  False if not added
        """
        # if table full, don't add player and return False
        if len(self.players) >= self.max_players:
            return False
        # otherwise, create player with params and return True
        player = Player(name, balance)
        self.players.append(player)
        return True
    
    def start_game(self) -> bool:
        """
        Starts the game by assigning blinds, dealing cards, and setting current_round and current_player

        returns:
            True if game successfully started
            False if not 
        """
        # make sure there's enough players to start game
        if len(self.players) < 2:
            return False
        
        # increment blinds if not first round
        if self.games_played > 0:
            self.current_small = (self.current_small + 1) % len(self.players)
            self.current_big = (self.current_big + 1) % len(self.players)

        # set active player to player after big blind
        self.active_player = (self.current_big + 1) % len(self.players)

        # initialize deck and shuffle
        self.deck: list = Cards.init_deck() # typehint so VSCode stops being annoying
        default_shuffle(self.deck)

        # deal cards
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.pop())

        # set betting round to pre_flop
        self.current_round = BettingRound.PRE_FLOP
        
        


