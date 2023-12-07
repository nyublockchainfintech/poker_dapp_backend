from poker_dapp_backend.server.game import Game
from poker_dapp_backend.server.utils import connect_to_redis


def setup(self):
    self.redis = connect_to_redis()
    self.counter = 0
    self.redis.delete("game_state")


def teardown(self):
    self.redis.delete("game_state")
    self.redis.close()


def test_store_game():
    game = Game(buy_in=1, blinds=(10, 20))
    setup(game)
    val = game.store_state_in_redis()
    teardown(game)
    assert val == 1


def test_retrieve_game():
    game = Game(buy_in=1, blinds=(10, 20))
    setup(game)
    game.store_state_in_redis()
    val = game.get_latest_state()
    teardown(game)
    assert isinstance(val, str)
