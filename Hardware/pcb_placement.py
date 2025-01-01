# Keyboard switch placement script for KiCAD. 
# To run, open "Tools/Scripting console" and run 
#    exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc_rev2/PCB/pcb_placement.py").read())

import pcbnew
import os

KICAD_VERSION = pcbnew.Version().split(".")[0]
fp_path = os.getenv("KICAD" + KICAD_VERSION + "_FOOTPRINT_DIR", default=None)

# Parameters
FOOTPRINT_REF_LARGE = [f"SW{i+1}" for i in range(20)]
FOOTPRINT_REF_SMALL = [f"SW{i+21}" for i in range(24)]

CENTER_X = 94.615
CENTER_Y = 95.5
PCB_WIDTH = 71.
PCB_HEIGHT = 139. 

CORNER_RAD = 2.
MOUNTING_HOLE_RAD = 1.6
MOUNTING_HOLE_DIST = 2.5

BOTTOM_Y = CENTER_Y + PCB_HEIGHT/2.

GRID_SPACING_LARGE_X = pcbnew.FromMM(12.3)  # Grid spacing in mm
GRID_SPACING_LARGE_Y = pcbnew.FromMM(10.0)  # Grid spacing in mm
START_POSITION_LARGE = (pcbnew.FromMM(CENTER_X - 12.3*2.), pcbnew.FromMM(BOTTOM_Y - 11.5))  # Starting position (x, y) in mm

GRID_SPACING_SMALL_X = pcbnew.FromMM(10.2)  # Grid spacing in mm
GRID_SPACING_SMALL_Y = pcbnew.FromMM(9.2)  # Grid spacing in mm
START_POSITION_SMALL = (pcbnew.FromMM(CENTER_X - 10.2*2.5), pcbnew.FromMM(BOTTOM_Y - 51.5))  # Starting position (x, y) in mm

PIN_LIB = "Connector_PinHeader_2.54mm.pretty"
PIN_NAME = "PinHeader_1x01_P2.54mm_Vertical"
PIN_DX1 = pcbnew.FromMM(-3.5)
PIN_DX2 = pcbnew.FromMM( 3.5)
PIN_DY = pcbnew.FromMM( 4.6)

# Get the current board
db = pcbnew.GetBoard()

for footprint in db.GetFootprints():
    print(f"Footprint Reference: {footprint.GetReference()}, Name: {footprint.GetFPID().GetLibItemName()}")

x_start, y_start = START_POSITION_LARGE
x = x_start
y = y_start
n = 0
for j in range(4):
  for i in range(5):
    footprint = db.FindFootprintByReference(FOOTPRINT_REF_LARGE[n])
    footprint.SetPosition(pcbnew.VECTOR2I(x, y))

    pina_fp = pcbnew.FootprintLoad(fp_path + PIN_LIB, PIN_NAME)
    pina_fp.SetReference(f"P{n+1}a")
    pina_fp.SetValue("")
    pina_fp.SetPosition(pcbnew.VECTOR2I(x + PIN_DX1, y + PIN_DY))
    pina_fp.Reference().SetVisible(False)
    db.Add(pina_fp)

    pinb_fp = pcbnew.FootprintLoad(fp_path + PIN_LIB, PIN_NAME)
    pinb_fp.SetReference(f"P{n+1}b")
    pinb_fp.SetValue("")
    pinb_fp.SetPosition(pcbnew.VECTOR2I(x + PIN_DX2, y + PIN_DY))
    pinb_fp.Reference().SetVisible(False)
    db.Add(pinb_fp)

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
    footprint = db.FindFootprintByReference(FOOTPRINT_REF_SMALL[n])
    footprint.SetPosition(pcbnew.VECTOR2I(x, y))

    pina_fp = pcbnew.FootprintLoad(fp_path + PIN_LIB, PIN_NAME)
    pina_fp.SetReference(f"P{n+21}a")
    pina_fp.SetValue("")
    pina_fp.SetPosition(pcbnew.VECTOR2I(x + PIN_DX1, y + PIN_DY))
    pina_fp.Reference().SetVisible(False)
    db.Add(pina_fp)

    pinb_fp = pcbnew.FootprintLoad(fp_path + PIN_LIB, PIN_NAME)
    pinb_fp.SetReference(f"P{n+21}b")
    pinb_fp.SetValue("")
    pinb_fp.SetPosition(pcbnew.VECTOR2I(x + PIN_DX2, y + PIN_DY))
    pinb_fp.Reference().SetVisible(False)
    db.Add(pinb_fp)

    print(f"Placed {FOOTPRINT_REF_SMALL[n]} at {pcbnew.ToMM(x)} mm, {pcbnew.ToMM(y)} mm.")
    x += GRID_SPACING_SMALL_X
    n += 1
  x = x_start
  y -= GRID_SPACING_SMALL_Y

