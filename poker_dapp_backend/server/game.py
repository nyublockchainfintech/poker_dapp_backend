from poker_dapp_backend.base import Card
from poker_dapp_backend.server.utils import connect_to_redis
from pokerlib.enums import Rank, Suit
from poker_dapp_backend.server.player import Player, Status
from poker_dapp_backend.server.ranking import Ranker
from poker_dapp_backend.enums import BettingRound
from pokerlib.enums import Rank, Suit
from random import shuffle as default_shuffle
import json


class Game:
    def __init__(
        self,
        buy_in: int,
        blinds: tuple[int, int],
        players: list[Player] = None,
        max_players: int = 8,
    ):
        self.buy_in = buy_in
        self.players = players if players is not None else []
        self.community_cards = []
        self.card_obj = Card(Rank.ACE, Suit.CLUB)
        self.small_blind = blinds[0]
        self.big_blind = blinds[1]
        self.current_dealer = 0
        self.current_small = 1
        self.current_big = 2
        self.active_player = 3
        self.current_round = BettingRound.PRE_FLOP
        self.current_pot = 0
        self.max_players = max_players
        self.deck = []
        self.ranker = Ranker()
        self.games_played = 0
        self.winner = None
        self.counter = 0
        self.action_count = 0
        self.num_inactive = 0
        self.check_before = False
        self.current_bet = 0

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
        # if there are no players, create empty list
        if self.players is None:
            self.players = []
        # if table full, don't add player and return False
        if len(self.players) >= self.max_players:
            return False
        # otherwise, create player with params and return True
        player = Player(name, starting_balance)
        player.set_status(Status.ACTIVE)
        self.players.append(player)
        return True

    def remove_player(self, name: str) -> bool:
        """
        Removes a player from the game

        args:
            name (str): name of player to remove from game

        returns:
            bool: True if removed
                  False if not removed
        """
        # if player not in game, return False
        if name not in [player.name for player in self.players]:
            return False
        # otherwise, remove player and return True
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                return True
        return False

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

        # increment blinds and dealer if not first round
        if self.games_played > 1:
            self.current_dealer = (self.current_dealer + 1) % len(self.players)
            self.current_small = (self.current_small + 1) % len(self.players)
            self.current_big = (self.current_big + 1) % len(self.players)

        # set current pot to 0
        self.current_pot = 0

        # set current bet to 0
        self.current_bet = 0

        # incremet games played
        self.games_played += 1

        # set number of inactive players to 0
        self.num_inactive = 0
        
        # set all players to active that are not sitting out, increase inactive count if sitting out
        for player in self.players:
            if player.status != Status.SITTING_OUT:
                player.set_status(Status.ACTIVE)
            else:
                self.num_inactive += 1

        # remove blinds from players and add to pot
        self.active_player = self.current_small
        self.players[self.current_small].bet(self.small_blind)
        self.current_pot += self.small_blind
        self.players[self.current_big].bet(self.big_blind)
        self.current_pot += self.big_blind

        # set active player to player after big blind
        self.active_player = (self.current_big + 1) % len(self.players)

        # initialize deck and shuffle
        self.deck: list = (
            self.card_obj.init_deck()
        )  # typehint so VSCode stops being annoying
        default_shuffle(self.deck)

        # deal cards
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.pop())

        # set betting round to pre_flop
        self.current_round = BettingRound.PRE_FLOP
        return True

    def increment_round(self) -> None:
        """
        Increments to next betting round
        """
        # if everyone but one player has folded, give them the pot and end the game
        if self.num_inactive == len(self.players) - 1:
            self.showdown()
            return
        
        # set current bet to 0
        self.current_bet = 0

        # increment round
        if self.current_round == BettingRound.PRE_FLOP:
            self.current_round = BettingRound.FLOP
        elif self.current_round == BettingRound.FLOP:
            self.current_round = BettingRound.TURN
        elif self.current_round == BettingRound.TURN:
            self.current_round = BettingRound.RIVER
        elif self.current_round == BettingRound.RIVER:
            self.showdown()
            return

        # if it's the flop, deal 3 cards
        if self.current_round == BettingRound.FLOP:
            for _ in range(3):
                self.community_cards.append(self.deck.pop())
        # if it's the turn or river, deal 1 card
        elif (
            self.current_round == BettingRound.TURN
            or self.current_round == BettingRound.RIVER
        ):
            self.community_cards.append(self.deck.pop())

        # set active player to first active player after big blind
        self.active_player = self.current_big
        for _ in range(len(self.players)):
            self.active_player = (self.active_player + 1) % len(self.players)
            if self.players[self.active_player].status == Status.ACTIVE:
                break

    def showdown(self) -> None:
        """
        Determines the winner of the game and sets the winner index and distributes pot
        """
        
        # set current round to finished
        self.current_round = BettingRound.FINISHED

        # get all hands if the player is not folded
        hands = []
        player_indexes = []
        counter = 0
        for player in self.players:
            if player.status != Status.FOLDED and player.status != Status.SITTING_OUT:
                hands.append(player.hand)
                player_indexes.append(counter)
            counter += 1

        # get winner index
        self.winner = player_indexes[self.ranker.best_hand(hands, self.community_cards)]
        # distribute pot
        self.players[self.winner].balance += self.current_pot
        self.current_pot = 0
        # empty hands
        for player in self.players:
            player.hand = []


    def player_bet(self, player_index: int, bet_amount: int) -> None:
        """
        Adjusts game state when a player submits a bet

        Args:
            player_index (int): index of player that is making a bet
            bet_amount (int): amount that player is betting
        """
        assert (
            player_index == self.active_player
        ), "illegal bet argument, bet not from active player"
        self.players[player_index].bet(bet_amount)
        self.action_count += 1
        self.current_pot += bet_amount
        # if the someone has checked before, reset check_before and reset action_count to 1
        if self.check_before:
            self.check_before = False
            self.action_count = 1
        # if this is a raise, reset action_count to 1
        if bet_amount > self.current_bet:
            self.current_bet = bet_amount
            self.action_count = 1
        # loop around table once and look for next active player
        for _ in range(len(self.players)):
            self.active_player = (self.active_player + 1) % len(self.players)
            if self.players[self.active_player].status == Status.ACTIVE:
                break
        if self.action_count == len(self.players) - self.num_inactive:
            self.increment_round()
            self.action_count = 0

    def player_check(self, player_index: int) -> None:
        """
        Adjusts game state when a player checks

        Args:
            player_index (int): index of player that is checking
        """
        assert (
            player_index == self.active_player
        ), "illegal check argument, check not from active player. check was from player: " + str(player_index) + " active player is: " + str(self.active_player)
        self.players[player_index].check()
        self.check_before = True
        self.action_count += 1
        # loop around table once and look for next active player
        for _ in range(len(self.players)):
            self.active_player = (self.active_player + 1) % len(self.players)
            if self.players[self.active_player].status == Status.ACTIVE:
                break
        if self.action_count == len(self.players) - self.num_inactive:
            self.increment_round()
            self.action_count = 0

    def player_fold(self, player_index: int) -> None:
        """
        Adjusts game state when a player folds

        Args:
            player_index (int): index of player that is folding
        """
        assert (
            player_index == self.active_player
        ), "illegal fold argument, check not from active player"
        self.players[player_index].fold()
        self.action_count += 1
        self.num_inactive += 1
        # loop around table once and look for next active player
        for _ in range(len(self.players)):
            self.active_player = (self.active_player + 1) % len(self.players)
            if self.players[self.active_player].status == Status.ACTIVE:
                break
        if self.action_count == len(self.players) - self.num_inactive:
            self.increment_round()
            self.action_count = 0

    def player_sitting_out(self, player_index: int) -> None:
        """
        Adjusts game state when a player sits out

        Args:
            player_index (int): index of player that is sitting out
        """
        assert (
            self.players[player_index].status != Status.SITTING_OUT
        ), "illegal sit out argument, player already sitting out"
        self.players[player_index].sit_out()

    def player_returns(self, player_index: int) -> None:
        """
        Adjusts game state when a player rejoins after sitting out

        Args:
            player_index (int): index of player that is rejoining
        """
        assert (
            self.players[player_index].status == Status.SITTING_OUT
        ), "illegal return argument, player not sitting out"
        self.players[player_index].rejoin()

    def get_index_from_name(self, name: str) -> int:
        """
        Gets the index of a player given their name

        Args:
            name (str): name of player

        Returns:
            int: index of player
        """
        for i in range(len(self.players)):
            if self.players[i].name == name:
                return i
        return -1

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
            "current_round": self.current_round.name,
            "current_pot": self.current_pot,
            "max_players": self.max_players,
            "games_played": self.games_played,
            "winner_index": self.winner,
        }
        return json.dumps(to_json)

    def store_state_in_redis(self, counter=None):
        """
        Set game state in redis
        """
        r = connect_to_redis()
        state = self.serialize()
        if counter:
            self.counter = counter
        return r.hset("game_state", f"state:{self.counter}", state)

    def get_latest_state(self, counter=None):
        """
        Get latest game state from redis
        """
        r = connect_to_redis()
        if counter:
            self.counter = counter
        return r.hget("game_state", f"state:{self.counter}")
