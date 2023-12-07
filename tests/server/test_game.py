from poker_dapp_backend.server.game import Game
from poker_dapp_backend.enums import BettingRound
from poker_dapp_backend.server.player import Player, Status
from poker_dapp_backend.base import Card
from pokerlib.enums import Rank, Suit


def test_add_player():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) is True
    assert game.add_player("Player2", 1000) is True
    assert game.add_player("Player3", 1000) is True
    assert game.add_player("Player4", 1000) is True
    assert game.add_player("Player5", 1000) is True
    assert game.add_player("Player6", 1000) is True
    assert game.add_player("Player7", 1000) is True
    assert game.add_player("Player8", 1000) is True
    assert game.add_player("Player9", 1000) is False


def test_start_game():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) is True
    assert game.add_player("Player2", 1000) is True
    assert game.add_player("Player3", 1000) is True
    assert game.add_player("Player4", 1000) is True
    assert game.add_player("Player5", 1000) is True
    assert game.add_player("Player6", 1000) is True
    assert game.add_player("Player7", 1000) is True
    assert game.add_player("Player8", 1000) is True
    assert game.add_player("Player9", 1000) is False
    assert game.start_game() is True
    assert game.current_round == BettingRound.PRE_FLOP
    assert game.active_player == 3
    assert game.current_pot == 30
    assert game.players[0].balance == 1000
    assert game.players[1].balance == 990
    assert game.players[2].balance == 980
    assert game.players[3].balance == 1000
    assert game.players[4].balance == 1000
    assert game.players[5].balance == 1000
    assert game.players[6].balance == 1000
    assert game.players[7].balance == 1000


def test_increment_round():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) == True
    assert game.add_player("Player2", 1000) == True
    assert game.add_player("Player3", 1000) == True
    assert game.add_player("Player4", 1000) == True
    assert game.add_player("Player5", 1000) == True
    assert game.add_player("Player6", 1000) == True
    assert game.add_player("Player7", 1000) == True
    assert game.add_player("Player8", 1000) == True
    assert game.add_player("Player9", 1000) == False
    assert game.start_game() == True
    assert game.current_round == BettingRound.PRE_FLOP
    game.increment_round()
    assert game.current_round == BettingRound.FLOP
    assert len(game.community_cards) == 3
    game.increment_round()
    assert game.current_round == BettingRound.TURN
    assert len(game.community_cards) == 4
    game.increment_round()
    assert game.current_round == BettingRound.RIVER
    assert len(game.community_cards) == 5
    try:
        game.increment_round()
        assert False
    except ValueError:
        assert True


def test_showdown():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) == True
    assert game.add_player("Player2", 1000) == True
    assert game.add_player("Player3", 1000) == True
    assert game.add_player("Player4", 1000) == True
    assert game.add_player("Player5", 1000) == True
    assert game.add_player("Player6", 1000) == True
    assert game.add_player("Player7", 1000) == True
    assert game.add_player("Player8", 1000) == True
    assert game.add_player("Player9", 1000) == False
    assert game.start_game() == True
    # give one player a better hand than the others
    game.players[0].hand = [Card(Rank.ACE, Suit.SPADE), Card(Rank.ACE, Suit.HEART)]
    game.players[1].hand = [Card(Rank.KING, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
    game.players[2].hand = [Card(Rank.QUEEN, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    game.players[3].hand = [Card(Rank.JACK, Suit.SPADE), Card(Rank.JACK, Suit.HEART)]
    game.players[4].hand = [Card(Rank.TEN, Suit.SPADE), Card(Rank.TEN, Suit.HEART)]
    game.players[5].hand = [Card(Rank.NINE, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    game.players[6].hand = [Card(Rank.EIGHT, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]
    game.players[7].hand = [Card(Rank.SEVEN, Suit.SPADE), Card(Rank.SEVEN, Suit.HEART)]
    # set the community cards
    game.community_cards = [
        Card(Rank.ACE, Suit.CLUB),
        Card(Rank.KING, Suit.CLUB),
        Card(Rank.QUEEN, Suit.CLUB),
        Card(Rank.JACK, Suit.CLUB),
        Card(Rank.TEN, Suit.CLUB),
    ]
    # run the showdown
    game.showdown()
    # assert that the winner is the player with the best hand and that the pot is distributed
    assert game.winner == 0
    assert game.players[0].balance == 1030
    assert game.players[1].balance == 990
    assert game.players[2].balance == 980


def test_player_bet():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) == True
    assert game.add_player("Player2", 1000) == True
    assert game.add_player("Player3", 1000) == True
    assert game.add_player("Player4", 1000) == True
    assert game.add_player("Player5", 1000) == True
    assert game.add_player("Player6", 1000) == True
    assert game.add_player("Player7", 1000) == True
    assert game.add_player("Player8", 1000) == True
    assert game.add_player("Player9", 1000) == False
    assert game.start_game() == True
    assert game.current_round == BettingRound.PRE_FLOP
    game.player_bet(3, 20)
    assert game.current_pot == 50
    assert game.players[3].balance == 980
    try:
        game.player_bet(3, 20)
        assert False
    except AssertionError:
        assert True


def test_player_fold():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) == True
    assert game.add_player("Player2", 1000) == True
    assert game.add_player("Player3", 1000) == True
    assert game.add_player("Player4", 1000) == True
    assert game.add_player("Player5", 1000) == True
    assert game.add_player("Player6", 1000) == True
    assert game.add_player("Player7", 1000) == True
    assert game.add_player("Player8", 1000) == True
    assert game.add_player("Player9", 1000) == False
    assert game.start_game() == True
    assert game.current_round == BettingRound.PRE_FLOP
    game.player_fold(3)
    assert game.players[3].status == Status.FOLDED
    assert game.active_player == 4
    try:
        game.player_fold(3)
        assert False
    except AssertionError:
        assert True


def test_player_check():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) == True
    assert game.add_player("Player2", 1000) == True
    assert game.add_player("Player3", 1000) == True
    assert game.add_player("Player4", 1000) == True
    assert game.add_player("Player5", 1000) == True
    assert game.add_player("Player6", 1000) == True
    assert game.add_player("Player7", 1000) == True
    assert game.add_player("Player8", 1000) == True
    assert game.add_player("Player9", 1000) == False
    assert game.start_game() == True
    assert game.current_round == BettingRound.PRE_FLOP
    game.player_check(3)
    assert game.active_player == 4
    try:
        game.player_check(3)
        assert False
    except AssertionError:
        assert True


def test_player_sitting_out():
    game = Game(1000, (10, 20))
    assert game.add_player("Player1", 1000) == True
    game.player_sitting_out(0)
    assert game.players[0].status == Status.SITTING_OUT
    game.player_returns(0)
    assert game.players[0].status == Status.ACTIVE
