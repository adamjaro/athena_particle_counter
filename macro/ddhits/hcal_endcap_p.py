
import math
from ctypes import c_double, c_int

from ROOT import TTree

#_____________________________________________________________________________
class hcal_endcap_p:
    #_____________________________________________________________________________
    def __init__(self, name):

        self.name = name

        #threshold at 300 MeV
        self.threshold = 0.3 # GeV

        #self.ilay_max = 5

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

        #sum for energy threshold
        lsum = 0.
        for hit in store.get(self.name):
            lsum += hit.energyDeposit()

        #energy threshold
        if lsum < self.threshold:
            return

        #print(lsum)

        #hit loop
        for hit in store.get(self.name):

            self.out_en.value = hit.energyDeposit()


            #imod = self.cell_id.get(hit.cellID(), self.module_idx)
            ilay = self.cell_id.get(hit.cellID(), self.layer_idx)
            #ix = self.cell_id.get(hit.cellID(), self.x_idx)
            #iy = self.cell_id.get(hit.cellID(), self.y_idx)

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










