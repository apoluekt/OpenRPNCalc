# Run with
# exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc_front_panel/front_panel.py").read())

import pcbnew
import math

pcb_width = 73.0
pcb_height = 134.4

center_x = 100
center_y = 97.2

lcd_width = 63.+0.2
lcd_height = 43.+0.2

# Load the current board and apply the script
board = pcbnew.GetBoard()

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

def milled_rectangle(center, width, height, radius, layer=pcbnew.Edge_Cuts):
    """
    Draws a milled rectangle on the specified layer using lines and arcs.
    
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
    r2 = to_nm(radius/math.sqrt(2.))

    # Corner arc centers
    corners = {
        "TL": (cx - w2 + r2, cy - h2 + r2),
        "TR": (cx + w2 - r2, cy - h2 + r2),
        "BR": (cx + w2 - r2, cy + h2 - r2),
        "BL": (cx - w2 + r2, cy + h2 - r2),
    }

    # Define the straight-line segments
    lines = [
        ((corners["TL"][0] + r2, corners["TL"][1] - r2), (corners["TR"][0] - r2, corners["TR"][1] - r2)),  # Top
        ((corners["TR"][0] + r2, corners["TR"][1] + r2), (corners["BR"][0] + r2, corners["BR"][1] - r2)),  # Right
        ((corners["BR"][0] - r2, corners["BR"][1] + r2), (corners["BL"][0] + r2, corners["BL"][1] + r2)),  # Bottom
        ((corners["BL"][0] - r2, corners["BL"][1] - r2), (corners["TL"][0] - r2, corners["TL"][1] + r2)),  # Left
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
        (corners["TL"], 225, 405), # Top Left
        (corners["BR"], 45, 225),  # Bottom Right
        (corners["TR"], 135, 315), # Bottom Left
        (corners["BL"], -45, 135), # Top Right
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

def large_keys() : 
    step_x = 12.3
    step_y = 10.
    key_w = 11.1
    key_h = 7.
    dx = center_x
    dy = center_y + pcb_height/2. - step_y*3 - 9.
    for ix in range(5) : 
        for iy in range(4) : 
             x = dx + step_x*(ix - 2)
             y = dy + step_y*iy
             rounded_rectangle(center=(x, y), width=key_w, height=key_h, radius=1.)

def small_keys() : 
    step_x = 10.2
    step_y = 9.2
    key_w = 9.2
    key_h = 6.2
    dx = center_x
    dy = center_y + pcb_height/2. - step_y*3 - 49.
    for ix in range(6) : 
        for iy in range(4) : 
             x = dx + step_x*(ix - 2.5)
             y = dy + step_y*iy
             rounded_rectangle(center=(x, y), width=key_w, height=key_h, radius=1.)

outline()
milled_rectangle(center=(center_x, center_y - pcb_height/2. + 6 + lcd_height/2.), width=lcd_width, height=lcd_height, radius=1.)
large_keys()
small_keys()
pcbnew.Refresh()

