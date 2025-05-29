# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/PCBs/Main/place_footprints.py").read())

import pcbnew

import os, sys
sys.path.append("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/python/")

from primitives import rounded_rectangle, milled_rectangle, circle
from geometry import pcb_width, pcb_height, corner_x, corner_y, corner_rad
from geometry import large_keys_coord, small_keys_coord

board = pcbnew.GetBoard()

def outline() : 
    rounded_rectangle(board, center=(corner_x + pcb_width/2., corner_y + pcb_height/2.), width=pcb_width, height=pcb_height, radius=corner_rad)
    circle(board, center = (corner_x + corner_rad, corner_y + corner_rad), radius=1.1)
    circle(board, center = (corner_x - corner_rad + pcb_width, corner_y + corner_rad), radius=1.1)
    circle(board, center = (corner_x + corner_rad, corner_y - corner_rad + pcb_height), radius=1.1)
    circle(board, center = (corner_x - corner_rad + pcb_width, corner_y - corner_rad + pcb_height), radius=1.1)
    circle(board, center = (corner_x + corner_rad, corner_y + pcb_height/2.), radius=1.1)
    circle(board, center = (corner_x - corner_rad + pcb_width, corner_y + pcb_height/2.), radius=1.1)

#outline()

KICAD_VERSION = pcbnew.Version().split(".")[0]
fp_path = os.getenv("KICAD" + KICAD_VERSION + "_FOOTPRINT_DIR", default=None)

n = 1
for x,y in large_keys_coord + small_keys_coord :
  footprint_ref = f"SW{n}"
  footprint = board.FindFootprintByReference(footprint_ref)
  footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
  n += 1

pcbnew.Refresh()
