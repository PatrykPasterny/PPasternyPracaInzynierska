# #-------------------------------------------------------------------
#
""" 
   --> converter fluka->root->tki using sf2r_lib.py and based on sf2rconverter 
       both written by Tomasz Szumlak and Agnieszka Oblatowska-Mucha

"""
#
#  @Kamil Piastowicz
#
###--------------------------------------------------------------------

# import section
import os, sys, getopt, matplotlib
import Tkinter as Tk
from commands import getoutput
from sf2r_lib import sf2r_manager
from ROOT import TFile, gPad, TCanvas, gStyle, TH2D, TH1F
from root2tk import plot_3d_2canvas

DEBUG = False
API = True
PLOT1D = False
PLOT2D = True
PLOT3D = False

# this is the root2tk test code
if __name__ == '__main__':
   # configure and run
   _MGR = sf2r_manager( DEBUG ,API)
   plots = _MGR.run_path("./","final_check10k_70.bnn.lis")
   root = Tk.Tk()
   root.wm_title("ROOT TH1F")  
 
   canvas = []
   for plot in plots:
      canvas.append(plot_3d_2canvas(plot,root))
 
   for cnv in canvas[0]:
      # a tk.DrawingAre
      cnv.show()
      cnv.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

   Tk.mainloop()
   print ' --> Press enter to finish... '
   raw_input()
