#
'''Problem 54 Poker Hands from ProjectEuler.net

In the card game poker, a hand consists of five cards and are ranked,
from lowest to highest, in the following way:

    High Card: Highest value card.
    One Pair: Two cards of the same value.
    Two Pairs: Two different pairs.
    Three of a Kind: Three cards of the same value.
    Straight: All cards are consecutive values.
    Flush: All cards of the same suit.
    Full House: Three of a kind and a pair.
    Four of a Kind: Four cards of the same value.
    Straight Flush: All cards are consecutive values of same suit.
    Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the
highest value wins; for example, a pair of eights beats a pair of fives
(see example 1 below). But if two ranks tie, for example, both players have
a pair of queens, then highest cards in each hand are compared (see example
4 below); if the highest cards tie then the nexthighest cards are compared,
and so on.

Consider the following five hands dealt to two players:
Hand            Player 1                Player 2                Winner
1               5H 5C 6S 7S KD          2C 3S 8S 8D TD
                Pair of Fives           Pair of Eights          Player 2
2               5D 8C 9S JS AC          2C 5C 7D 8S QH
                Highest card Ace        Highest card Queen      Player 1
3               2D 9C AS AH AC          3D 6D 7D TD QD
                Three Aces              Flush with Diamonds     Player 2
4               4D 6S 9H QH QC          3D 6D 7H QD QS
                Pair of Queens          Pair of Queens
                Highest card Nine       Highest card Seven      Player 1
5               2H 2D 4C 4D 4S          3C 3D 3S 9S 9D
                Full House              Full House
                With Three Fours        with Three Threes       Player 1

The file, poker.txt, contains one-thousand random hands dealt to two
players. Each line of the file contains ten cards (separated by a single
space): the first five are Player 1's cards and the last five are Player
2's cards. You can assume that all hands are valid (no invalid characters
or repeated cards), each player's hand is in no specific order, and in each
hand there is a clear winner.

Task: How many hands does Player 1 win?
'''

import sys, logging
from collections import Counter

# Configure logging
# set level to logging.ERROR, logging.INFO, or logging.DEBUG
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Datafile contains two poker hands per line with 10 cards in a string.
# Cards are two characters with pip values A23456789TJQK and suits (S)pads,
# (H)earts, (C)lubs, (D)iamonds
DATAFILE = "p054_poker.txt"

CARD_VALUES = {'2': 2,
               '3': 3,
               '4': 4,
               '5': 5,
               '6': 6,
               '7': 7,
               '8': 8,
               '9': 9,
               'T': 10,
               'J': 11,
               'Q': 12,
               'K': 13,
               'A': 14,
               }

SUIT_VALUES = {'H': 1,
               'S': 2,
               'D': 3,
               'C': 4,
               }

DECODE_HAND_RANKS = {1: "High Card",
                     2: "One Pair",
                     3: "Two Pairs",
                     4: "Three of a Kind",
                     5: "Straight",
                     6: "Flush",
                     7: "Full House",
                     8: "Four of a Kind",
                     9: "Straight Flush",
                     10: "Royal Flush",
                     }

ENCODE_HAND_RANK = {"High Card": 1,
                    "One Pair": 2,
                    "Two Pairs": 3,
                    "Three of a Kind": 4,
                    "Straight": 5,
                    "Flush": 6,
                    "Full House": 7,
                    "Four of a Kind": 8,
                    "Straight Flush": 9,
                    "Royal Flush": 10,
                    }

def get_hands():
    '''Yield line of two poker hands from file'''
    with open(DATAFILE) as poker_hands:
        for two_hands in poker_hands:
            yield two_hands.rstrip()

def encode_hand(cards):
    '''Encode a five card hand into list of tuples. Each tuple represents a
    card value and suit value. Return sorted list of cards by highest value.
    '''
    pips = [CARD_VALUES[card[0]] for card in cards]
    suits = [SUIT_VALUES[card[1]] for card in cards]
    # sort pips decending, not important if suit order maintained
    return sorted(pips, reverse=True), suits

def is_straight(pips):
    """Return True if hand is a straight.

    Compare card pip values are in decending order. Hand is presorted.
    """
    return (pips[0] == pips[1] + 1 == pips[2] + 2 == 
            pips[3] + 3 == pips[4] + 4)

