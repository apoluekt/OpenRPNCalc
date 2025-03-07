# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc_spacer2/keys_bottom.py").read())

import pcbnew
import math
import os

KICAD_VERSION = pcbnew.Version().split(".")[0]
fp_path = os.getenv("KICAD" + KICAD_VERSION + "_FOOTPRINT_DIR", default=None)

pcb_width = 73.
pcb_height = 134.4

center_x = 100
center_y = 97.2

# Load the current board and apply the script
board = pcbnew.GetBoard()

def circle(center, radius, layer=pcbnew.Edge_Cuts) : 
    circ = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_CIRCLE)
    circ.SetCenter(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1])))
    circ.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1]+radius)))
    circ.SetLayer(pcbnew.Edge_Cuts)
    board.Add(circ)

def panelised_rectangle(center, width, height, radius, bridge = 3., position = "C"):
    """
    Draws a rounded rectangle on the specified layer using lines and arcs.

    :param center: Tuple (x, y) of the rectangle's center in millimeters
    :param width: Width of the rectangle in millimeters
    :param height: Height of the rectangle in millimeters
    :param radius: Corner radius in millimeters
    :param bridge: Width of the panelisation bridge
    """
    layer=pcbnew.Edge_Cuts

    # Convert millimeters to internal PCB units (nanometers)
    def to_nm(value):
        return pcbnew.FromMM(value)

    # Convert degrees to KiCAD's `EDA_ANGLE` (which expects tenths of a degree)
    def to_kicad_angle(deg):
        return pcbnew.EDA_ANGLE(deg, pcbnew.DEGREES_T)

    def add_arc(center, radius, position) : 
      corner = {
        "TR" : (90, 180),  # Top Right
        "BR" : (0, 90),    # Bottom Right
        "BL" : (270, 360), # Bottom Left
        "TL" : (180, 270), # Top Left
      }
      start_angle, end_angle = corner[position]
      arc = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_ARC)
      arc.SetCenter(pcbnew.VECTOR2I(*center))

      # Compute start point for the arc
      start_x = center[0] + radius * math.cos(math.radians(start_angle))
      start_y = center[1] - radius * math.sin(math.radians(start_angle))
      arc.SetStart(pcbnew.VECTOR2I(int(start_x), int(start_y)))

      # Set the angle span using `EDA_ANGLE`
      arc.SetArcAngleAndEnd(to_kicad_angle(end_angle - start_angle))
      arc.SetLayer(layer)
      board.Add(arc)

    def add_line(start, end) : 
      line = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
      line.SetStart(pcbnew.VECTOR2I(*start))
      line.SetEnd(pcbnew.VECTOR2I(*end))
      line.SetLayer(layer)
      board.Add(line)

    # Center point in KiCAD units
    cx, cy = to_nm(center[0]), to_nm(center[1])
    w2, h2 = to_nm(width / 2), to_nm(height / 2)
    b2 = to_nm(bridge/2)
    r = to_nm(radius)
    r2 = to_nm(2*radius)

    # Corner arc centers
    corners = {
        "TL": (cx - w2 + r, cy - h2 + r),
        "TR": (cx + w2 - r, cy - h2 + r),
        "BR": (cx + w2 - r, cy + h2 - r),
        "BL": (cx - w2 + r, cy + h2 - r),
    }

    bridge_corners = {
        "BR": (cx - w2 - r, cy - b2 - r),
        "BL": (cx + w2 + r, cy - b2 - r),
        "TR": (cx - w2 - r, cy + b2 + r),
        "TL": (cx + w2 + r, cy + b2 + r),
    }

    # Define the straight-line segments
    lines = [
        ((corners["TL"][0], corners["TL"][1] - r), (corners["TR"][0], corners["TR"][1] - r)),  # Top
        ((corners["BR"][0], corners["BR"][1] + r), (corners["BL"][0], corners["BL"][1] + r)),  # Bottom
        ((corners["BL"][0] - r, corners["BL"][1]), (bridge_corners["TR"][0] + r, bridge_corners["TR"][1])),  # Left
        ((corners["TL"][0] - r, corners["TL"][1]), (bridge_corners["BR"][0] + r, bridge_corners["BR"][1])),  # Left
        ((corners["TR"][0] + r, corners["TR"][1]), (bridge_corners["BL"][0] - r, bridge_corners["BL"][1])),  # Right
        ((corners["BR"][0] + r, corners["BR"][1]), (bridge_corners["TL"][0] - r, bridge_corners["TL"][1])),  # Right
    ]

    # Draw the lines
    for start, end in lines:
        add_line(start, end)

    for pos, cent in list(corners.items()) + list(bridge_corners.items()) : 
        add_arc(cent, r, pos)

    if position == "L" : 
        add_arc((cx - w2 - r, cy - b2 - r), r, "BL")
        add_arc((cx - w2 - r, cy + b2 + r), r, "TL")
        add_line((cx - w2 - r2, cy - h2 - r), (cx - w2 - r2, cy - b2 - r))
        add_line((cx - w2 - r2, cy + h2 + r), (cx - w2 - r2, cy + b2 + r))

    if position == "R" : 
        add_arc((cx + w2 + r, cy - b2 - r), r, "BR")
        add_arc((cx + w2 + r, cy + b2 + r), r, "TR")
        add_line((cx + w2 + r2, cy - h2 - r), (cx + w2 + r2, cy - b2 - r))
        add_line((cx + w2 + r2, cy + h2 + r), (cx + w2 + r2, cy + b2 + r))

