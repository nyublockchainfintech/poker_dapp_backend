def decode_rank(rank):
    """
    Decodes rank from integer to string

    Args:
        rank (int): integer representing rank

    Returns:
        string: string representing rank
    """
    rank_mapping = {
        0: "TWO",
        1: "THREE",
        2: "FOUR",
        3: "FIVE",
        4: "SIX",
        5: "SEVEN",
        6: "EIGHT",
        7: "NINE",
        8: "TEN",
        9: "JACK",
        10: "QUEEN",
        11: "KING",
        12: "ACE",
    }
    return rank_mapping[rank]


def decode_suit(suit):
    """
    Decodes suit from integer to string

    Args:
        suit (int): integer representing suit

    Returns:
        string: string representing suit
    """
    suit_mapping = {
        0: "SPADE",
        1: "CLUB",
        2: "DIAMOND",
        3: "HEART",
    }
    return suit_mapping[suit]
