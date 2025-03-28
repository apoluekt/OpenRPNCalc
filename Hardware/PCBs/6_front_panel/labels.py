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

front_silk_name = "front_silk"

small_keys = [
  [
    (r"$\sqrt{x}$", 9, func_style, r"$x^{2}$", 6, shift_style), 
    (r"$1/x$", 9, func_style, r"$x!$", 6, shift_style), 
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
    ("MR", 9, memory_style, r"MR$x$", 6, shift_style), 
    ("MS", 9, memory_style, r"MS$x$", 6, shift_style), 
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
    ("/$-$/", 10, input_style, r"Prog", 6, shift_style), 
    (".", 11, input_style, r"Rewind", 6, shift_style), 
    ("$\pm$", 11, input_style, r"Step", 6, shift_style), 
    ("Enter", 7, stack_style, r"Run", 6, shift_style), 
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
    ("6", 11, input_style, r"$N\sigma(p)$", 6, shift_style), 
    (r"$\times$", 11, op_style, r"mean", 7, shift_style), 
    ("$\div$", 11, op_style, r"RMS", 7, shift_style), 
  ], 
  [ 
    ("7", 11, input_style, r"$\eta(\theta)$", 7, shift_style), 
    ("8", 11, input_style, r"$\gamma(\beta)$", 7, shift_style), 
    ("9", 11, input_style, r"$p(z\to xy)$", 7, shift_style), 
    ("Exp", 10, input_style, r"$\chi^2$", 6, shift_style), 
    ("C", 11, c_style, r"CST", 6, shift_style), 
  ], 
]

large_hole_w = 11.1
large_hole_h = 7.

small_hole_w = 9.2
small_hole_h = 6.2

front_w = 73.0
front_h = 134.4

silk_dist = 0.5

def create_fig(w, h) : 
  fig, ax = plt.subplots(figsize = (w/25.4, h/25.4), frameon = False)
  fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
  ax.set_xlim(0., w)
  ax.set_ylim(0., h)
  ax.set_axis_off()
  return fig, ax

fig_front_silk, ax_front_silk = create_fig(front_w, front_h)

plt.rc('text', usetex=False)
plt.rc('font', weight='bold')

def draw_key_front(dx, dy, ix, iy, w, h, k, step_x, step_y) : 
  """
    Draw key hole in keyboard frontplate
  """
  x = dx + step_x*ix
  y = dy + step_y*iy

  if len(k)>3 :
    ax_front_silk.text(x, y + h/2 + 1.5, k[3],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[4], color = "black")

def draw_large_key(ix, iy, k) : 
  step_x = 12.3
  step_y = 10

  dx = front_w/2-step_x*2
  dy = 9.
  draw_key_front(dx, dy, ix, iy, large_hole_w, large_hole_h, k, step_x, step_y)

def draw_small_key(ix, iy, k) : 
  step_x = 10.2
  step_y = 9.2

  dx = front_w/2-step_x*2.5
  dy = 49.
  draw_key_front(dx, dy, ix, iy, small_hole_w, small_hole_h, k, step_x, step_y)

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

fig_front_silk.savefig(f"{front_silk_name}.pdf")
#fig_front_silk.savefig(f"{front_silk_name}.svg")
fig_front_silk.savefig(f"{front_silk_name}.png", dpi = 300)

plt.show()
