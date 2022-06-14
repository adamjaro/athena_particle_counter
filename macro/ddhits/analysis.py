
from ROOT import TFile, TTree

from ctypes import c_double

from dd4hep import Detector
from EventStore import EventStore

from hcal_layers import hcal_layers
from hcal_endcap_p import hcal_endcap_p
from scifi_nfib import scifi_nfib
from block_scale import block_scale
from pixel import pixel
from sipm import sipm

#_____________________________________________________________________________
class analysis:
    #_____________________________________________________________________________
    def __init__(self, outnam="ddhits.root"):

        self.inputs = []
        self.detectors = {}

        self.outnam = outnam

    #_____________________________________________________________________________
    def load_detectors(self, compact):

        #load geometry
        det = self.load_compact(compact)

        #Hcal with threshold on layer
        nam = ["HcalBarrelHits", "HcalEndcapNHits"]
        for i in nam:
            self.add_detector(i, hcal_layers)
            self.detectors[i].load_compact(det)

        #first layers to count
        self.detectors["HcalBarrelHits"].ilay_max = 5
        self.detectors["HcalEndcapNHits"].ilay_max = 10

        #HcalEndcapPHits with 300 MeV for sum of layers
        self.add_detector("HcalEndcapPHits", hcal_endcap_p)
        self.detectors["HcalEndcapPHits"].load_compact(det)

        #EcalBarrelScFiHits, SciFi set for groups of 300 fibers
        self.add_detector("EcalBarrelScFiHits", scifi_nfib)

        #EcalEndcapPHits with hits per homogenious block
        self.add_detector("EcalEndcapPHits", block_scale)

        #detectors with one hit per pixel
        self.add_detector("VertexBarrelHits", pixel)
        self.detectors["VertexBarrelHits"].threshold = 4e-7 # GeV, 0.4 keV

        self.add_detector("TrackerBarrelHits", pixel)
        self.detectors["TrackerBarrelHits"].threshold = 4e-7 # GeV, 0.4 keV

        self.add_detector("TrackerEndcapHits", pixel)
        self.detectors["TrackerEndcapHits"].threshold = 4e-7 # GeV, 0.4 keV

        self.add_detector("MPGDTrackerBarrelHits", pixel)
        self.detectors["MPGDTrackerBarrelHits"].threshold = 2e-7 # GeV, 0.2 keV

        self.add_detector("GEMTrackerEndcapHits", pixel)
        self.detectors["GEMTrackerEndcapHits"].threshold = 2e-7 # GeV, 0.2 keV

        self.add_detector("EcalEndcapNHits", pixel)
        self.detectors["EcalEndcapNHits"].threshold = 2.5e-3 # GeV, 2.5 MeV

        self.add_detector("EcalBarrelHits", pixel)
        self.detectors["EcalBarrelHits"].threshold = 4e-7 # GeV, 0.4 keV

        #SiPMs
        self.add_detector("ERICHHits", sipm)
        self.add_detector("DRICHHits", sipm)


    #_____________________________________________________________________________
    def load_compact(self, nam):

        det = Detector.getInstance()
        det.fromCompact(nam)
        det.volumeManager()
        det.apply("DD4hepVolumeManager", 0, 0)

        return det

    #_____________________________________________________________________________
    def event_loop(self):

        store = EventStore(self.inputs)

        out = TFile(self.outnam, "recreate")
        for i in self.detectors.values():
            i.create_output()

        #mc tree
        mc_tree = TTree("mc", "mc")
        phot_ve_x = c_double(0)
        phot_ve_y = c_double(0)
        phot_ve_z = c_double(0)
        phot_vs_x = c_double(0)
        phot_vs_y = c_double(0)
        phot_vs_z = c_double(0)
        mc_tree.Branch("phot_ve_x", phot_ve_x, "phot_ve_x/D")
        mc_tree.Branch("phot_ve_y", phot_ve_y, "phot_ve_y/D")
        mc_tree.Branch("phot_ve_z", phot_ve_z, "phot_ve_z/D")
        mc_tree.Branch("phot_vs_x", phot_vs_x, "phot_vs_x/D")
        mc_tree.Branch("phot_vs_y", phot_vs_y, "phot_vs_y/D")
        mc_tree.Branch("phot_vs_z", phot_vs_z, "phot_vs_z/D")

        #event loop
        nev = 0
        for iev, evt in enumerate(store):

            nev += 1

            #print("Next event")

            #mc particles
            for imc in store.get("mcparticles"):

                #if imc.pdgID() != 22 or imc.parents_size() != 0: continue

                if imc.parents_size() == 0:

                    phot_ve_x.value = imc.ve().x
                    phot_ve_y.value = imc.ve().y
                    phot_ve_z.value = imc.ve().z
                    phot_vs_x.value = imc.vs().x
                    phot_vs_y.value = imc.vs().y
                    phot_vs_z.value = imc.vs().z

                    #print("mc: ", imc.pdgID(), imc.parents_size(), imc.ve().z, imc.vs().z)

            mc_tree.Fill()

            self.detectors["VertexBarrelHits"].vtx_z.value = phot_vs_z.value
            self.detectors["TrackerBarrelHits"].vtx_z.value = phot_vs_z.value
            self.detectors["TrackerEndcapHits"].vtx_z.value = phot_vs_z.value

            #hit loop for each detector
            for i in self.detectors.values():
                i.hit_loop(store)






        print("    Output file:     ", self.outnam)
        print("    Number of events:", nev)
        for i in self.detectors.values():
            print("    {0:24s}".format(i.name,), i.otree.GetEntries())
            i.otree.Write()

        mc_tree.Write()

        out.Close()

    #_____________________________________________________________________________
    def add_input(self, inp):

        self.inputs.append( inp )

    #_____________________________________________________________________________
    def set_input(self, inp):

        self.inputs = inp

    #_____________________________________________________________________________
    def add_detector(self, name, det):

        self.detectors[name] = det(name)
















