import random
import config as cfg

class Hand(object):

    def __init__(self, tab):
        #playercolors is used in  Deck.score
        if cfg.player_num == 1:
            self.playercolors = [cfg.playercolor, cfg.opponentcolor]
        else:
            self.playercolors = [cfg.opponentcolor, cfg.playercolor]
        self.refill(tab)

    def refill(self, tab):
        cfg.deck.refill_deck(tab)