
from ROOT import TFile

from EventStore import EventStore

from detector import detector
from pmt import pmt

#_____________________________________________________________________________
class analysis:
    #_____________________________________________________________________________
    def __init__(self, outnam="ddhits.root"):

        self.inputs = []
        self.detectors = []
        self.pmts = []

        self.outnam = outnam

    #_____________________________________________________________________________
    def event_loop(self):

        store = EventStore(self.inputs)

        out = TFile(self.outnam, "recreate")
        for i in self.detectors:
            i.create_output()
        for i in self.pmts:
            i.create_output()

        #event loop
        nev = 0
        for iev, evt in enumerate(store):

            nev += 1

            #hit loop
            for i in self.detectors:
                i.hit_loop(store)
            for i in self.pmts:
                i.hit_loop(store)

        print("    Output file:     ", self.outnam)
        print("    Number of events:", nev)
        for i in self.detectors:
            #print(i.name, i.otree.GetEntries())
            print("    {0:24s}".format(i.name,), i.otree.GetEntries())
            i.otree.Write()
        for i in self.pmts:
            #print(i.name, i.otree.GetEntries())
            print("    {0:24s}".format(i.name,), i.otree.GetEntries())
            i.otree.Write()

        out.Close()

    #_____________________________________________________________________________
    def add_input(self, inp):

        self.inputs.append( inp )

    #_____________________________________________________________________________
    def set_input(self, inp):

        self.inputs = inp

    #_____________________________________________________________________________
    def add_detector(self, name):

        self.detectors.append( detector(name) )

    #_____________________________________________________________________________
    def add_pmt(self, name):

        self.pmts.append( pmt(name) )














