import os
import shutil
import subprocess
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Arc, Rectangle
import pcbnew

import os, sys
sys.path.append("../python/")

from geometry import large_keys_coord, small_keys_coord, large_key_w, large_key_h, small_key_w, small_key_h
from primitives import rounded_rectangle, panelised_rectangle, circle, filled_rectangle

w = 10.
h = 6. 
min_r = 1.
silk_dist = 0.5

def add_latex(board, x, y, text, size = 7, inverted = False, rotation = "horizontal") : 

  svg_raw = "latex_raw.svg"
  bmp_raw = "latex_raw.bmp"
  png_raw = "latex_raw.png"
  svg_clean = "latex_clean.svg"
  footprint_name = "latex_text"
  output_path = f"{footprint_name}.kicad_mod"
  pretty_dir = f"{footprint_name}.pretty"
  mod_path = os.path.join(pretty_dir, f"{footprint_name}.kicad_mod")

  # Render LaTeX to SVG
  fig, ax = plt.subplots(figsize=(1, 1), dpi=300)
  ax.axis('off')
  ax.set_frame_on(False)
  ax.set_xlim(-0.5*25.4, 0.5*25.4)
  ax.set_ylim(-0.5*25.4, 0.5*25.4)

  if inverted : 
    if rotation == "vertical" : 
      rect = FancyBboxPatch(( -h/2. + silk_dist, -w/2. + silk_dist),
                             width = h - 2*silk_dist, height = w - 2*silk_dist,
                             linewidth=0.5, edgecolor = "black", facecolor = "black", 
                             boxstyle="round,pad=1")
    else : 
      rect = FancyBboxPatch(( -w/2. + silk_dist, -h/2. + silk_dist),
                             width = w - 2*silk_dist, height = h - 2*silk_dist,
                             linewidth=0.5, edgecolor = "black", facecolor = "black", 
                             boxstyle="round,pad=1")
    ax.add_patch(rect)
    ax.text(0., 0., text, fontsize=size, ha='center', va='center', color = "white", rotation = rotation)
  else : 
    ax.text(0., 0., text, fontsize=size, ha='center', va='center', color = "black", rotation = rotation)
  plt.gcf().patch.set_visible(False)
  plt.savefig(png_raw, bbox_inches='tight', transparent=True, edgecolor = "white", format='png', pad_inches=0, dpi=1200)
  plt.close()

  subprocess.run(["convert", png_raw, bmp_raw], check=True)

  subprocess.run([
    "potrace", bmp_raw,
    "-b", "svg",  
    "--flat", 
    "-a 0.5", 
#    "-O 0.1", 
    "-r", "1200"
  ], check=True)

  # Convert SVG to footprint using svg2mod
  cmd = [
    "svg2mod",
    "-i", svg_raw,
    "-o", output_path,
    "--name", footprint_name,
    "--force", "F.SilkS",
    "-p", "1.0",
    "--center"
  ]
  subprocess.run(cmd, check=True)

  # Make .pretty dir and move the .kicad_mod file
  os.makedirs(pretty_dir, exist_ok=True)
  shutil.move(output_path, mod_path)

  footprint = pcbnew.FootprintLoad(pretty_dir, footprint_name)
  footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
  board.Add(footprint)

normal = False
inverted = True

func_style = normal
shift_style = inverted
mode_style = inverted
memory_style = normal
input_style = normal
op_style = normal
c_style = inverted
stack_style = normal

