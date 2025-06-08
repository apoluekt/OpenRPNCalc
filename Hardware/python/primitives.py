import pcbnew
import math
import os

KICAD_VERSION = pcbnew.Version().split(".")[0]
fp_path = os.getenv("KICAD" + KICAD_VERSION + "_FOOTPRINT_DIR", default=None)

def rounded_rectangle(board, center, width, height, radius, layer=pcbnew.Edge_Cuts):
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

def milled_rectangle(board, center, width, height, radius, layer=pcbnew.Edge_Cuts):
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

def circle(board, center, radius, layer=pcbnew.Edge_Cuts) : 
    circ = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_CIRCLE)
    circ.SetCenter(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1])))
    circ.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1]+radius)))
    circ.SetLayer(pcbnew.Edge_Cuts)
    board.Add(circ)

def line(board, x1, y1, x2, y2, layer=pcbnew.Edge_Cuts) : 
    start = (pcbnew.FromMM(x1), pcbnew.FromMM(y1))
    end = (pcbnew.FromMM(x2), pcbnew.FromMM(y2))
    line = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
    line.SetStart(pcbnew.VECTOR2I(*start))
    line.SetEnd(pcbnew.VECTOR2I(*end))
    line.SetLayer(layer)
    board.Add(line)

def arc(board, center, radius, start_angle, end_angle, layer = pcbnew.Edge_Cuts) : 
    arc = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_ARC)
    arc.SetCenter(pcbnew.VECTOR2I(pcbnew.FromMM(center[0]), pcbnew.FromMM(center[1])))

    # Compute start point for the arc
    start_x = pcbnew.FromMM(center[0] + radius * math.cos(math.radians(start_angle)))
    start_y = pcbnew.FromMM(center[1] - radius * math.sin(math.radians(start_angle)))
    arc.SetStart(pcbnew.VECTOR2I(int(start_x), int(start_y)))

    # Set the angle span using `EDA_ANGLE`
    arc.SetArcAngleAndEnd(pcbnew.EDA_ANGLE((end_angle - start_angle), pcbnew.DEGREES_T))
    arc.SetLayer(layer)
    board.Add(arc)

def panelised_rectangle(board, center, width, height, radius, bridge = 3., position = "C"):
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

def place_pin(board, x, y, n) : 
    PIN_LIB = "Connector_Wire.pretty"
    PIN_NAME = "SolderWire-0.5sqmm_1x01_D0.9mm_OD2.1mm"
    pin_fp = pcbnew.FootprintLoad(fp_path + PIN_LIB, PIN_NAME)
    pin_fp.SetReference(f"P{n+1}a")
    pin_fp.SetValue("")
    pin_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    pin_fp.Reference().SetVisible(False)
    board.Add(pin_fp)

def filled_rectangle(board, center, width, height, layer=pcbnew.B_Cu):
    """
    Adds a filled copper rectangle (zone) to the specified layer.

    :param board: The PCB board object
    :param pos: Tuple (x, y) of the bottom-left corner in millimeters
    :param width: Width of the rectangle in millimeters
    :param height: Height of the rectangle in millimeters
    :param layer: The PCB layer to draw on (default is F.Cu)
    """
    def to_nm(value):
        return pcbnew.FromMM(value)

    pos = (center[0] - width/2., center[1] - height/2.)

    # Create a zone container
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    #zone.SetNetCode(0)  # Set to an actual net number if needed
    #zone.SetClearance(to_nm(0.2))  # Example clearance

    # Define the 4 corners of the rectangle
    corners = [
        pcbnew.VECTOR2I(to_nm(pos[0]), to_nm(pos[1])),
        pcbnew.VECTOR2I(to_nm(pos[0] + width), to_nm(pos[1])),
        pcbnew.VECTOR2I(to_nm(pos[0] + width), to_nm(pos[1] + height)),
        pcbnew.VECTOR2I(to_nm(pos[0]), to_nm(pos[1] + height)),
    ]

    # Create an outline for the zone
    outline = zone.Outline()
    outline.NewOutline()
    for corner in corners:
        outline.Append(corner)

    # Close the polygon
    outline.Append(corners[0])

    # Add zone to the board
    board.Add(zone)
    return zone

