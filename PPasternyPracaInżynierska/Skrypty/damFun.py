###-------------------------------------------------------------------
#
""" 
   --> script convert USRTRAC of certain particle into it's neq equality
"""
#
#  @Patryk Pasterny
# 
#  To use type:
#  python damFun.py  particle.root particle.txt
#  in console, where:
#  particle.txt is file with particle damage function
#  particle.root is ROOTfile with USRTRAC TH1F histos of dPhi/dE
#
###----------------------------------------------------------------------
# import section

import os, sys, getopt
from commands import getoutput
from ROOT import TFile, gPad, TCanvas, gStyle, TH1F, TH1
from math import *
from array import *

def getDamageToMultiply(meanEnValue, damFun):

    #print meanEnValue
    lowestSubstraction = meanEnValue
    for index in xrange(1,len(damFun)-1):
        if abs(damFun[index][0] - meanEnValue) < abs(damFun[index + 1][0] - meanEnValue) and abs(damFun[index][0] - meanEnValue) < abs(damFun[index - 1][0] - meanEnValue):
            return damFun[index][1]

    if meanEnValue<damFun[1][0]:
        return damFun[0][1]
    else:
        return damFun[len(damFun)-1][1]              


def main():
   # configure and run

    if len(sys.argv) == 2:
        pathROOT = sys.argv[1]
        pathFile = pathROOT.replace('.root','.txt')

    elif len(sys.argv) == 3:
        pathROOT = sys.argv[1]
        pathFile = sys.argv[2]

    else:
        pathROOT = 'pions.root'
        pathFile = pathROOT.replace('.root','.txt')

    f1 = TFile( pathROOT, 'read' )
    f2 = TFile( pathROOT.replace('.root','neq.root'), 'new')
    if not os.path.exists( pathROOT.replace('.root','neq.root') ):
        f2 = TFile( pathROOT.replace('.root','neq.root'), 'new' )
    else:
        f2 = TFile( pathROOT.replace('.root','neq.root'),'recreate' )

    KeysToNamesOfHistos = f1.GetListOfKeys()
    histos = []
    histos_new = []

    for key in KeysToNamesOfHistos:
        histos.append( f1.Get( key.GetName() ) )
        if len(f1.Get( key.GetName() ).GetXaxis().GetXbins()):
            bins = array('d', f1.Get( key.GetName() ).GetXaxis().GetXbins())
            histos_new.append( TH1F( key.GetName(), key.GetName(), f1.Get( key.GetName() ).GetXaxis().GetNbins(), bins ) )
        else:
            histos_new.append( TH1F( key.GetName(), key.GetName(), f1.Get( key.GetName() ).GetXaxis().GetNbins(), f1.Get( key.GetName() ).GetXmin(), f1.Get( key.GetName() ).GetXmax() ) )

    damageFunctionFile = open(pathFile, 'r')
    damageFunction = []

    for line in damageFunctionFile:
        damageFunction.append((float(line.split('\t')[0].replace(',','.'))/1000.0, float(line.split('\t')[1].replace(',','.'))))
    damageFunctionFile.close()

    i = 0
    for histo in histos:
        startX = histo.GetXaxis().GetXmin()
        endX = histo.GetXaxis().GetXmax()
        binX = histo.GetNbinsX()
        ResX = ( endX - startX ) / float ( binX )
        for index in xrange( histo.GetNbinsX() ):
           xcenter = startX + ( index * ResX) + ResX/2
           histos_new[i].SetBinContent( index+1, histo.GetBinContent(index+1) * getDamageToMultiply( xcenter, damageFunction))
           #print index
           #print histo.GetXaxis().GetBinLowEdge(index+1)
           #print histo.GetXaxis().GetBinUpEdge(index+1) 
        histos_new[i].Write()
        i+=1

    f2.Close()
    f1.Close()

if __name__ == "__main__":
    main()
