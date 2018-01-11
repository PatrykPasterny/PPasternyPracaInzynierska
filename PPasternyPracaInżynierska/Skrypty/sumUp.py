###-------------------------------------------------------------------
#
""" 
   --> script sum up data in bins for 4 particles: kaons, pions, protons and neutrons and saves histograms with dPhi/dE in 4 sensors to ROOT file
#
#  @Patryk Pasterny
# 
###----------------------------------------------------------------------
# import section

import os, sys, getopt
from commands import getoutput
from ROOT import TFile, gPad, TCanvas, gStyle, TH1F, TH1
from math import *
from array import *

def appendHistos(keyOfHistos, f, histos):
    for key in keyOfHistos:
        histos.append( f.Get( key.GetName() ) )

def sumHistos(histosElse,binX,data_points):
    for histo in histosElse:
        if "neu" not in histo.GetName():
            for index in xrange( binX ):
                data_points[index] += histo.GetBinContent( index + 1 )
        else:
            i=0
            for index in xrange( histo.GetNbinsX() ):
                if histo.GetBinLowEdge( index + 1 ) < 0.2:
                    i+=1
                    data_points[0] += histo.GetBinContent( index+1 )
                else:
                    data_points[index-i+1] += histo.GetBinContent( index+1 )
               
def main():
   # configure and run

    pathROOT_1 = sys.argv[1]
    pathROOT_2 = sys.argv[2]
    pathROOT_3 = sys.argv[3]
    pathROOT_4 = sys.argv[4]

    f1 = TFile( pathROOT_1, 'read' )
    f2 = TFile( pathROOT_2, 'read' )
    f3 = TFile( pathROOT_3, 'read' )
    f4 = TFile( pathROOT_4, 'read' )    

    if not os.path.exists( 'sumup.root' ):
        f5 = TFile( 'sumup.root', 'new' )
    else:
        f5 = TFile( 'sumup.root','recreate' )

    KeysToNamesOfHistos_1 = f1.GetListOfKeys()
    KeysToNamesOfHistos_2 = f2.GetListOfKeys()
    KeysToNamesOfHistos_3 = f3.GetListOfKeys()
    KeysToNamesOfHistos_4 = f4.GetListOfKeys()
    Keys = []

    histos = []
    histo_01 = []
    histo_07 = []
    histo_14 = []
    histo_19 = []

    appendHistos(KeysToNamesOfHistos_1, f1, histos)
    appendHistos(KeysToNamesOfHistos_2, f2, histos)
    appendHistos(KeysToNamesOfHistos_3, f3, histos)
    appendHistos(KeysToNamesOfHistos_4, f4, histos)
 
    for histo in histos:
        if "01" in histo.GetName():
            histo_01.append(histo)
        elif "07" in histo.GetName():
            histo_07.append(histo)
        elif "14" in histo.GetName():
            histo_14.append(histo)
        elif "19" in histo.GetName():
            histo_19.append(histo)

    del histos[:]

    binX = histo_01[1].GetNbinsX()
    startX = histo_01[1].GetXaxis().GetXmin()
    endX = histo_01[1].GetXaxis().GetXmax()
    data_points_01 = [0]*binX
    data_points_07 = [0]*binX
    data_points_14 = [0]*binX
    data_points_19 = [0]*binX
    sumHistos(histo_01,binX,data_points_01)
    sumHistos(histo_07,binX,data_points_07)
    sumHistos(histo_14,binX,data_points_14)
    sumHistos(histo_19,binX,data_points_19)
    
    histos.append( TH1F( "NEQ_01", "NEQ_01",binX,startX,endX ) )
    histos.append( TH1F( "NEQ_07", "NEQ_07",binX,startX,endX ) )
    histos.append( TH1F( "NEQ_14", "NEQ_14",binX,startX,endX ) )
    histos.append( TH1F( "NEQ_19", "NEQ_19",binX,startX,endX ) )

    for index in xrange( binX ):
        histos[0].SetBinContent( index+1, data_points_01[index] )

    for index in xrange( binX ):
        histos[1].SetBinContent( index+1, data_points_07[index] )

    for index in xrange( binX ):
        histos[2].SetBinContent( index+1, data_points_14[index] )

    for index in xrange( binX ):
        histos[3].SetBinContent( index+1, data_points_19[index] )
        
    f5.Close()
    f4.Close()
    f3.Close()
    f2.Close()
    f1.Close()

if __name__ == "__main__":
    main()

