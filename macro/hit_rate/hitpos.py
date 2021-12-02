#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH2D

import sys
sys.path.append("/home/jaroslav/sim/lmon/macro")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = xypos
    func[1] = rzpos

    func[iplot]()

#main

#_____________________________________________________________________________
def xypos():

    #mm
    #xybin = 1
    #xymax = 490
    #xybin = 10
    #xymax = 2900
    xybin = 10
    xymax = 3900

    #infile = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a/ddhits_pass2.root"
    infile = "/home/jaroslav/sim/Athena/data/pythia6/py10x100a/ddhits_pass2.root"

    #legtxt = "Electron beam-gas"
    legtxt = "Pythia6"

    #det = {"VertexBarrelHits": "blue", "TrackerBarrelHits": "gold", "TrackerEndcapHits": "red"}
    #det = {"EcalEndcapPHits": "blue", "EcalEndcapNHits": "gold", "EcalBarrelHits": "lime"}#, "EcalBarrelScFiHits": "red"}
    det = {"HcalBarrelHits": "blue", "HcalEndcapNHits": "gold", "HcalEndcapPHits": "red"}

    inp = TFile.Open(infile)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    #gStyle.SetPalette(56)

    #detector loop
    for i in det:

        tree = inp.Get(i)
        tree.Draw("y:x >>+hxy")

    hxy.SetXTitle("#it{x} (mm)")
    hxy.SetYTitle("#it{y} (mm)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    hxy.GetXaxis().CenterTitle()
    hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.58, 0.88, 0.1, 0.1, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+legtxt+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#xypos

#_____________________________________________________________________________
def rzpos():

    #mm
    #rzbin = 1
    #rmax = 490
    #zmax = 1800
    #rzbin = 10
    #rmax = 2900
    #zmax = 4100
    rzbin = 10
    rmax = 3900
    zmax = 5500

    #infile = "/home/jaroslav/sim/Athena/data/beam-gas/cnt1a/ddhits_pass2.root"
    infile = "/home/jaroslav/sim/Athena/data/pythia6/py10x100a/ddhits_pass2.root"

    #legtxt = "Electron beam-gas"
    legtxt = "Pythia6"

    #det = {"VertexBarrelHits": "blue", "TrackerBarrelHits": "gold", "TrackerEndcapHits": "red"}
    #det = {"EcalEndcapPHits": "blue", "EcalEndcapNHits": "gold", "EcalBarrelHits": "lime"}#, "EcalBarrelScFiHits": "red"}
    det = {"HcalBarrelHits": "blue", "HcalEndcapNHits": "gold", "HcalEndcapPHits": "red"}

    inp = TFile.Open(infile)

    can = ut.box_canvas()

    hrz = ut.prepare_TH2D("hrz", rzbin, -zmax, zmax, rzbin, 0, rmax)

    #detector loop
    for i in det:

        tree = inp.Get(i)
        tree.Draw("TMath::Sqrt(x*x+y*y):z >>+hrz")

    hrz.SetXTitle("#it{z} (mm)")
    hrz.SetYTitle("Radius #it{r} (mm)")

    hrz.SetTitleOffset(1.6, "Y")
    hrz.SetTitleOffset(1.4, "X")

    hrz.GetXaxis().CenterTitle()
    hrz.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.11)

    hrz.SetMinimum(0.98)
    hrz.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.58, 0.88, 0.1, 0.1, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+legtxt+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rzpos

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()














