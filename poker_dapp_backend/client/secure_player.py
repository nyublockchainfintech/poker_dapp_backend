from pokerlib import Player
from typing import Optional 
from sign_state import generate_private_key

## Player + priv key + serialized/unserialized game states
class SecurePlayer(Player):

    def __init__(self, table_id, _id, name, money, priv_key:Optional, pub_key:Optional):
        super().__init__(table_id, _id, name, money)
        self.priv_key = generate_private_key()
        self.pub_key = self.priv_key.public_key()


    