small_keys = [

    (r"DEL", 8, normal, "CLEAR", 5, normal), 
    (r"$\Leftarrow$", 8, normal, "DROP", 5, normal), 
    (r"$+/-$", 8, normal, "EDIT $CMD$", 5, normal), 
    (r"EEX", 8, normal, "PURG $ARG$", 5, normal), 
    (r"ENTER$\uparrow$", 8, normal, "EQN $MATRIX$", 5, normal), 

    (r"$\sin$", 8, normal, r"asin  $\partial$", 5, normal), 
    (r"$\cos$", 8, normal, r"acos  $\int$", 5, normal), 
    (r"$\tan$", 8, normal, r"atan  $\sum$", 5, normal), 
    (r"$\sqrt{x}$", 8, normal, r"$x^2$  $\sqrt[x]{y}$", 6, normal), 
    (r"$y^x$", 8, normal,  r"$10^{x}$ $\log$", 6, normal), 
    (r"$1/x$", 8, normal,  r"$e^{x}$  $\ln$", 6, normal), 

    (r"$'$", 8, normal, r"UP $HOME$", 5, normal), 
    (r"STO", 8, normal, r"DEF $RCL$", 5, normal), 
    (r"EVAL", 7, normal, r"$\to$NUM $UNDO$", 5, normal), 
    (r"$\triangleleft$", 8, normal, r"PICTURE", 5, normal), 
    (r"$\bigtriangledown$", 8, normal, r"VIEW", 5, normal), 
    (r"$\triangleright$", 8, normal, r"SWAP", 5, normal), 

    (r"MTH", 8, normal, r"RAD $POLAR$", 5, normal), 
    (r"PRG", 8, normal, r"$CHARS$", 5, normal), 
    (r"CST", 8, normal, r"$MODES$", 5, normal), 
    (r"VAR", 8, normal, r"$MEMORY$", 5, normal), 
    (r"$\bigtriangleup$", 8, normal, r"$STACK$", 5, normal), 
    (r"NXT", 8, normal, r"PREV $MENU$", 5, normal), 

    (r"F1", 8, normal), 
    (r"F2", 8, normal), 
    (r"F3", 8, normal), 
    (r"F4", 8, normal), 
    (r"F5", 8, normal), 
    (r"F6", 8, normal), 
]

large_keys = [
    (r"ON", 12, normal, r"CONT $OFF$", 6, normal), 
    (r"0", 12, normal, r"$=$   $\rightarrow$", 6, normal), 
    (r".", 12, normal, r",   $\leftarrow$", 6, normal), 
    (r"SPC", 11, normal, r"$\pi$   $\measuredangle$", 6, normal), 
    (r"$+$", 12, normal, r"{ }   $: :$", 6, normal), 

    (r"$\Rsh$", 12, inverted), 
    (r"1", 12, normal, r"$I/O$", 6, normal), 
    (r"2", 12, normal, r"$LIBRARY$", 6, normal), 
    (r"3", 12, normal, r"$EQ\;LIB$", 6, normal), 
    (r"$-$", 12, normal, r'$\ll \gg$   " "', 6, normal), 

    (r"$\Lsh$", 12, inverted), 
    (r"4", 12, normal, r"$TIME$", 6, normal), 
    (r"5", 12, normal, r"$STAT$", 6, normal), 
    (r"6", 12, normal, r"$UNITS$", 6, normal), 
    (r"$\times$", 12, normal, r"$[\;]$   __", 6, normal), 

    (r"$\alpha$", 12, normal, r"USER $ENTRY$", 5, normal), 
    (r"7", 12, normal, r"$SOLVE$", 6, normal), 
    (r"8", 12, normal, r"$PLOT$", 6, normal), 
    (r"9", 12, normal, r"$SYMBOLIC$", 6, normal), 
    (r"$\div$", 12, normal, r"$(\;)$   #", 6, normal), 
]

alpha = {
  23 : "A", 
  24 : "B", 
  25 : "C", 
  26 : "D", 
  27 : "E", 
  28 : "F", 

  17 : "G", 
  18 : "H", 
  19 : "I", 
  20 : "J", 
  21 : "K", 
  22 : "L", 

  11 : "M", 
  12 : "N", 
  13 : "O", 
  14 : "P", 
  15 : "Q", 
  16 : "R", 

   5 : "S", 
   6 : "T", 
   7 : "U", 
   8 : "V", 
   9 : "W", 
  10 : "X", 

   2 : "Y", 
   3 : "Z", 
}

board = pcbnew.LoadBoard("FrontPanel/FrontPanel.kicad_pcb")

for n,(x,y) in enumerate(large_keys_coord) : 
  key = large_keys[n]
  text = key[0]
  size = key[1]
  inverted = key[2]
  #add_latex(board, x, y, text, size, False)
  if len(key)>4 : 
    text_shift = key[3]
    size_shift = key[4]
    add_latex(board, x, y-5.0, text_shift, size_shift)

for n,(x,y) in enumerate(small_keys_coord) : 
  key = small_keys[n]
  text = key[0]
  size = key[1]
  inverted = key[2]
  #add_latex(board, x, y, text, size, False)
  if len(key)>4 : 
    text_shift = key[3]
    size_shift = key[4]
    add_latex(board, x, y-4.1, text_shift, size_shift)

