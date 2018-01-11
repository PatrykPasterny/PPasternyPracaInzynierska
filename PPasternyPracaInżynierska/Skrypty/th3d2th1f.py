###-------------------------------------------------------------------
#
""" 
   --> scrypt make TH1F histos from TH3D charts and projected on each axis.
"""
#
#  @Patryk Pasterny
#  
#To use type:
#python th3d2th1f.py file.root rpz   - if you want to project it on RPhiZ axes.
#python th3d2th1f.py file.root xyz   - if you want to project it on XYZ axes.
#in console, where:
#file.root is ROOTfile with USRBIN TH3D chart.
###----------------------------------------------------------------------
# import section

import os, sys, getopt
from commands import getoutput
from ROOT import TFile, gPad, TCanvas, gStyle, TH1F, TH1, TH3D, TH3
from math import *             

def main():
   # configure and run
    selectedOption = "z"
    if len(sys.argv) == 2:
        pathROOT = sys.argv[1]
        selectedOption = "rpz"
    elif len(sys.argv) == 3:
        pathROOT = sys.argv[1]
        selectedOption = sys.argv[2]
    else:
        pathROOT = 'fluka2root_one_detector.root'
        selectedOption = "rpz"

    f1 = TFile( pathROOT, 'read' )
    if not os.path.exists( pathROOT.replace('.root','TH1F.root') ):
        f2 = TFile( pathROOT.replace('.root','TH1F.root'), 'new' )
    else:
        f2 = TFile( pathROOT.replace('.root','TH1F.root'),'recreate' )

    KeysToNamesOfHistos = f1.GetListOfKeys()
    histos3D = []
    histos1D = []

    for key in KeysToNamesOfHistos:
       histo3DName = key.GetName()
       if "TH3D" in str( type( f1.Get( histo3DName ) ) ):
           histos3D.append( f1.Get( histo3DName ) )
    
    for histo3D in histos3D:
        startX = histo3D.GetXaxis().GetXmin()
        startY = histo3D.GetYaxis().GetXmin()
        startZ = histo3D.GetZaxis().GetXmin()
        endX = histo3D.GetXaxis().GetXmax()
        endY = histo3D.GetYaxis().GetXmax()
        endZ = histo3D.GetZaxis().GetXmax()
        startBinX = 0
        startBinY = 0
        startBinZ = 0
        binX = histo3D.GetNbinsX()
        binY = histo3D.GetNbinsY()
        binZ = histo3D.GetNbinsZ()
        ResX = ( endX - startX ) / float( binX )
        ResY = ( endY - startY ) / float( binY )
        ResZ = ( endZ - startZ ) / float( binZ )
        print "Na osi X jest: " + str( binX ) + " binow, na osi Y jest: " + str( binY ) + " binow, a na osi Z jest: " + str( binZ ) + " binow."
        print "Os X rozciaga sie miedzy wartoscia: " + str( startX ) + " ,a wartoscia: " + str( endX ) + "."
        print "Os Y miedzy: " + str( startY ) + " , a wartoscia: " + str( endY ) + "."
        print "Os Z miedzy: " + str( startZ ) + " , a wartoscia: " + str( endZ ) + "."
        print "Odleglosc miedzy binami osi X: " + str( ResX ) + ". Miedzy binami osi Y: " + str( ResY ) + ". Miedzy binami osi Z: " + str( ResZ )
        #PROJECTION X / R
        data_points = [0] * binX
        for singleBinX in xrange( binX ):
            for singleBinY in xrange( binY ):
                for singleBinZ in xrange( binZ ):
                    data_points[ singleBinX ] += histo3D.GetBinContent( singleBinX, singleBinY, singleBinZ  )

            data_points[ singleBinX ] /= binZ * binY                

        histos1D.append( TH1F( "Projection" + "X" + " OF " + histo3D.GetName(), "Projection" + "X" + " OF " + histo3D.GetName(), int( binX ), float( startX + ResX * startBinX ), float( endX ) ) )
            
        for indx, data_point in enumerate( data_points ):
            histos1D[ len( histos1D ) - 1 ].SetBinContent( indx + 1, data_point )
        #PROJECTION Y / Phi
        data_points = [0] * binY
        for singleBinY in xrange( binY ):
            for singleBinZ in xrange( binZ ):
                for singleBinX in xrange( binX ):
                    data_points[ singleBinY ] += histo3D.GetBinContent( singleBinX, singleBinY, singleBinZ  )

            data_points[ singleBinY ] /= binX * binZ                

        if selectedOption == "xyz":
            axis = "Y"
        else:
            axis = "Phi"

        histos1D.append( TH1F( "Projection" + axis + " OF " + histo3D.GetName(), "Projection" + axis + " OF " + histo3D.GetName(), int( binY ), float( startY + ResY * startBinY ), float( endY ) ) )
            
        for indx, data_point in enumerate( data_points ):
            histos1D[ len( histos1D ) - 1 ].SetBinContent( indx + 1, data_point )

        #PROJECTION Z 
        if selectedOption == "rpz":
            surface = 0.0
            data_points = [0] * binZ
            for singleBinZ in xrange( startBinZ, binZ ):
                for singleBinY in xrange( startBinY, binY ):
                    for singleBinX in xrange( startBinX, binX ):
                        xcenter = startX + (singleBinX * ResX) + ResX/2
                        data_points[ singleBinZ ] += (histo3D.GetBinContent( singleBinX, singleBinY, singleBinZ ) * ResX * xcenter * ResY )
                        surface += ResX * xcenter * ResY
                data_points[ singleBinZ ] /= surface
                surface = 0.0
            histos1D.append( TH1F( "Projection" + "Z" + " OF " + histo3D.GetName(), "Projection" + "Z" + " OF " + histo3D.GetName(), int( binZ ), float( startZ + ResZ * startBinZ ), float( endZ ) ) )
            
            for indx, data_point in enumerate( data_points ):
                histos1D[ len( histos1D ) - 1 ].SetBinContent( indx + 1, data_point )

        if selectedOption == "xyz":
            data_points = [0] * binZ
            for singleBinZ in xrange( startBinZ, binZ ):
                for singleBinY in xrange( startBinY, binY ):
                    for singleBinX in xrange( startBinX, binX ):
                        data_points[ singleBinZ ] += histo3D.GetBinContent( singleBinX, singleBinY, singleBinZ )
                data_points[ singleBinZ ] /=  ResX*ResY

            histos1D.append( TH1F( "Projection" + "Z" + " OF " + histo3D.GetName(), "Projection" + "Z" + " OF " + histo3D.GetName(), int( binZ ), float( startZ + ResZ * startBinZ ), float( endZ ) ) )
            
            for indx, data_point in enumerate( data_points ):
                histos1D[ len( histos1D ) - 1 ].SetBinContent( indx + 1, data_point )

    #set for apperance
    c = TCanvas('f2r_test', 'f2r Test', 600, 400)
    gStyle.SetPalette(1)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)

    for histo1D in histos1D:
        histo1D.Draw("hist")
        histo1D.Write()
        print ' --> Press enter to finish... '
        raw_input()

    f2.Close()
    f1.Close()

if __name__ == "__main__":
    main()
