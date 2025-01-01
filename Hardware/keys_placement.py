# Keyboard switch placement script for KiCAD. 
# To run, open "Tools/Scripting console" and run 
#    exec(open("/home/poluekt/cernbox/devel/OpenRPNCalc_rev2/PCB/keys_placement.py").read())

import pcbnew
import os

KICAD_VERSION = pcbnew.Version().split(".")[0]
fp_path = os.getenv("KICAD" + KICAD_VERSION + "_FOOTPRINT_DIR", default=None)

KEYS_WIDTH = 90.
KEYS_HEIGHT = 112.
CENTER_X = 50 + KEYS_WIDTH/2.
CENTER_Y = 50 + KEYS_HEIGHT/2.

BOTTOM_Y = CENTER_Y + KEYS_HEIGHT/2.

GRID_SPACING_LARGE_X = pcbnew.FromMM(11.8+2.)  # Grid spacing in mm
GRID_SPACING_LARGE_Y = pcbnew.FromMM(9.5+2.)  # Grid spacing in mm
START_POSITION_LARGE = (pcbnew.FromMM(CENTER_X - (11.8+2.)*2.), pcbnew.FromMM(BOTTOM_Y - 14.))  # Starting position (x, y) in mm

GRID_SPACING_SMALL_X = pcbnew.FromMM(9.7+2.)  # Grid spacing in mm
GRID_SPACING_SMALL_Y = pcbnew.FromMM(8.7+2.)  # Grid spacing in mm
START_POSITION_SMALL = (pcbnew.FromMM(CENTER_X - (9.7+2.)*2.5), pcbnew.FromMM(BOTTOM_Y - 67.))  # Starting position (x, y) in mm

PIN_LIB = "Connector_Wire.pretty"
PIN_NAME = "SolderWire-0.5sqmm_1x01_D0.9mm_OD2.1mm"
PIN_DX1 = pcbnew.FromMM(-2.3)
PIN_DX2 = pcbnew.FromMM( 2.3)
PIN_DY = pcbnew.FromMM(-1.0)

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

    x += GRID_SPACING_SMALL_X
    n += 1
  x = x_start
  y -= GRID_SPACING_SMALL_Y

# Refresh the PCB view
pcbnew.Refresh()
