###-------------------------------------------------------------------
#
""" 
   --> smart fluka to root histogram converter, it can iterate over
       any number of files containg data from fluka for both 1d and 2d
       deposit projections
   --> it is presumed that the file with memory map will always have
       extension .lis!

"""
#
#  @Agnieszka Oblakowska-Mucha
#  @Patryk Pasterny
#  @Tomasz Szumlak
#
#  Run it using:
#  python sf2rconverter -p path_With_FLUKA_Files -n name_Of_FLUKA_File
#
###--------------------------------------------------------------------

# import section
import os, sys, getopt
from commands import getoutput
from sf2r_lib import sf2r_manager
from ROOT import TFile, gPad, TCanvas, gStyle

DEBUG = False
PLOT1D = True
PLOT2D = True
PLOT3D = True

# this is the converter manager code
#---
def main():
   # configure and run
   _MGR = sf2r_manager( DEBUG )
   _MGR.ff_type_detector()
   plots = _MGR.run()
   file = None
   if not os.path.exists( 'fluka2root.root' ):
       file = TFile( 'fluka2root.root', 'new' )
   else:
       file = TFile( 'fluka2root.root', 'recreate' )

   # make a test plot and store plots in file
   for plot in plots:
       if plot.get_type() == '1DPLOT':
           if PLOT1D:
               plot.get_histo().Draw('hist')
               plot.get_histo().Write()
       if plot.get_type() == '2DPLOT':
           if PLOT2D:
               plot.get_histo().Write()
       if plot.get_type() == '3DPLOT':
           if PLOT3D:
               plot.get_histo().Write()


   file.Close()

   #print ' --> Press enter to finish... '
   #raw_input()

if __name__ == "__main__":
    main()



   

