import random
import config as cfg

class Hand(object):

    def __init__(self, tab):
        #Choose a color for the player
        #rndgen = random.Random(0)
        #ran = rndgen.randint(0, len(cfg.PLAYERCOLORS) - 1)
        #self.playercolor = cfg.PLAYERCOLORS.pop(ran)    #e.g. ["green", "lightgreen"]
        self.playercolor = ["green", "yellow"]
        self.refill(tab)

    def refill(self, tab):
        cfg.deck.refill_deck(tab)