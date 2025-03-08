# Keyboard switch placement script for KiCAD. 
# To run, open "Tools/Scripting console" and run 
#    exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc_keyboard/pcb_placement.py").read())

import pcbnew
import os
import math

KICAD_VERSION = pcbnew.Version().split(".")[0]
fp_path = os.getenv("KICAD" + KICAD_VERSION + "_FOOTPRINT_DIR", default=None)

# Parameters
FOOTPRINT_REF_LARGE = [f"SW{i+1}" for i in range(20)]
FOOTPRINT_REF_SMALL = [f"SW{i+21}" for i in range(24)]

center_x = 100.
center_y = 97.2
pcb_width = 73.
pcb_height = 134.4

BOTTOM_Y = center_y + pcb_height/2.

GRID_SPACING_LARGE_X = pcbnew.FromMM(12.3)  # Grid spacing in mm
GRID_SPACING_LARGE_Y = pcbnew.FromMM(10.0)  # Grid spacing in mm
START_POSITION_LARGE = (pcbnew.FromMM(center_x - 12.3*2.), pcbnew.FromMM(BOTTOM_Y - 9.))  # Starting position (x, y) in mm

GRID_SPACING_SMALL_X = pcbnew.FromMM(10.2)  # Grid spacing in mm
GRID_SPACING_SMALL_Y = pcbnew.FromMM(9.2)  # Grid spacing in mm
START_POSITION_SMALL = (pcbnew.FromMM(center_x - 10.2*2.5), pcbnew.FromMM(BOTTOM_Y - 49.))  # Starting position (x, y) in mm

# Get the current board
board = pcbnew.GetBoard()

x_start, y_start = START_POSITION_LARGE
x = x_start
y = y_start
n = 0
for j in range(4):
  for i in range(5):
    footprint = board.FindFootprintByReference(FOOTPRINT_REF_LARGE[n])
    footprint.SetPosition(pcbnew.VECTOR2I(x, y))

    print(f"Placed {FOOTPRINT_REF_LARGE[n]} at {pcbnew.ToMM(x)} mm, {pcbnew.ToMM(y)} mm.")
    x += GRID_SPACING_LARGE_X
    n += 1
  x = x_start
  y -= GRID_SPACING_LARGE_Y

x_start, y_start = START_POSITION_SMALL
x = x_start
y = y_start
n = 0
for j in range(4):
  for i in range(6):
    footprint = board.FindFootprintByReference(FOOTPRINT_REF_SMALL[n])
    footprint.SetPosition(pcbnew.VECTOR2I(x, y))

    print(f"Placed {FOOTPRINT_REF_SMALL[n]} at {pcbnew.ToMM(x)} mm, {pcbnew.ToMM(y)} mm.")
    x += GRID_SPACING_SMALL_X
    n += 1
  x = x_start
  y -= GRID_SPACING_SMALL_Y

def rounded_rectangle(center, width, height, radius, layer=pcbnew.Edge_Cuts):
    """
    Draws a rounded rectangle on the specified layer using lines and arcs.
    
    :param board: The PCB board object
    :param center: Tuple (x, y) of the rectangle's center in millimeters
    :param width: Width of the rectangle in millimeters
    :param height: Height of the rectangle in millimeters
    :param radius: Corner radius in millimeters
    :param layer: The PCB layer to draw on (default is F.Cu)
    """
    # Convert millimeters to internal PCB units (nanometers)
    def to_nm(value):
        return pcbnew.FromMM(value)

    # Convert degrees to KiCAD's `EDA_ANGLE` (which expects tenths of a degree)
    def to_kicad_angle(deg):
        return pcbnew.EDA_ANGLE(deg, pcbnew.DEGREES_T)

    # Center point in KiCAD units
    cx, cy = to_nm(center[0]), to_nm(center[1])
    w2, h2 = to_nm(width / 2), to_nm(height / 2)
    r = to_nm(radius)

    # Corner arc centers
    corners = {
        "TL": (cx - w2 + r, cy - h2 + r),
        "TR": (cx + w2 - r, cy - h2 + r),
        "BR": (cx + w2 - r, cy + h2 - r),
        "BL": (cx - w2 + r, cy + h2 - r),
    }

    # Define the straight-line segments
    lines = [
        ((corners["TL"][0], corners["TL"][1] - r), (corners["TR"][0], corners["TR"][1] - r)),  # Top
        ((corners["TR"][0] + r, corners["TR"][1]), (corners["BR"][0] + r, corners["BR"][1])),  # Right
        ((corners["BR"][0], corners["BR"][1] + r), (corners["BL"][0], corners["BL"][1] + r)),  # Bottom
        ((corners["BL"][0] - r, corners["BL"][1]), (corners["TL"][0] - r, corners["TL"][1])),  # Left
    ]

    # Draw the lines
    for start, end in lines:
        line = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(pcbnew.VECTOR2I(*start))
        line.SetEnd(pcbnew.VECTOR2I(*end))
        line.SetLayer(layer)
        board.Add(line)

    # Define the arcs
    arcs = [
        (corners["TR"], 90, 180),  # Bottom Right
        (corners["BR"], 0, 90),    # Top Right
        (corners["BL"], 270, 360), # Top Left
        (corners["TL"], 180, 270), # Bottom Left
    ]

    # Draw the arcs
    for center, start_angle, end_angle in arcs:
        arc = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_ARC)
        arc.SetCenter(pcbnew.VECTOR2I(*center))
        
        # Compute start point for the arc
        start_x = center[0] + r * math.cos(math.radians(start_angle))
        start_y = center[1] - r * math.sin(math.radians(start_angle))
        arc.SetStart(pcbnew.VECTOR2I(int(start_x), int(start_y)))

        # Set the angle span using `EDA_ANGLE`
        arc.SetArcAngleAndEnd(to_kicad_angle(end_angle - start_angle))

        arc.SetLayer(layer)
        board.Add(arc)

def circle(center, radius, layer=pcbnew.Edge_Cuts) : 
    circ = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_CIRCLE)
    circ.SetCenter(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1])))
    circ.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1]+radius)))
    circ.SetLayer(pcbnew.Edge_Cuts)
    board.Add(circ)

def outline() : 
    corner_rad = 2.7
    rounded_rectangle(center=(center_x, center_y), width=pcb_width, height=pcb_height, radius=corner_rad)
    circle(center = (center_x - pcb_width/2. + corner_rad, center_y - pcb_height/2. + corner_rad), radius=1.1)
    circle(center = (center_x + pcb_width/2. - corner_rad, center_y - pcb_height/2. + corner_rad), radius=1.1)
    circle(center = (center_x - pcb_width/2. + corner_rad, center_y + pcb_height/2. - corner_rad), radius=1.1)
    circle(center = (center_x + pcb_width/2. - corner_rad, center_y + pcb_height/2. - corner_rad), radius=1.1)
    circle(center = (center_x - pcb_width/2. + corner_rad, center_y), radius=1.1)
    circle(center = (center_x + pcb_width/2. - corner_rad, center_y), radius=1.1)

outline()

# Refresh the PCB view
pcbnew.Refresh()