def rounded_rectangle(x1, y1, x2, y2, r) : 

  lines = [ 
    (x1+r, y1, x2-r, y1), 
    (x2, y1+r, x2, y2-r), 
    (x2-r, y2, x1+r, y2), 
    (x1, y2-r, x1, y1+r), 
  ]

  for l in lines : 
    if l[0] != l[2] or l[1] != l[3] : 
      line = pcbnew.PCB_SHAPE(db)
      line.SetShape(pcbnew.SHAPE_T_SEGMENT)
      line.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(l[0]), pcbnew.FromMM(l[1])))
      line.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(l[2]), pcbnew.FromMM(l[3])))
      line.SetLayer(pcbnew.Edge_Cuts)
      db.Add(line)

  arcs = [
    (x1+r, y1+r, x1, y1+r, x1+r, y1), 
    (x2-r, y1+r, x2-r, y1, x2, y1+r), 
    (x2-r, y2-r, x2, y2-r, x2-r, y2), 
    (x1+r, y2-r, x1+r, y2, x1, y2-r), 
  ]

  for a in arcs : 
    arc = pcbnew.PCB_SHAPE(db)
    arc.SetShape(pcbnew.SHAPE_T_ARC)
    arc.SetCenter(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]), pcbnew.FromMM(a[1])))
    arc.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[2]), pcbnew.FromMM(a[3])))
    arc.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(a[4]), pcbnew.FromMM(a[5])))
    arc.SetLayer(pcbnew.Edge_Cuts)
    db.Add(arc)

rounded_rectangle(CENTER_X-PCB_WIDTH/2., CENTER_Y-PCB_HEIGHT/2., CENTER_X+PCB_WIDTH/2., CENTER_Y+PCB_HEIGHT/2., CORNER_RAD)
rounded_rectangle(CENTER_X-7., CENTER_Y-PCB_HEIGHT/2.+4., CENTER_X+7., CENTER_Y-PCB_HEIGHT/2+7., 1.5)

circles = [
  (CENTER_X-PCB_WIDTH/2.+MOUNTING_HOLE_DIST, CENTER_Y-PCB_HEIGHT/2.+MOUNTING_HOLE_DIST, MOUNTING_HOLE_RAD), 
  (CENTER_X-PCB_WIDTH/2.+MOUNTING_HOLE_DIST, CENTER_Y+PCB_HEIGHT/2.-MOUNTING_HOLE_DIST, MOUNTING_HOLE_RAD), 
  (CENTER_X+PCB_WIDTH/2.-MOUNTING_HOLE_DIST, CENTER_Y-PCB_HEIGHT/2.+MOUNTING_HOLE_DIST, MOUNTING_HOLE_RAD), 
  (CENTER_X+PCB_WIDTH/2.-MOUNTING_HOLE_DIST, CENTER_Y+PCB_HEIGHT/2.-MOUNTING_HOLE_DIST, MOUNTING_HOLE_RAD), 
  (CENTER_X+PCB_WIDTH/2.-MOUNTING_HOLE_DIST, CENTER_Y, MOUNTING_HOLE_RAD), 
  (CENTER_X-PCB_WIDTH/2.+MOUNTING_HOLE_DIST, CENTER_Y, MOUNTING_HOLE_RAD), 
]

for c in circles : 
  circ = pcbnew.PCB_SHAPE(db)
  circ.SetShape(pcbnew.SHAPE_T_CIRCLE)
  circ.SetCenter(pcbnew.VECTOR2I(pcbnew.FromMM(c[0]), pcbnew.FromMM(c[1])))
  circ.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(c[0]), pcbnew.FromMM(c[1]+c[2])))
  circ.SetLayer(pcbnew.Edge_Cuts)
  db.Add(circ)

# Refresh the PCB view
pcbnew.Refresh()
