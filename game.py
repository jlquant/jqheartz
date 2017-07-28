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
        self._trick = {}
        self._suit_led = None

    def initialize(self, hearts_json='hearts.json'):
        with open(hearts_json, 'r') as fil:
            self.cache = json.load(fil)

        if self.cache['deck'] is None:
            self.cache['deck'] = create_poker_deck()

    def new_game(self):
        # Reset player
        for player in self.cache['player']:
            player['points'] = 0
            player['hand'][:] = [] # In place clear
            player['trick_pile'][:] = [] # In place clear

        # Reset deck
        self.cache['deck'] = create_poker_deck()

        # Shuffle deck
        random.shuffle(self.cache['deck'])

        # Deal cards
        while self.cache['deck']:
            for player in self.cache['player']: # Assume cards divide evenly
                player['hand'].append(self.cache['deck'].pop(0))

        # SKIP CARD PASSING FOR EXAMPLE SIMPLICITY

        # Find start player
        for player in self.cache['player']:
            if any(card['suit'] == 'clubs' and card['rank'] == 2 for card in player['hand']):
                self.cache['next_up'] = {
                    '$href': '#/player/%d' % player['id']
                }

    def play_card(self, player_idx, card_idx):
        player_name = self.cache['player']['name']
        card = self.cache['player'][player_idx]['hand'].pop(card_idx)

        # First card played?
        if self._suit_led is None:
            print player_name, "leads with the", card['name']
            self._suit_led = card['suit']
        else:
            print player_name, "plays the", card['name']

        # Play card
        self._trick.append({
            'owner_id': self.cache['player'][player_idx]['id'],
            'card': card,
        })

        # Last card played?
        if len(self._trick) == len(self.cache['player']):
            self.determine_trick_winner()

        # Find next player
        next_player_idx = player_idx + 1
        if len(self.cache['player'] == next_player_idx):
            next_player_idx = 0


    def determine_trick_winner(self):
        winner = None
        for player, card in self._trick.iteritems():
            if card['suit'] != self._suit_led:
                # Didn't win for sure
                pass
            elif winner is None:
                winner = player
            elif card['rank'] > self._trick[winner]['rank']:
                winner = player
            else:
                # Not higher
                pass