def is_flush(suits):
    """Return True if hand is a flush.

    Compare if card suit values are all equal.
    """
    return suits[0] == suits[1] == suits[2] == suits[3] == suits[4]

def count_pips(pips):
    """Return sorted list of tuples for of-a-kind values and counts
    """
    # create dict of pip values and their count
    pip_count = Counter(pips)
    # sort dict by key, value (pip, count) pairs by count, then by pip,
    # reverse for decending order: [(10, 2), (2, 2), (8, 1)]
    return sorted(pip_count.items(), key=lambda x: (x[1], x[0]), reverse=True)
    
def eval_hand(pips, suits):
    '''Evaluate poker hand pips and suits values.
    Return a list of hand rank value followed by ordered relevant card
    values and ordered remainder cards. Two eval_hands lists can be
    directly compared using > for winner or == for ties. 

    Example list returned for evaluated hand:
      Two Pair Js and 7s with A: [3, 11, 7, 14, 0, 0]
      Full House 8s over 3: [7, 8, 3, 0, 0, 0]
      Straight Flush: [9, 7, 6, 5, 4, 3]
      Royal Flush: [10, 14, 13, 12, 11, 10]
      
    '''
    # check for straight, flush, straight flush, royal flush results
    straight = is_straight(pips)
    flush = is_flush(suits)
    if straight and not flush:
        # Basic Straight
        result = [ENCODE_HAND_RANK["Straight"]] + pips
    elif not straight and flush:
        # Basic Flush
        result = [ENCODE_HAND_RANK["Flush"]] + pips
    elif straight and flush:
        if pips[0] == CARD_VALUES['A']:
            # High card Ace is Royal Flush
            result = [ENCODE_HAND_RANK["Royal Flush"]] + pips
        else:
            # Straight Flush otherwise
            result = [ENCODE_HAND_RANK["Straight Flush"]] + pips
    else:
        # checking for of-a-kind results
        # get sorted list of pips and count tuples
        counted_pips = count_pips(pips)
        highest_pip_count = counted_pips[0][1]
        second_pip_count = counted_pips[1][1]
        # get reduced pip list from counted pips
        reduced_pips = [pip_count[0] for pip_count in counted_pips]
        # pad reduced pips to five values for readability
        reduced_pips.extend([0] * (5 - len(reduced_pips)))
        
        # check highest pip count
        if highest_pip_count == 1:
            # High Card if highest pip count is 1
            result = [ENCODE_HAND_RANK["High Card"]] + pips
        elif highest_pip_count == 2:
            # could be one or two pairs. check second pip count
            if second_pip_count == 2:
                # Two Pair
                result = [ENCODE_HAND_RANK["Two Pairs"]] + reduced_pips
            else:
                # One Pair
                result = [ENCODE_HAND_RANK["One Pair"]] + reduced_pips
        elif highest_pip_count == 3:
            # could be full house or 3-of-a-kind. check second pip count
            if second_pip_count == 2:
                # Full House
                result = [ENCODE_HAND_RANK["Full House"]] + reduced_pips
            else:
                # Three of a Kind
                result = [ENCODE_HAND_RANK["Three of a Kind"]] + reduced_pips
        elif highest_pip_count == 4:
            # Four of a Kind
            result = [ENCODE_HAND_RANK["Four of a Kind"]] + reduced_pips
        else:
            # highest_pip_count not 1-4
            raise ValueError("Illegal highest pip count: {0}".format(highest_pip_count))
    return result

def main():
    '''Project Euler Problem 54 Solver'''
    hands_won = 0
    hands_tied = 0
    for two_hands in get_hands():
        cards = two_hands.split(' ')
        pips1, suits1 = encode_hand(cards[:5])
        pips2, suits2 = encode_hand(cards[5:])
        logging.debug("Encoded: player1:{0}{1} player2:{2}{3}".format(pips1, suits1, pips2, suits2))
        eval1 = eval_hand(pips1, suits1)
        eval2 = eval_hand(pips2, suits2)
        logging.debug("Eval'ed: player1:{0} player2:{1}".format(eval1, eval2))
        if eval1 > eval2:
            logging.debug("player 1 Wins!")
            hands_won += 1
        elif eval1 == eval2:
            logging.error("Error: Hands shouldn't tie")
            hands_tied += 1
            
    logging.info("Player 1 won {0} hands, tied {1} times".format(hands_won, hands_tied))

if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
