#!/usr/bin/python3

from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np

from EventStore import EventStore

from ROOT import TVector3

#_____________________________________________________________________________
def main():

    iplot = 0
    func = {}
    func[0] = fit_x_csv
    func[1] = fit_y_csv 

    func[101] = hits_xyz

    func[iplot]()

#main

#_____________________________________________________________________________
def fit_x_csv():

    infile = "Q3.csv"

    inp = read_csv(infile)

    nbins = 60

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = plt.hist(inp["xhit"], bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, hx[0])
    #pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, hx[0], p0=[-45, 1])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    ax.set_xlabel("$x$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_x$ (mm): {0:.3f} $\pm$ {1:.3f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "3$\sigma_x$ (mm): {0:.3f} $\pm$ {1:.3f}".format( 3.*pars[1], 3.*np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    log = open("out.txt", "w")
    log.write("    dd mx (mm):  {0:.3f} +/- {1:.3f}\n".format( pars[0], np.sqrt(cov[0,0]) ))
    log.write("       3sx (mm): {0:.3f} +/- {1:.3f}\n".format( 3.*pars[1], 3.*np.sqrt(cov[1,1]) ))

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#fit_x_csv

#_____________________________________________________________________________
def fit_y_csv():

    infile = "Q3.csv"

    inp = read_csv(infile)

    nbins = 60

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #fitran = [-1, 1]
    #inp = inp[ inp["y"].between(fitran[0], fitran[1], inclusive=False) ]

    hy = plt.hist(inp["yhit"], bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hy[1][1:]+hy[1][:-1]))
    fit_data = DataFrame({"y": centers, "density": hy[0]})
    #fitran = [-0.5, 0.5]
    #fit_data = fit_data[ fit_data["y"].between(fitran[0], fitran[1], inclusive=False) ] # select the data to the range
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["y"], fit_data["density"]) # , p0=[0,1]

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    ax.set_xlabel("$y$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_y$ (mm): {0:.3f} $\pm$ {1:.3f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "3$\sigma_y$ (mm): {0:.3f} $\pm$ {1:.3f}".format( 3.*pars[1], 3.*np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    log = open("out.txt", "w")
    log.write("    dd my (mm):  {0:.3f} +/- {1:.3f}\n".format( pars[0], np.sqrt(cov[0,0]) ))
    log.write("       3sy (mm): {0:.3f} +/- {1:.3f}\n".format( 3.*pars[1], 3.*np.sqrt(cov[1,1]) ))

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#fit_y_csv

#_____________________________________________________________________________
def hits_xyz():

    infile = "../../output.root"
    detector = "ParticleCounter"

    #Q3eR location
    x0 = -460.027 # mm
    z0 = -37696.067 # mm
    theta0 = 0.0180766389 # rad

    store = EventStore([infile])

    nev = 0 # all events
    nev_hit = 0 # events with hits
    #xhit = []
    #yhit = []
    #zhit = []
    dcol = ["xhit", "yhit", "zhit"]
    val = []

    nbins = 60

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    nmax = -40

    #event loop
    ii = 0
    for iev, evt in enumerate(store):

        nev += 1
        was_hit = False

        #hit loop
        for ihit in store.get(detector):

            ii += 1
            if nmax > 0 and ii > nmax: break

            hpos = ihit.position()

            #global to local
            pos = TVector3(hpos.x-x0, hpos.y, hpos.z-z0)
            pos.RotateY(-theta0)

            #xhit.append(pos.X())
            #yhit.append(pos.Y())
            #zhit.append(pos.Z())

            val.append([pos.X(), pos.Y(), pos.Z()])

            was_hit = True

        #hit loop

        if was_hit: nev_hit += 1

    #event loop

    df = DataFrame(val, columns=dcol)
    df.to_csv("Q3.csv")

    print("All events:", nev)
    print("Events with hits:", nev_hit)

    #plt.hist2d(df["xhit"], df["yhit"], bins=nbins)
    #cbar = plt.colorbar()
    #ax.set_xlabel("x (mm)")
    #ax.set_ylabel("y (mm)")

    plt.hist(df["zhit"], bins=nbins, color="blue", density=True, histtype="step", lw=2)
    ax.set_xlabel("z (mm)")
    ax.set_ylabel("Normalized counts")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hits_xyz

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
        if col is not None:
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

    main()



