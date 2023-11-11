from pokerlib import Table, Player, PlayerSeats
from pokerlib.enums import RoundPublicInId, TablePublicInId


# table that prints outputs
class MyTable(Table):
    def publicOut(self, out_id, **kwargs):
        print(out_id, kwargs)

    def privateOut(self, player_id, out_id, **kwargs):
        print(out_id, kwargs)


# define a new table
table = MyTable(
    _id=0,
    seats=PlayerSeats([None] * 9),
    buyin=100,
    small_blind=5,
    big_blind=10,
)

player1 = Player(table_id=table.id, _id=1, name="alice", money=table.buyin)
player2 = Player(table_id=table.id, _id=2, name="bob", money=table.buyin)
# seat player1 at the first seat
table += player1, 0
# seat player2 at the first free seat
table += player2


table.publicIn(player1.id, TablePublicInId.STARTROUND)
# table.publicIn(player1.id, RoundPublicInId.CALL)
# table.publicIn(player2.id, RoundPublicInId.CHECK)
# table.publicIn(player1.id, RoundPublicInId.CHECK)
# table.publicIn(player2.id, RoundPublicInId.RAISE, raise_by=50)
# table.publicIn(player1.id, RoundPublicInId.CALL)
# table.publicIn(player1.id, RoundPublicInId.CHECK)
# table.publicIn(player2.id, RoundPublicInId.CHECK)
# table.publicIn(player1.id, RoundPublicInId.ALLIN)
# table.publicIn(player2.id, RoundPublicInId.CALL)
