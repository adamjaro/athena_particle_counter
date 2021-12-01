
import math
from ctypes import c_double, c_int

from ROOT import TTree

#_____________________________________________________________________________
class hcal_layers:
    #_____________________________________________________________________________
    def __init__(self, name):

        self.name = name

        #threshold at 0.1 MeV
        self.threshold = 1e-4 # GeV

        self.ilay_max = 5

    #_____________________________________________________________________________
    def load_compact(self, det):

        #readout ID
        readout_id = det.readout(self.name).idSpec()

        #cell_id
        self.cell_id = readout_id.decoder()

        #indices
        #self.module_idx = self.cell_id.index("module")
        self.layer_idx = self.cell_id.index("layer")
        #self.x_idx = self.cell_id.index("x")
        #self.y_idx = self.cell_id.index("y")


    #_____________________________________________________________________________
    def hit_loop(self, store):

        for hit in store.get(self.name):

            self.out_en.value = hit.energyDeposit()

            #energy threshold
            if(self.out_en.value < self.threshold):
                continue

            #imod = self.cell_id.get(hit.cellID(), self.module_idx)
            ilay = self.cell_id.get(hit.cellID(), self.layer_idx)
            #ix = self.cell_id.get(hit.cellID(), self.x_idx)
            #iy = self.cell_id.get(hit.cellID(), self.y_idx)

            #max num of layers
            if ilay > self.ilay_max:
                continue

            #print(ilay)

            self.out_ilay.value = ilay

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
        self.out_ilay = c_int(0)
        self.otree.Branch("en", self.out_en, "en/D")
        self.otree.Branch("x", self.out_x, "x/D")
        self.otree.Branch("y", self.out_y, "y/D")
        self.otree.Branch("z", self.out_z, "z/D")
        self.otree.Branch("ilay", self.out_ilay, "ilay/D")










