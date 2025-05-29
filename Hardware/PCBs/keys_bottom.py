# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/PCBs/Spacer3/keys_bottom.py").read())

import pcbnew
import math
import os, sys

sys.path.append("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/python/")

from geometry import large_key_w, large_key_h, small_key_w, small_key_h, corner_x, corner_y, pcb_height, pcb_width
from primitives import rounded_rectangle, panelised_rectangle, place_pin, circle

# Load the current board and apply the script
board = pcbnew.GetBoard()

n = 0

def large_keys() : 
    global n
    key_h = large_key_w + 1.0
    key_w = large_key_h + 1.0
    rad = 1.
    step_x = key_w + 2*rad
    step_y = key_h + 2*rad
    dx = corner_x + key_w/2. + 6. + 2.
    dy = corner_y + pcb_height - step_y*3 - 5.5 - 2. - key_h/2.
    for ix in range(5) : 
        for iy in range(4) : 
             x = dx + step_x*ix
             y = dy + step_y*iy
             pos = "C"
             if ix == 0 : pos = "L"
             if ix == 4 : pos = "R"
             panelised_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1., position = pos)
             circle(board, (x, y), 1.5) # Central hole
             place_pin(board, x, y + 3.1, n)
             n += 1
             place_pin(board, x, y - 3.1, n)
             n += 1
             circle(board,  (x - key_w/2., y + 0.6), 0.3) # Mouse bites
             circle(board,  (x - key_w/2., y - 0.6), 0.3)
             circle(board,  (x + key_w/2., y + 0.6), 0.3)
             circle(board,  (x + key_w/2., y - 0.6), 0.3)

def small_keys() : 
    global n
    key_h = small_key_w + 1.0
    key_w = small_key_h + 1.0
    rad = 1.
    step_x = key_w + 2*rad
    step_y = key_h + 2*rad
    
    # For keys places inside keyboard frame
    dx1 = corner_x + key_w/2. + 6. + 2.
    dy1 = corner_y + pcb_height - step_y*3 - 5.5 - 2. - (large_key_w + 1.0 + 2.)*4 - key_h/2.

    # For keys plaince inside LCD frame
    dx2 = corner_x + key_w/2. + 4.9 + 2.
    dy2 = corner_y + 6.0 + 2. + key_h/2.

    for ix in range(6) : 
        for iy in range(4) : 
             if iy < 2 : 
               dy = dy2
               dx = dx2
             else : 
               dy = dy1
               dx = dx1
             x = dx + step_x*ix
             y = dy + step_y*iy
             pos = "C"
             if ix == 0 : pos = "L"
             if ix == 5 : pos = "R"
             panelised_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1., position = pos)
             circle(board, (x, y), 1.5)
             place_pin(board, x, y + 2.95, n)
             n += 1
             place_pin(board, x, y - 2.95, n)
             n += 1
             circle(board,  (x - key_w/2., y + 0.6), 0.3)
             circle(board,  (x - key_w/2., y - 0.6), 0.3)
             circle(board,  (x + key_w/2., y + 0.6), 0.3)
             circle(board,  (x + key_w/2., y - 0.6), 0.3)

def enter_key() : 
    key_h = 18.2 + 1.0
    key_w = small_key_h + 1.0
    rad = 1.
    x = corner_x + key_w/2. + 4.9 + 2.
    y = corner_y + 6.0 + 2. + key_h/2. + (small_key_w + 2.)*2 + 1.
    panelised_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1., position = "C")
    circle(board, (x, y), 1.5)
    place_pin(board, x, y + 2.95, n+1)
    place_pin(board, x, y - 2.95, n+2)
    place_pin(board, x, y + 6.95, n+3)
    place_pin(board, x, y - 6.95, n+4)
    circle(board,  (x - key_w/2., y + 0.6), 0.3)
    circle(board,  (x - key_w/2., y - 0.6), 0.3)
    circle(board,  (x + key_w/2., y + 0.6), 0.3)
    circle(board,  (x + key_w/2., y - 0.6), 0.3)

#large_keys()
#small_keys()
enter_key()

pcbnew.Refresh()
