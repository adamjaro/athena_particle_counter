
import math
from ctypes import c_double

from ROOT import TTree

#_____________________________________________________________________________
class detector:
    #_____________________________________________________________________________
    def __init__(self, name):

        self.name = name

    #_____________________________________________________________________________
    def hit_loop(self, store):

        for ihit in store.get(self.name):

            self.out_en.value = ihit.energyDeposit()

            pos = ihit.position()

            self.out_z.value = pos.z
            self.out_r.value = math.sqrt( pos.x**2 + pos.y**2 )

            self.otree.Fill()

    #_____________________________________________________________________________
    def create_output(self):

        self.otree = TTree(self.name, self.name)
        self.out_en = c_double(0)
        self.out_r = c_double(0)
        self.out_z = c_double(0)
        self.otree.Branch("en", self.out_en, "en/D")
        self.otree.Branch("r", self.out_r, "r/D")
        self.otree.Branch("z", self.out_z, "z/D")

