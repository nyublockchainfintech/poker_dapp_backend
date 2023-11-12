def encode_rank(rank):
    """
    Decodes rank from integer to string

    Args:
        rank (int): integer representing rank

    Returns:
        string: string representing rank
    """
    rank_mapping = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "6",
        6: "7",
        7: "8",
        8: "9",
        9: "J",
        10: "Q",
        11: "K",
        12: "A",
    }
    return rank_mapping[rank]


def encode_suit(suit):
    """
    Decodes suit from integer to string

    Args:
        suit (int): integer representing suit

    Returns:
        string: string representing suit
    """
    suit_mapping = {
        0: "s",
        1: "c",
        2: "d",
        3: "h",
    }
    return suit_mapping[suit]
