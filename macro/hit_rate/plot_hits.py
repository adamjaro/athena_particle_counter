#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D

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

    #infile = "../ddhits/ddhits.root"
    #infile = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a/ddhits_pass2.root"
    infile = "/home/jaroslav/sim/Athena/data/pythia6/py10x100a/ddhits_pass2.root"

    #legtxt = "Electron beam-gas"
    legtxt = "Pythia6"

    #det = {"VertexBarrelHits": "blue", "TrackerBarrelHits": "gold", "TrackerEndcapHits": "red"}
    #det = {"EcalEndcapPHits": "blue", "EcalEndcapNHits": "gold", "EcalBarrelHits": "lime", "EcalBarrelScFiHits": "red"}
    det = {"HcalBarrelHits": "blue", "HcalEndcapNHits": "gold", "HcalEndcapPHits": "red"}
    #det = {"HcalBarrelHits": "blue", "HcalEndcapNHits": "gold"}

    inp = TFile.Open(infile)

    ep = {}
    for i in det:
        ep[i] = get_hit_en(inp, i)

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    leg.add_entry(leg_txt(), legtxt)

    for i in ep:

        plt.plot(ep[i][0], ep[i][1], "-", color=det[i], lw=1)
        leg.add_entry(leg_lin(det[i]), i[0:-4])

    ax.set_xlabel("Hit energy (keV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i)+"}$" for i in ax.get_xticks()[1:-1]])
    #plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.1f}".format(i)+"}$" for i in ax.get_xticks()[1:-1]])

    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hit_en

#_____________________________________________________________________________
def get_hit_en(inp, det):

    #log_10(keV)
    emin = -9
    emax = 9
    ebin = 0.1

    htree = inp.Get(det)

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    #htree.Draw("TMath::Log10(en*1e6) >> hE") # keV
    htree.Draw("TMath::Log10(en*1e6) >> hE", "en>0.4*1e-6") # keV

    ut.norm_to_integral(hE, 1.)

    return ut.h1_to_arrays(hE)

#get_hit_en

#_____________________________________________________________________________
def hit_rate():

    #hit rate

    #infile = "../ddhits/ddhits.root"
    #infile = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a/ddhits_f1000.root"
    infile = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a/ddhits_pass2.root"

    #number of simulated events
    nsim = 1e6

    #detectors
    det = [ \
	"VertexBarrelHits", \
	"EcalEndcapPHits", \
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

    #divide factors
    divide = {}
    divide["HcalEndcapPHits"] = 51. # number of layers
    divide["ERICHHits"] = 3. # quantum efficiency
    divide["DRICHHits"] = 3. # quantum efficiency

    bg = get_rate_beam_gas(infile, nsim, det, divide)

    #in_py = "/home/jaroslav/sim/Athena/data/pythia6/py10x100a/ddhits_f10.root"
    in_py = "/home/jaroslav/sim/Athena/data/pythia6/py10x100a/ddhits_pass2.root"
    nsim_py = 44000.

    py = get_rate_pythia6(in_py, nsim_py, det, divide)

    #print(py)

    idet = 0
    xp = []
    yp = []
    ypy = []
    labels = ([], [])
    for i in bg:
        xp.append(idet-0.5)
        xp.append(idet+0.5)

        yp.append(bg[i])
        yp.append(bg[i])

        ypy.append(py[i])
        ypy.append(py[i])

        labels[0].append( idet )
        labels[1].append( i[0:-4] )

        idet += 1

    #print(xp)
    #print(yp)

    #table
    print(r"Detector & $R_h$ (MHz), Electron beam-gas & $R_h$ (MHz), Pythia6 \\")
    for i in bg:
        #print(i[0:-4], " & {0:.3f}".format(bg[i]*1e-6), " & {0:.3f}".format(py[i]*1e-6), r"\\") # MHz
        #print(i[0:-4], " & {0:.3f}".format(bg[i]*1e-6), r"\\") # MHz
        print(i[0:-4], r" & \si{\num{"+"{0:.6f}".format(bg[i]*1e-6)+"}}", r" & \si{\num{"+"{0:.6f}".format(py[i]*1e-6)+"}}", r"\\") # MHz

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, ypy, "-", color="blue", lw=1)
    plt.plot(xp, yp, "-", color="red", lw=1)

    ax.set_ylabel("Number of hits per second")

    ax.set_yscale("log")

    plt.xticks(labels[0], labels[1], rotation = "vertical")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Electron beam-gas, 10 GeV")
    leg.add_entry(leg_lin("blue"), "Pythia6, 10x100 GeV")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hit_rate

#_____________________________________________________________________________
def get_rate_beam_gas(infile, nsim, det, divide):

    #total production rate
    total_rate = 3177253.7 # Hz, Eg > 10 keV

    #rate per simulated event
    rsim = total_rate/nsim
    #print("rsim:", rsim)

    inp = TFile.Open(infile)

    rate = {}
    for i in det:
        htree = inp.Get(i)

        rate[i] = htree.GetEntries()*rsim

        if divide.get(i) is not None:
            rate[i] = rate[i]/divide[i]

    #sort by the rate
    rate = dict(sorted(rate.items(), key=lambda item: -item[1]))

    return rate

#get_rate_beam_gas

#_____________________________________________________________________________
def get_rate_pythia6(infile, nsim, det, divide):

    #Pythia6 total cross section
    sigma = 40.891e-3 # mb

    #instantaneous luminosity, Table 3.3, 10x100 GeV
    lumi_cmsec = 4.48e33 # cm^-2 sec^-1

    #production rate for Pythia
    prod_rate = sigma*lumi_cmsec*1e-27 # to mb

    #rate per simulated event
    rsim = prod_rate/nsim
    #print("rsim:", rsim)

    inp = TFile.Open(infile)

    rate = {}
    for i in det:
        htree = inp.Get(i)

        rate[i] = htree.GetEntries()*rsim

        if divide.get(i) is not None:
            rate[i] = rate[i]/divide[i]

    #sort by the rate
    #rate = dict(sorted(rate.items(), key=lambda item: -item[1]))

    return rate

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
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, col=None, **kw):
        leg = px.legend(self.items, self.data, **kw)
        if col != None:
            px.setp(leg.get_texts(), color=col)
            if col != "black":
                leg.get_frame().set_edgecolor("orange")
        return leg

#_____________________________________________________________________________
def leg_lin(col, sty="-"):
    return Line2D([0], [0], lw=2, ls=sty, color=col)

#_____________________________________________________________________________
def leg_txt():
    return Line2D([0], [0], lw=0)

#_____________________________________________________________________________
def leg_dot(fig, col, siz=8):
    return Line2D([0], [0], marker="o", color=fig.get_facecolor(), markerfacecolor=col, markersize=siz)

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()





























