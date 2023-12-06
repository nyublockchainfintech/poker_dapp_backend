from poker_dapp_backend.base import Cards
from poker_dapp_backend.server.player import Player, Blind, Status
from poker_dapp_backend.server.ranking import Ranker
from poker_dapp_backend.enums import BettingRound
from random import shuffle as default_shuffle
import json

class Game:

    def __init__(self, buy_in: int, blinds: tuple[int, int], players: list[Player] = None, max_players: int = 8):
        self.buy_in = buy_in
        self.players = players
        self.community_cards = []
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
        self.winner = None

    def add_player(self, name: str, starting_balance: int) -> bool:
        """
        Adds a player to the game. 

        args:
            name (str): name of player to add to game
            balance (int): starting balance of player

        returns:
            bool: True if added
                  False if not added
        """
        # if table full, don't add player and return False
        if len(self.players) >= self.max_players:
            return False
        # otherwise, create player with params and return True
        player = Player(name, starting_balance)
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

    def increment_round(self) -> None:
        """
        Increments to next betting round
        """
        if self.current_round == BettingRound.RIVER:
            raise ValueError("Can't go to next round, it is the river")
        self.current_round.next_round()
        # if it's the flop, deal 3 cards
        if self.current_round == BettingRound.FLOP:
            for _ in range(3):
                self.community_cards.append(self.deck.pop())
        # if it's the turn or river, deal 1 card
        elif self.current_round == BettingRound.TURN or self.current_round == BettingRound.RIVER:
            self.community_cards.append(self.deck.pop())

    def showdown(self) -> None:
        """
        Determines the winner of the game and sets the winner index and distributes pot
        """
        # get all hands if the player is not folded
        hands = []
        for player in self.players:
            if player.status == Status.ACTIVE or player.status == Status.ALL_IN:
                hands.append(player.hand)
        # get winner index
        self.winner = self.ranker.best_hand(hands, self.community_cards)
        # distribute pot
        self.players[self.winner].balance += self.current_pot

    def player_bet(self, player_index: int, bet_amount: int) -> None:
        """
        Adjusts game state when a player submits a bet

        Args:
            player_index (int): index of player that is making a bet
            bet_amount (int): amount that player is betting
        """
        assert player_index == self.active_player, "illegal bet argument, bet not from active player"
        self.players[player_index].bet(bet_amount)
        self.active_player = (self.active_player + 1) % len(self.players)

    def player_check(self, player_index: int) -> None:
        """
        Adjusts game state when a player checks

        Args:
            player_index (int): index of player that is checking
        """
        assert player_index == self.active_player, "illegal check argument, check not from active player"
        self.players[player_index].check()
        self.active_player = (self.active_player + 1) % len(self.players)
    
    def player_fold(self, player_index: int) -> None:
        """
        Adjusts game state when a player folds

        Args:
            player_index (int): index of player that is folding
        """
        assert player_index == self.active_player, "illegal fold argument, check not from active player"
        self.players[player_index].fold()
        self.active_player = (self.active_player + 1) % len(self.players)

    def player_sitting_out(self, player_index: int) -> None:
        """
        Adjusts game state when a player sits out

        Args:
            player_index (int): index of player that is sitting out
        """
        self.players[player_index].sit_out()
    
    def player_returns(self, player_index: int) -> None:
        """
        Adjusts game state when a player rejoins after sitting out

        Args:
            player_index (int): index of player that is rejoining
        """
        self.players[player_index].rejoin()
    
    def serialize(self) -> str:
        """
        Serializes game state to JSON

        returns:
            str: JSON string representing game state
        """
        to_json = {
            "buy_in": self.buy_in,
            "players": [player.serialize() for player in self.players],
            "community_cards": [card.encode() for card in self.community_cards],
            "small_blind": self.small_blind,
            "big_blind": self.big_blind,
            "current_dealer_index": self.current_dealer,
            "current_small_index": self.current_small,
            "current_big_index": self.current_big,
            "active_player_index": self.active_player,
            "current_round": self.current_round.value,
            "current_pot": self.current_pot,
            "max_players": self.max_players,
            "games_played": self.games_played,
            "winner_index": self.winner
        }
        return json.dumps(to_json)

    
    