def place_pin(x, y, n) : 
    PIN_LIB = "Connector_Wire.pretty"
    PIN_NAME = "SolderWire-0.5sqmm_1x01_D0.9mm_OD2.1mm"
    pin_fp = pcbnew.FootprintLoad(fp_path + PIN_LIB, PIN_NAME)
    pin_fp.SetReference(f"P{n+1}a")
    pin_fp.SetValue("")
    pin_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    pin_fp.Reference().SetVisible(False)
    board.Add(pin_fp)

n = 0

def large_keys() : 
    global n
    key_h = 11.1 + 0.8
    key_w = 7. + 0.8
    rad = 1.
    step_x = key_w + 2*rad
    step_y = key_h + 2*rad
    dx = center_x - pcb_width/2. + key_w/2. + 6. + 2.
    dy = center_y + pcb_height/2. - step_y*3 - 5.5 - 2. - key_h/2.
    for ix in range(5) : 
        for iy in range(4) : 
             x = dx + step_x*ix
             y = dy + step_y*iy
             pos = "C"
             if ix == 0 : pos = "L"
             if ix == 4 : pos = "R"
             panelised_rectangle(center=(x, y), width=key_w, height=key_h, radius=1., position = pos)
             circle((x, y), 1.5)
             place_pin(x, y + 3.1, n)
             n += 1
             place_pin(x, y - 3.1, n)
             n += 1
             circle( (x - key_w/2. - 0.3, y + 0.6), 0.3)
             circle( (x - key_w/2. - 0.3, y - 0.6), 0.3)
             circle( (x + key_w/2. + 0.3, y + 0.6), 0.3)
             circle( (x + key_w/2. + 0.3, y - 0.6), 0.3)

def small_keys() : 
    global n
    key_h = 9.2 + 0.4
    key_w = 6.2 + 0.8
    rad = 1.
    step_x = key_w + 2*rad
    step_y = key_h + 2*rad
    dx = center_x - pcb_width/2. + key_w/2. + 6. + 2.
    dy = center_y + pcb_height/2. - step_y*3 - 5.5 - 2. - (11.1 + 0.8 + 2.)*4 - key_h/2.
    for ix in range(6) : 
        for iy in range(4) : 
             x = dx + step_x*ix
             y = dy + step_y*iy
             pos = "C"
             if ix == 0 : pos = "L"
             if ix == 5 : pos = "R"
             panelised_rectangle(center=(x, y), width=key_w, height=key_h, radius=1., position = pos)
             circle((x, y), 1.5)
             place_pin(x, y + 3.1, n)
             n += 1
             place_pin(x, y - 3.1, n)
             n += 1
             circle( (x - key_w/2. - 0.3, y + 0.6), 0.3)
             circle( (x - key_w/2. - 0.3, y - 0.6), 0.3)
             circle( (x + key_w/2. + 0.3, y + 0.6), 0.3)
             circle( (x + key_w/2. + 0.3, y - 0.6), 0.3)

large_keys()
small_keys()

pcbnew.Refresh()
