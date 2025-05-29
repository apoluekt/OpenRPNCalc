# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/PCBs/Spacer1/spacer.py").read())

import pcbnew

import os, sys
sys.path.append("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/python/")

from primitives import rounded_rectangle, milled_rectangle, circle, arc, line
from geometry import large_keys_coord, small_keys_coord

board = pcbnew.GetBoard()

def large_keys() : 
    w = 6.5
    h = 6.0
    step = 12.3
    for x,y in large_keys_coord : 
      line(board, x-w/2., y-h/2., x+w/2., y-h/2.)
      line(board, x-w/2., y+h/2., x+w/2., y+h/2.)
      arc(board, (x+w/2., y+h/2.-1), 1., 0., 90.)
      arc(board, (x+w/2., y-h/2.+1), 1., 90., 180.)
      arc(board, (x-w/2., y+h/2.-1), 1., 270., 360.)
      arc(board, (x-w/2., y-h/2.+1), 1., 180., 270.)
      line(board, x-w/2.-1, y-h/2.+1, x-w/2.-step+w+1., y-h/2.+1)
      line(board, x-w/2.-1, y+h/2.-1, x-w/2.-step+w+1., y+h/2.-1)

def small_keys() : 
    w = 6.5
    h = 6.0
    step = 10.2
    for n,(x,y) in enumerate(small_keys_coord) : 
      line(board, x-w/2., y-h/2., x+w/2., y-h/2.)
      line(board, x-w/2., y+h/2., x+w/2., y+h/2.)
      arc(board, (x+w/2., y+h/2.-1), 1., 0., 90.)
      arc(board, (x+w/2., y-h/2.+1), 1., 90., 180.)
      arc(board, (x-w/2., y+h/2.-1), 1., 270., 360.)
      arc(board, (x-w/2., y-h/2.+1), 1., 180., 270.)
      line(board, x-w/2.-1, y-h/2.+1, x-w/2.-step+w+1., y-h/2.+1)
      line(board, x-w/2.-1, y+h/2.-1, x-w/2.-step+w+1., y+h/2.-1)

large_keys()
small_keys()
pcbnew.Refresh()
