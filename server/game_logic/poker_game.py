from pokerkit import Automation, NoLimitTexasHoldem

class GameState:

    def __init__(self, antes: int, blinds_or_straddles: tuple, min_bet: int, 
    starting_stacks: tuple, player_count: int):

        self.state = NoLimitTexasHoldem.create_state(
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
            antes,    
            (blinds_or_straddles[0], blinds_or_straddles[1]),   
            min_bet,   
            (starting_stacks[0], starting_stacks[1], starting_stacks[2]),     
            player_count,   
        )

    # Below shows the pre-flop dealings and actions.
    def deal_hole(card):
        self.state.deal_hole("")
   
   #state.deal_hole('7h6h')  # Dwan

    def complete_bet_or_raise_to(amount):
        self.state.complete_bet_or_raise_to(amount)  # Dwan
    
    def fold():
        self.state.fold()

    def check_or_call():
        self.state.check_or_call()

    # Below shows the flop dealing and actions.

    def deal_board(card):
        self.state.deal_board("")



#print(state.stacks)  # [572100, 1997500, 1109500]