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
    rect = FancyBboxPatch(( -w/2. + min_r + silk_dist, -h/2. + min_r + silk_dist),
                             width = w - 2*min_r - 2*silk_dist, height = h - 2*min_r - 2*silk_dist,
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

    (r"PROG", 7, mode_style, "Rewind", 6, mode_style), 
    (r"RUN", 8, mode_style, "Step", 6, mode_style), 
    (r"$\leftarrow$", 7, func_style), 
    (r"$\rightarrow$", 7, func_style), 
    (r"ENTER$\uparrow$", 8, stack_style), 

    (r"$\sqrt{x}$", 9, func_style, r"$x^{2}$", 6, shift_style), 
    (r"$1/x$", 9, func_style, r"$x!$", 6, shift_style), 
    (r"erf", 9, func_style, r"erf${}^{-1}$", 6, shift_style), 
    (r"R$\rightarrow$P", 7, func_style, r"P$\rightarrow$R", 6, shift_style), 
    (r"$\Gamma(x)$", 8, func_style,  r"$\ln\Gamma(x)$", 6, shift_style), 
    (r"$C_{y}^{x}$", 8, func_style,  r"$P_{y}^{x}$", 6, shift_style), 

    (r"$y^x$", 9, func_style, r"$\sqrt[x]{y}$", 6, shift_style), 
    (r"$\ln$", 9, func_style, r"$e^{x}$", 6, shift_style), 
    (r"$\lg$", 9, func_style, r"$10^{x}$", 6, shift_style), 
    (r"$\sin$", 9, func_style, r"$\sin^{-1}$", 6, shift_style), 
    (r"$\cos$", 9, func_style, r"$\cos^{-1}$", 6, shift_style), 
    (r"$\tan$", 9, func_style, r"$\tan^{-1}$", 6, shift_style), 

    (r"DROP", 7, stack_style, r"Rot$\uparrow$", 6, shift_style), 
    (r"X$\leftrightarrow$Y", 7, stack_style, r"LAST$x$", 6, shift_style), 
    ("DR", 9, mode_style, r"D$\leftrightarrow$R", 6, shift_style), 
    ("M$+$", 9, memory_style, r"M$-$", 6, shift_style), 
    ("MR", 9, memory_style, r"MR$x$", 6, shift_style), 
    ("MS", 9, memory_style, r"MS$x$", 6, shift_style), 

    ("F", 10, shift_style), 
    ("G", 10, shift_style), 
    ("MOD", 8, mode_style), 
    ("UNC", 8, mode_style), 
    ("PRC", 8, mode_style), 
    ("ON", 10, c_style, r"Off", 6, shift_style), 
]

large_keys = [
    ("0", 11, input_style), 
    ("/$-$/", 10, input_style), 
    (".", 11, input_style), 
    ("$\pm$", 11, input_style), 
    (r"$\alpha$", 11, input_style), 

    ("1", 11, input_style, r"$\pi$", 7, shift_style), 
    ("2", 11, input_style), 
    ("3", 11, input_style), 
    ("$+$", 11, op_style, r"$N\sigma(x)$", 7, shift_style), 
    ("$-$", 11, op_style, r"$N\sigma(x-y)$", 7, shift_style), 

    ("4", 11, input_style, r"Pois$(\!k_{x}|\lambda_{y}\!)$", 6, shift_style), 
    ("5", 11, input_style, r"$p(\chi^2(y)\!\!>\!\!x)$", 6, shift_style), 
    ("6", 11, input_style, r"$N\sigma(p)$", 6, shift_style), 
    (r"$\times$", 11, op_style, r"mean", 7, shift_style), 
    ("$\div$", 11, op_style, r"RMS", 7, shift_style), 

    ("7", 11, input_style, r"$\eta(\theta)$", 7, shift_style), 
    ("8", 11, input_style, r"$\gamma(\beta)$", 7, shift_style), 
    ("9", 11, input_style, r"$p(z\to xy)$", 7, shift_style), 
    ("EXP", 10, input_style, r"$\chi^2$", 6, shift_style), 
    ("C", 11, c_style, r"CST", 6, shift_style), 
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

   0 : "Y", 
   1 : "Z", 
   2 : "_", 
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
    add_latex(board, x, y-4.0, text_shift, size_shift)

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

board.Save("FrontPanel/FrontPanel_labelled.kicad_pcb")

board = pcbnew.LoadBoard("KeyTops/KeyTops.kicad_pcb")

key_w = large_key_w
key_h = large_key_h
for n,(x,y) in enumerate(large_keys_coord) : 
    rounded_rectangle(board, center=(x, y), width=key_w, height=key_h, radius=1.)
    key = large_keys[n]
    text = key[0]
    size = key[1]
    inverted = key[2]
    add_latex(board, x, y, text, size, False)

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
    add_latex(board, x, y, text, size, False)

board.Save("KeyTops/KeyTops_labelled.kicad_pcb")

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
    add_latex(board, x, y, text, size, False, rotation = "vertical")
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
    #else : 
        #panelised_rectangle(board, center=(x, y), width=key_h, height=key_w, radius=1.)
    add_latex(board, x, y, text, size, False, rotation = "vertical")
    #circle(board,  (x - key_h/2. - 0.3, y + 0.6), 0.3)
    #circle(board,  (x - key_h/2. - 0.3, y - 0.6), 0.3)
    #circle(board,  (x + key_h/2. + 0.3, y + 0.6), 0.3)
    #circle(board,  (x + key_h/2. + 0.3, y - 0.6), 0.3)
    #zones += [ filled_rectangle(board, center=(x, y), width = 3., height = 7.) ]
    #zones += [ filled_rectangle(board, center=(x, y), width = 3.1, height = 7.1, layer = pcbnew.B_Mask) ]
    n += 1

#filler = pcbnew.ZONE_FILLER(board)
#filler.Fill(zones)

board.Save("KeyTops/KeyTops_production.kicad_pcb")
