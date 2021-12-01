
import math
from ctypes import c_double

from ROOT import TTree

#_____________________________________________________________________________
class scifi_nfib:
    #_____________________________________________________________________________
    def __init__(self, name):

        self.name = name

        #number of fibers in a group
        self.nfib = 300

        #threshold at 2.5 MeV for the group of fibers
        self.threshold = 2.5e-3 # GeV

    #_____________________________________________________________________________
    def hit_loop(self, store):

        ifib = 0
        esum = 0.
        for ihit in store.get(self.name):

            ifib += 1
            esum += ihit.energyDeposit()

            if ifib >= self.nfib:
                ifib = 0

                if esum < self.threshold:
                    esum = 0.
                    continue

                #print(esum)

                self.out_en.value = esum
                self.otree.Fill()

                esum = 0.

    #_____________________________________________________________________________
    def create_output(self):

        self.otree = TTree(self.name, self.name)
        self.out_en = c_double(0)
        self.otree.Branch("en", self.out_en, "en/D")