for n,(x,y) in enumerate(small_keys_coord) : 
  if n in alpha : 
    text = pcbnew.PCB_TEXT(board)
    text.SetText(alpha[n])
    text.SetLayer(pcbnew.F_SilkS)
    text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x+5.), pcbnew.FromMM(y+1.5)))
    text.SetTextHeight(pcbnew.FromMM(1.5))
    text.SetTextWidth(pcbnew.FromMM(1.2))
    text.SetTextThickness(pcbnew.FromMM(0.22))
    board.Add(text)

board.Save("FrontPanel/FrontPanel_labelled_hp48.kicad_pcb")

board = pcbnew.LoadBoard("KeyTops/KeyTops.kicad_pcb")

key_w = large_key_w
key_h = large_key_h
for n,(x,y) in enumerate(large_keys_coord) : 
    rounded_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1.)
    key = large_keys[n]
    text = key[0]
    size = key[1]
    inverted = key[2]
    add_latex(board, x, y, text, size, inverted)

key_w = small_key_w
key_h = small_key_h
for n,(x,y) in enumerate(small_keys_coord) : 
    if n == 4 : 
        rounded_rectangle(board, center=(x, y), width=18.2, height=key_h, radius=1.)
    else : 
        rounded_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1.)
    key = small_keys[n]
    text = key[0]
    size = key[1]
    inverted = key[2]
    add_latex(board, x, y, text, size, inverted)

board.Save("KeyTops/KeyTops_labelled_hp48.kicad_pcb")

board = pcbnew.LoadBoard("KeyTops/KeyTops_empty.kicad_pcb")

zones = []

key_w = large_key_w
key_h = large_key_h
n = 0
for iy in range(4) : 
  for ix in range(5) : 
    x = (large_key_h+2.)*ix + 43.4
    y = (large_key_w+2.)*iy + 45.0
    #panelised_rectangle(board, center=(x, y), width=key_h, height=key_w, radius=1.)
    key = large_keys[n]
    text = key[0]
    size = key[1]
    inverted = key[2]
    add_latex(board, x, y, text, size, inverted, rotation = "vertical")
    #circle(board,  (x - key_h/2. - 0.3, y + 0.6), 0.3)
    #circle(board,  (x - key_h/2. - 0.3, y - 0.6), 0.3)
    #circle(board,  (x + key_h/2. + 0.3, y + 0.6), 0.3)
    #circle(board,  (x + key_h/2. + 0.3, y - 0.6), 0.3)
    #zones += [ filled_rectangle(board, center=(x, y), width = 3., height = 8.) ]
    #zones += [ filled_rectangle(board, center=(x, y), width = 3.1, height = 8.1, layer = pcbnew.B_Mask) ]
    n += 1

key_w = small_key_w
key_h = small_key_h
n = 0
for iy in range(5) : 
  for ix in range(6) : 
    if ix == 5 and iy == 0 : continue
    key = small_keys[n]
    text = key[0]
    size = key[1]
    inverted = key[2]
    x = (small_key_h+2.)*ix + 42.5
    y = (small_key_w+2.)*iy + 92.4
    if n == 4 : 
        x += 20. 
        #panelised_rectangle(board, center=(x, y), width=key_h, height=18.2, radius=1.)
        x -= 20.
    #else : 
        #panelised_rectangle(board, center=(x, y), width=key_h, height=key_w, radius=1.)
    if n == 4 : 
      add_latex(board, x + (small_key_h+2), y + (small_key_w+2.)/2., text, size, inverted, rotation = "vertical")
    elif n == 10 : 
      add_latex(board, x - (small_key_h+2), y - (small_key_w+2), text, size, inverted, rotation = "vertical")
    else : 
      add_latex(board, x, y, text, size, inverted, rotation = "vertical")
    #circle(board,  (x - key_h/2. - 0.3, y + 0.6), 0.3)
    #circle(board,  (x - key_h/2. - 0.3, y - 0.6), 0.3)
    #circle(board,  (x + key_h/2. + 0.3, y + 0.6), 0.3)
    #circle(board,  (x + key_h/2. + 0.3, y - 0.6), 0.3)
    #zones += [ filled_rectangle(board, center=(x, y), width = 3., height = 7.) ]
    #zones += [ filled_rectangle(board, center=(x, y), width = 3.1, height = 7.1, layer = pcbnew.B_Mask) ]
    n += 1

#filler = pcbnew.ZONE_FILLER(board)
#filler.Fill(zones)

board.Save("KeyTops/KeyTops_production_hp48.kicad_pcb")
