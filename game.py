# pylint: disable=all
import random

POKER_DECK_SUITS = ('clubs', 'diamonds', 'spades', 'hearts')

POKER_DECK_RANK_2_SYMBOL = {
    1: 'two',
    2: 'three',
    3: 'four',
    4: 'five',
    5: 'six',
    6: 'seven',
    7: 'eight',
    8: 'nine',
    9: 'ten',
    10: 'jack',
    11: 'queen',
    12: 'king',
    13: 'ace',
}

def create_poker_deck():
    next_id = 1
    deck = []
    for suit in POKER_DECK_SUITS:
        for rank in xrange(1, 13+1): # 2 thru 10, J, Q, K, A
            deck.append({
                'id': next_id,
                'suit': suit,
                'rank': rank,
                'name': '%s of %s' % (POKER_DECK_RANK_2_SYMBOL[rank], suit)
            })
        next_id += 1

class HeartsMgr(object):
    def __init__(self):
        self.cache = {}

    def initialize(self, hearts_json='hearts.json'):
        with open(hearts_json, 'r') as fil:
            self.cache = json.load(fil)

        if self.cache['deck'] is None:
            self.cache['deck'] = create_poker_deck()


