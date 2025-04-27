# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/PCBs/Frame/frame.py").read())

import pcbnew

import os, sys
sys.path.append("/home/poluekt/cernbox/devel/OpenRPNCalc4/Hardware/python/")

from primitives import rounded_rectangle, circle
from geometry import pcb_width, pcb_height, corner_x, corner_y, corner_rad, visible_lcd_width, visible_lcd_height, keyboard_width, keyboard_height

board = pcbnew.GetBoard()

def outline() : 
    rounded_rectangle(board, center=(corner_x + pcb_width/2., corner_y + pcb_height/2.), width=pcb_width, height=pcb_height, radius=corner_rad)
    circle(board, center = (corner_x + corner_rad, corner_y + corner_rad), radius=1.1)
    circle(board, center = (corner_x - corner_rad + pcb_width, corner_y + corner_rad), radius=1.1)
    circle(board, center = (corner_x + corner_rad, corner_y - corner_rad + pcb_height), radius=1.1)
    circle(board, center = (corner_x - corner_rad + pcb_width, corner_y - corner_rad + pcb_height), radius=1.1)
    circle(board, center = (corner_x + corner_rad, corner_y + pcb_height/2.), radius=1.1)
    circle(board, center = (corner_x - corner_rad + pcb_width, corner_y + pcb_height/2.), radius=1.1)

keyboard_height = 82.

outline()
rounded_rectangle(board, center=(corner_x + pcb_width/2., corner_y + 6 + 1.5 + visible_lcd_height/2.), width=visible_lcd_width, height=visible_lcd_height, radius=1.)
rounded_rectangle(board, center=(corner_x + pcb_width/2., corner_y + pcb_height - 5. - keyboard_height/2.), width=keyboard_width, height=keyboard_height, radius=1.)

pcbnew.Refresh()
