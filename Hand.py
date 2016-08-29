import random
import config as cfg

class Hand(object):

    def __init__(self, tab):
        self.playercolors = [cfg.playercolor, cfg.opponentcolor]
        self.refill(tab)

    def refill(self, tab):
        cfg.deck.refill_deck(tab)