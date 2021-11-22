#!/bin/bash

npsim\
  --inputFiles /home/jaroslav/sim/GETaLM_data/beam_gas/beam_gas_ep_10GeV_emin0p1_10Mevt.hepmc \
  --compactFile athena_with_fe.xml \
  --runType vis \
  --enableQtUI \
  --outputFile output.root\
  --macro visualize.mac


#

#  --compactFile main.xml \

#  --enableGun \
#  --gun.direction "0 0 -1" \
#  --gun.position "0 0 15000" \
#  --gun.energy 10000 \
#  --gun.particle e- \


