from server.encryption import symencrypt


def test_symencrypt():
    """Test symencrypt function"""
    data = b"Hello, world!"
    key = b"1234567890123456"
    encrypted_data = symencrypt(key, data)
    assert data != encrypted_data
    assert data == symencrypt(key, encrypted_data)


def test_encode_decode():
    """Test encode and decode functions"""
    data = "Hello, world!"
    key = "1234567890123456"
    encrypted_data = symencrypt(key.encode(), data.encode())
    assert data != encrypted_data
    assert data == symencrypt(key.encode(), encrypted_data).decode()
