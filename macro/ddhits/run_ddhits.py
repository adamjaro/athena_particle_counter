#!/usr/bin/python3

from glob import glob

import sys
sys.path.append("/home/jaroslav/sim/Athena/athena_particle_counter/macro/ddhits")

from analysis import analysis

#_____________________________________________________________________________
def main():

    #input
    indir = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a"
    inlist = glob(indir+"/000?/"+"output.root")

    outfile = "ddhits.root"

    det = [ \
	"VertexBarrelHits", \
	"EcalEndcapPHits", \
	"DIRCBarHits", \
	"TrackerBarrelHits", \
	"TrackerEndcapHits", \
	"MPGDTrackerBarrelHits", \
	"GEMTrackerEndcapHits", \
	"EcalEndcapNHits", \
	"EcalBarrelHits", \
	"EcalBarrelScFiHits", \
	"HcalBarrelHits", \
	"HcalEndcapNHits", \
	"HcalEndcapPHits" \
    ]
    pmt = [ \
	"ERICHHits", \
	"DRICHHits", \
    ]

    ana = analysis(outfile)
    ana.set_input(inlist)

    for i in det:
        ana.add_detector(i)
    for i in pmt:
        ana.add_pmt(i)

    ana.event_loop()



#_____________________________________________________________________________
if __name__ == "__main__":

    main()


