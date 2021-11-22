#!/bin/bash

npsim\
  --inputFiles /home/jaroslav/sim/GETaLM_data/qr/qr_18x275_Qe_beff2_120kevt.hepmc \
  --compactFile main.xml \
  --random.seed 123 \
  --physics.list FTFP_BERT \
  --field.eps_min 5e-06 \
  --field.eps_max 1e-04 \
  --action.tracker ParticleCounterSDAction \
  --numberOfEvents 10000 \
  --outputFile output.root


#  --inputFiles /home/jaroslav/sim/GETaLM_data/beam/el_beam_18_t3p3_10kevt.hepmc \


#  --field.eps_min 5e-06 \
#  --field.eps_max 1e-04 \


#      --enableGun\
#      --gun.energy 18000 \
#      --gun.particle e- \
#     --gun.direction "0 0 -1" \



# --gun.direction "0 1 0" \
#      --gun.isotrop True\
#
#      --gun.energyMin 1000 \
#      --gun.energyMax 1000 \
#

#      --gun.multiplicity 3\
#      --gun.thetaMin pi/2\
#      --gun.thetaMax pi/2\
#      --gun.phiMin 0\
#      --gun.phiMax 2*pi\
#      --gun.distribution "uniform"\

