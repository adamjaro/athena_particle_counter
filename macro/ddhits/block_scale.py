
import math
from ctypes import c_double

from ROOT import TTree

#_____________________________________________________________________________
class block_scale:
    #_____________________________________________________________________________
    def __init__(self, name):

        self.name = name

        #energy threshold 5 MeV for the block
        self.threshold = 5e-3 # GeV

        #scale for the block
        self.scale = 0.028

    #_____________________________________________________________________________
    def hit_loop(self, store):

        for hit in store.get(self.name):

            self.out_en.value = self.scale*hit.energyDeposit()

            if self.out_en.value < self.threshold:
                continue

            pos = hit.position()

            self.out_x.value = pos.x
            self.out_y.value = pos.y
            self.out_z.value = pos.z

            self.otree.Fill()

    #_____________________________________________________________________________
    def create_output(self):

        self.otree = TTree(self.name, self.name)
        self.out_en = c_double(0)
        self.out_x = c_double(0)
        self.out_y = c_double(0)
        self.out_z = c_double(0)
        self.otree.Branch("en", self.out_en, "en/D")
        self.otree.Branch("x", self.out_x, "x/D")
        self.otree.Branch("y", self.out_y, "y/D")
        self.otree.Branch("z", self.out_z, "z/D")















