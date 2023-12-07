def test_create_room(server_create):
    ws1, p1_msg = server_create
    assert p1_msg["MESSAGE"] == {
        "PLAYER_NAME": "John Doe",
        "BALANCE": "100",
        "BUY_IN": "20",
        "BLINDS": ["10", "20"],
    }
    assert p1_msg["MESSAGE TYPE"] == "CREATE"
