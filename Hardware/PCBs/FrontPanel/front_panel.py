# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/PCBs/FrontPanel/front_panel.py").read())

import pcbnew

import os, sys
sys.path.append("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/python/")

from primitives import rounded_rectangle, milled_rectangle, circle
from geometry import pcb_width, pcb_height, corner_x, corner_y, corner_rad, lcd_width, lcd_height
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

def large_keys() : 
    key_w = 10.3
    key_h = 7.0
    for x,y in large_keys_coord : 
        rounded_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1.)

def small_keys() : 
    key_w = 8.2
    key_h = 5.2
    for n,(x,y) in enumerate(small_keys_coord) : 
        if n == 4 : 
            rounded_rectangle(board, center=(x, y), width=18.4, height=key_h, radius=1.)
        else : 
            rounded_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1.)

outline()
milled_rectangle(board, center=(corner_x + pcb_width/2., corner_y + 6 + lcd_height/2.), width=lcd_width, height=lcd_height, radius=1.)
large_keys()
small_keys()
pcbnew.Refresh()
