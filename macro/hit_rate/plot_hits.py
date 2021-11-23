#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("/home/jaroslav/sim/lmon/macro")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = hit_en
    func[1] = hit_rate


    func[iplot]()

#main

#_____________________________________________________________________________
def hit_en():

    #hit energy

    infile = "../ddhits/ddhits.root"

    #log_10(keV)
    emin = -9
    emax = 9
    ebin = 0.1

    #det = "VertexBarrelHits"
    #det = "TrackerBarrelHits"
    #det = "TrackerEndcapHits"
    det = "EcalEndcapNHits"

    inp = TFile.Open(infile)
    htree = inp.Get(det)

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)
    htree.Draw("TMath::Log10(en*1e6) >> hE") # keV
    ep = ut.h1_to_arrays(hE)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(ep[0], ep[1], "-", color="blue", lw=1)

    ax.set_xlabel("keV")
    ax.set_ylabel("Counts")

    ax.set_yscale("log")

    #plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i)+"}$" for i in ax.get_xticks()[1:-1]])
    plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.1f}".format(i)+"}$" for i in ax.get_xticks()[1:-1]])

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hit_en

#_____________________________________________________________________________
def hit_rate():

    #hit rate

    infile = "../ddhits/ddhits.root"

    #number of simulated events
    nsim = 2000.

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
	"HcalEndcapPHits", \
	"ERICHHits", \
	"DRICHHits" \
    ]

    bg = get_rate_beam_gas(infile, nsim, det)

    get_rate_pythia6()

    #print(bg)

    idet = 0
    xp = []
    yp = []
    labels = ([], [])
    for i in bg:
        xp.append(idet-0.5)
        xp.append(idet+0.5)

        yp.append(bg[i])
        yp.append(bg[i])

        labels[0].append( idet )
        labels[1].append( i[0:-4] )

        idet += 1

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, yp, "-", color="blue", lw=1)

    #ax.set_xlabel("det")
    ax.set_ylabel("Hits")

    ax.set_yscale("log")

    plt.xticks(labels[0], labels[1], rotation = "vertical")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hit_rate

#_____________________________________________________________________________
def get_rate_beam_gas(infile, nsim, det):

    #total production rate
    total_rate = 3177253.7 # Hz, Eg > 10 keV

    #rate per simulated event
    rsim = total_rate/nsim
    #print("rsim:", rsim)

    inp = TFile.Open(infile)

    rate = {}
    for i in det:
        htree = inp.Get(i)
        #print(i, htree)
        #print(i, htree.GetEntries()*rsim*1e-6)

        rate[i] = htree.GetEntries()*rsim

    #sort by the rate
    rate = dict(sorted(rate.items(), key=lambda item: -item[1]))

    return rate

#get_rate_beam_gas

#_____________________________________________________________________________
def get_rate_pythia6():

    #infile, nsim, det

    #Pythia6 total cross section
    sigma = 40.891e-3 # mb

    #instantaneous luminosity, Table 3.3, 10x100 GeV
    lumi_cmsec = 4.48e33 # cm^-2 sec^-1

    #production rate for Pythia
    prod_rate = sigma*lumi_cmsec*1e-27 # to mb

    print(prod_rate)

#_____________________________________________________________________________
def set_axes_color(ax, col):

    ax.xaxis.label.set_color(col)
    ax.yaxis.label.set_color(col)
    ax.tick_params(which = "both", colors = col)
    ax.spines["bottom"].set_color(col)
    ax.spines["left"].set_color(col)
    ax.spines["top"].set_color(col)
    ax.spines["right"].set_color(col)

#set_axes_color

#_____________________________________________________________________________
def set_grid(px, col="lime"):

    px.grid(True, color = col, linewidth = 0.5, linestyle = "--")

#set_grid

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()





























