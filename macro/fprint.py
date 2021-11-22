#!/usr/bin/python3

import math

from EventStore import EventStore

#_____________________________________________________________________________
def main():

    infile = "output.root"
    detector = "ParticleCounter"

    store = EventStore([infile])

    #print(store)
    #return

    nmax = 40

    #event loop
    ii = 0
    for iev, evt in enumerate(store):

        #print("Next event, hits:", len(store.get(detector)))

        #mc loop
        #for imc in store.get("mcparticles"):
        #    print("  mc:", imc.energy())

        #continue

        #hit loop
        for ihit in store.get(detector):

            ii += 1
            if nmax > 0 and ii > nmax: break

            pos = ihit.position()

            radius = math.sqrt( pos.x**2 + pos.y**2 )

            print("  hit:", radius, pos.z, ihit.energyDeposit())

#main


#_____________________________________________________________________________
if __name__ == "__main__":

    main()


















