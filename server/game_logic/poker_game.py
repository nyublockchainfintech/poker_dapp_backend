from pokerkit import Automation, NoLimitTexasHoldem

state = NoLimitTexasHoldem.create_state(
    (
        Automation.ANTE_POSTING,
        Automation.BET_COLLECTION,
        Automation.BLIND_OR_STRADDLE_POSTING,
        Automation.CARD_BURNING,
        Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
        Automation.HAND_KILLING,
        Automation.CHIPS_PUSHING,
        Automation.CHIPS_PULLING,
    ),
    True,
    500,
    (1000, 2000),
    2000,
    (1125600, 2000000, 553500),
    3,
)

# Below shows the pre-flop dealings and actions.

state.deal_hole('Ac2d')  # Ivey
state.deal_hole('5h7s')  # Antonius*
state.deal_hole('7h6h')  # Dwan

state.complete_bet_or_raise_to(7000)  # Dwan
state.complete_bet_or_raise_to(23000)  # Ivey
state.fold()  # Antonius
state.check_or_call()  # Dwan

# Below shows the flop dealing and actions.

state.deal_board('Jc3d5c')

state.complete_bet_or_raise_to(35000)  # Ivey
state.check_or_call()  # Dwan

# Below shows the turn dealing and actions.

state.deal_board('4h')

state.complete_bet_or_raise_to(90000)  # Ivey
state.complete_bet_or_raise_to(232600)  # Dwan
state.complete_bet_or_raise_to(1067100)  # Ivey
state.check_or_call()  # Dwan

# Below shows the river dealing.

state.deal_board('Jh')

# Below shows the final stacks.

print(state.stacks)  # [572100, 1997500, 1109500]