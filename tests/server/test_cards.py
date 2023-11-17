from poker_dapp_backend.server.dealer import Card, Dealer


def test_dealer_build():
    dealer = Dealer()
    assert len(dealer.decoded_cards) == 52


def test_dealer_encode():
    dealer = Dealer()
    dealer.encode()
    assert len(dealer.encoded_cards) == 52 * 2
