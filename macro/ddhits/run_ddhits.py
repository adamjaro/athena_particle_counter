#!/usr/bin/python3

from glob import glob

import sys
sys.path.append("/home/jaroslav/sim/Athena/athena_particle_counter/macro/ddhits")

from analysis import analysis

#_____________________________________________________________________________
def main():

    #geometry
    compact = "../../../athena/athena.xml"

    #input
    indir = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a"
    #indir = "/home/jaroslav/sim/Athena/data/pythia6/py10x100a"
    inlist = glob(indir+"/0000/"+"output.root")

    #output
    outfile = "ddhits.root"

    #analysis instance
    ana = analysis(outfile)
    ana.set_input(inlist)

    ana.load_detectors(compact)

    ana.event_loop()

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    main()























