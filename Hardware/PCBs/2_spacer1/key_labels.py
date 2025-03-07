import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from matplotlib.patches import FancyBboxPatch, Polygon, Arc, Rectangle
import numpy as np
import os

normal = ("white", "black")
inverted = ("black","white")

line_color = "black"

func_style = normal
shift_style = inverted
mode_style = inverted
memory_style = normal
input_style = normal
op_style = normal
c_style = inverted
stack_style = normal

keys_silk_name = "keys_silk"

small_keys = [
  [
    (r"$\sqrt{x}$", 9, func_style, r"$x^{2}$", 6, shift_style), 
    (r"$1/x$", 9, func_style), 
    (r"erf", 9, func_style, r"erf${}^{-1}$", 6, shift_style), 
    (r"R$\rightarrow$P", 7, func_style, r"P$\rightarrow$R", 6, shift_style), 
    (r"$\Gamma(x)$", 8, func_style,  r"$\ln\Gamma(x)$", 6, shift_style), 
    (r"$C_{y}^{x}$", 8, func_style,  r"$P_{y}^{x}$", 6, shift_style), 
  ], 
  [
    (r"$y^x$", 9, func_style, r"$\sqrt[x]{y}$", 6, shift_style), 
    (r"$\ln$", 9, func_style, r"$e^{x}$", 6, shift_style), 
    (r"$\lg$", 9, func_style, r"$10^{x}$", 6, shift_style), 
    (r"$\sin$", 9, func_style, r"$\sin^{-1}$", 6, shift_style), 
    (r"$\cos$", 9, func_style, r"$\cos^{-1}$", 6, shift_style), 
    (r"$\tan$", 9, func_style, r"$\tan^{-1}$", 6, shift_style), 
  ], 
  [
    (r"Drop", 7, stack_style, r"Rot$\uparrow$", 6, shift_style), 
    (r"X$\leftrightarrow$Y", 7, stack_style, r"LAST$x$", 6, shift_style), 
    ("DR", 9, mode_style, r"D$\leftrightarrow$R", 6, shift_style), 
    ("M$+$", 9, memory_style, r"M$-$", 6, shift_style), 
    ("MR", 9, memory_style), 
    ("MS", 9, memory_style), 
  ], 
  [
    ("F", 10, shift_style), 
    ("G", 10, shift_style), 
    ("MOD", 8, mode_style), 
    ("UNC", 8, mode_style), 
    ("PRC", 8, mode_style), 
    ("On", 10, c_style, r"Off", 6, shift_style), 
  ], 
]

large_keys = [
  [ 
    ("0", 11, input_style), 
    ("/$-$/", 10, input_style), 
    (".", 11, input_style), 
    ("$\pm$", 11, input_style), 
    ("Enter", 7, stack_style), 
  ], 
  [ 
    ("1", 11, input_style, r"$\pi$", 7, shift_style), 
    ("2", 11, input_style), 
    ("3", 11, input_style), 
    ("$+$", 11, op_style, r"$N\sigma(x)$", 7, shift_style), 
    ("$-$", 11, op_style, r"$N\sigma(x-y)$", 7, shift_style), 
  ], 
  [ 
    ("4", 11, input_style, r"Pois$(\!k_{x}|\lambda_{y}\!)$", 6, shift_style), 
    ("5", 11, input_style, r"$p(\chi^2(y)\!\!>\!\!x)$", 6, shift_style), 
    ("6", 11, input_style), 
    (r"$\times$", 11, op_style), 
    ("$\div$", 11, op_style), 
  ], 
  [ 
    ("7", 11, input_style, r"$\eta(\theta)$", 7, shift_style), 
    ("8", 11, input_style, r"$\gamma(\beta)$", 7, shift_style), 
    ("9", 11, input_style, r"$p(z\to xy)$", 7, shift_style), 
    ("Exp", 10, input_style), 
    ("C", 11, c_style, r"CST", 6, shift_style), 
  ], 
]

face_w = 73.
face_h = 134.4

min_r = 1.
outline_w = 0.1
silk_dist = 0.5

def create_fig(w, h) : 
  fig, ax = plt.subplots(figsize = (w/25.4, h/25.4), frameon = False)
  fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
  ax.set_xlim(0., w)
  ax.set_ylim(0., h)
  ax.set_axis_off()
  return fig, ax

fig_keys_silk, ax_keys_silk = create_fig(face_w, face_h)

plt.rc('text', usetex=False)
plt.rc('font', weight='bold')

def draw_key(dx, dy, ix, iy, w, h, k, step_x, step_y) : 
  """
    Draw key, top/bottom part
      - With silkscreen if part = top
      - With mounting holes if part = bottom
  """
  x = dx + step_x*ix
  y = dy + step_y*iy

  if k[2][0] == "black" : 
      rect2 = FancyBboxPatch((x-w/2. + min_r + silk_dist, y-h/2. + min_r + silk_dist),
                             width = w - 2*min_r - 2*silk_dist, height = h - 2*min_r - 2*silk_dist,
                             linewidth=0.5, edgecolor = line_color, facecolor = k[2][0], 
                             boxstyle="round,pad=1"
                         )
      ax_keys_silk.add_patch(rect2)

  ax_keys_silk.text(x + 0.3, y + 0.3, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[2][1], rotation = 90.)

def draw_large_key(ix, iy, k) : 
  key_h = 11.1 - 0.4
  key_w = 7. - 0.4
  rad = 1.
  step_x = key_w + 2*rad
  step_y = key_h + 2*rad
  dx = key_w/2. + 6. + 2.
  dy = 5.5 + 2. + key_h/2.

  draw_key(dx, dy, ix, iy, key_w, key_h, k, step_x, step_y)

def draw_small_key(ix, iy, k) : 
  key_h = 9.2 - 0.4
  key_w = 6.2 - 0.4
  rad = 1.
  step_x = key_w + 2*rad
  step_y = key_h + 2*rad
  dx = key_w/2. + 6. + 2.
  dy = 5.5 + 2. + (11.1 - 0.4 + 2.)*4 + key_h/2.
  draw_key(dx, dy, ix, iy, key_w, key_h, k, step_x, step_y)

def draw_large_keys(keys) : 
  for iy, row in enumerate(keys) : 
    for ix, k in enumerate(row) : 
      draw_large_key(ix, iy, k)

def draw_small_keys(keys) : 
  for iy, row in enumerate(keys) : 
    for ix, k in enumerate(row) : 
      draw_small_key(ix, iy, k)

draw_large_keys(large_keys)
draw_small_keys(small_keys)

fig_keys_silk.savefig(f"{keys_silk_name}.pdf")
fig_keys_silk.savefig(f"{keys_silk_name}.svg")
fig_keys_silk.savefig(f"{keys_silk_name}.png", dpi = 300)

plt.show()
