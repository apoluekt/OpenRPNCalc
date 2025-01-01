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

face_edge_name = "face_edge"
face_silk_name = "face_silk"
keys_edge_name = "keys_edge"
keys_fcop_name = "keys_fcop"
keys_bcop_name = "keys_bcop"
keys_silk_name = "keys_silk"
keys_bottom_edge_name = "keys_bottom_edge"

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

large_hole_w = 11.1
large_hole_h = 7.
large_key_w = large_hole_w-0.4
large_key_h = large_hole_h-0.4
large_key_bottom_w = 11.8
large_key_bottom_h = 9.5

small_hole_w = 9.2
small_hole_h = 6.2
small_key_w = small_hole_w-0.4
small_key_h = small_hole_h-0.4
small_key_bottom_w = 9.7
small_key_bottom_h = 8.7

face_w = 71.
face_h = 139.
mounting_hole_dist = 2.5
mounting_hole_rad = 1.6

keys_w = 90. 
keys_h = 112.

disp_w = 60.2
disp_h = 37.2
disp_y = 90.
disp_w_inner = 64.
disp_h_inner = 44.
disp_y_inner = 86.

min_r = 1.
outline_w = 0.1
bridge_w = 3.
panel_d = 3.
copper_dist = 1.
silk_dist = 0.5

def create_fig(w, h) : 
  fig, ax = plt.subplots(figsize = (w/25.4, h/25.4), frameon = False)
  fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
  ax.set_xlim(0., w)
  ax.set_ylim(0., h)
  ax.set_axis_off()
  return fig, ax

fig_face_edge, ax_face_edge = create_fig(face_w, face_h)
fig_face_silk, ax_face_silk = create_fig(face_w, face_h)
fig_keys_edge, ax_keys_edge = create_fig(keys_w, keys_h)
fig_keys_silk, ax_keys_silk = create_fig(keys_w, keys_h)
fig_keys_bcop, ax_keys_bcop = create_fig(keys_w, keys_h)
fig_keys_bottom_edge, ax_keys_bottom_edge = create_fig(keys_w, keys_h)

plt.rc('text', usetex=False)
plt.rc('font', weight='bold')

def draw_key_face(dx, dy, ix, iy, w, h, k, step_x, step_y) : 
  """
    Draw key hole in keyboard faceplate
  """
  x = dx + step_x*ix
  y = dy + step_y*iy

  rect1 = FancyBboxPatch((x-w/2. + min_r, y-h/2. + min_r),
                             width = w - 2*min_r, height = h - 2*min_r,
                             linewidth=outline_w, edgecolor = line_color, facecolor = "none", 
                             boxstyle="round,pad=1"
                         )
  ax_face_edge.add_patch(rect1)

  if len(k)>3 :
    ax_face_silk.text(x, y + h/2 + 1.5, k[3],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[4], color = "black")

def draw_key(dx, dy, ix, iy, w, h, k, last, panel_x, panel_y, part) : 
  """
    Draw key, top/bottom part
      - With silkscreen if part = top
      - With mounting holes if part = bottom
  """
  x = dx + (w + panel_x)*ix
  y = dy + (h + panel_y)*iy

  polys = [
    Polygon([(x-bridge_w/2-min_r, y-h/2), (x-w/2+min_r, y-h/2)], 
      closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Polygon([(x-w/2, y-h/2+min_r), (x-w/2, y+h/2-min_r)], 
      closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Polygon([(x-bridge_w/2-min_r, y+h/2), (x-w/2+min_r, y+h/2)], 
      closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Polygon([(x+bridge_w/2+min_r, y-h/2), (x+w/2-min_r, y-h/2)], 
      closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Polygon([(x+w/2, y-h/2+min_r), (x+w/2, y+h/2-min_r)], 
      closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Polygon([(x+bridge_w/2+min_r, y+h/2), (x+w/2-min_r, y+h/2)], 
      closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
  ]

  # Bridges
  if iy != 0 : 
    polys += [
      Polygon([(x+bridge_w/2, y-h/2-min_r), (x+bridge_w/2, y-h/2-panel_y/2)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      Polygon([(x-bridge_w/2, y-h/2-min_r), (x-bridge_w/2, y-h/2-panel_y/2)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]
  if iy != 3 : 
    polys += [
      Polygon([(x+bridge_w/2, y+h/2+min_r), (x+bridge_w/2, y+h/2+panel_y/2)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      Polygon([(x-bridge_w/2, y+h/2+min_r), (x-bridge_w/2, y+h/2+panel_y/2)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]

  arcs = [
    # Corners
    Arc((x-w/2+min_r, y-h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=180., theta2=270., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Arc((x-w/2+min_r, y+h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=90., theta2=180., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Arc((x+w/2-min_r, y-h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=270., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Arc((x+w/2-min_r, y+h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=0., theta2=90., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 

    # Bridges
    Arc((x-bridge_w/2-min_r, y-h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=0., theta2=90., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Arc((x+bridge_w/2+min_r, y-h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=90., theta2=180., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Arc((x-bridge_w/2-min_r, y+h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=270., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    Arc((x+bridge_w/2+min_r, y+h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=180., theta2=270., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
  ]

  if ix == 0 : 
    yy1 = y-h/2-min_r if iy == 0 else y-h/2-panel_y/2
    yy2 = y+h/2+min_r if iy == 3 else y+h/2+panel_y/2
    polys += [
      Polygon([(x-w/2-2*min_r, yy1), (x-w/2-2*min_r, yy2)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]
    if iy == 0 : 
      arcs += [
        Arc((x-w/2-min_r, y-h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=180., theta2=270., 
            linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      ]
    if iy == 3 : 
      arcs += [
        Arc((x-w/2-min_r, y+h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=90., theta2=180., 
            linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      ]


  if ix == last : 
    yy1 = y-h/2-min_r if iy == 0 else y-h/2-panel_y/2
    yy2 = y+h/2+min_r if iy == 3 else y+h/2+panel_y/2
    polys += [
      Polygon([(x+w/2+2*min_r, yy1), (x+w/2+2*min_r, yy2)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]
    if iy == 0 : 
      arcs += [
        Arc((x+w/2+min_r, y-h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=270., theta2=360., 
            linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      ]
    if iy == 3 : 
      arcs += [
        Arc((x+w/2+min_r, y+h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=0., theta2=90., 
            linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      ]

  if iy == 0 : 
    xx1 = x-w/2-min_r if ix == 0 else x-w/2-panel_x/2
    xx2 = x+w/2+min_r if ix == last else x+w/2+panel_x/2
    polys += [
      Polygon([(xx1, y-h/2-2*min_r), (x-bridge_w/2-min_r, y-h/2-2*min_r)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      Polygon([(x+bridge_w/2+min_r, y-h/2-2*min_r), (xx2, y-h/2-2*min_r)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]
    arcs += [
      Arc((x-bridge_w/2-min_r, y-h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=270., theta2=360., 
          linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      Arc((x+bridge_w/2+min_r, y-h/2-min_r), 2*min_r, 2*min_r, angle=0., theta1=180., theta2=270., 
          linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]

  if iy == 3 : 
    xx1 = x-w/2-min_r if ix == 0 else x-w/2-panel_x/2
    xx2 = x+w/2+min_r if ix == last else x+w/2+panel_x/2
    polys += [
      Polygon([(xx1, y+h/2+2*min_r), (x-bridge_w/2-min_r, y+h/2+2*min_r)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      Polygon([(x+bridge_w/2+min_r, y+h/2+2*min_r), (xx2, y+h/2+2*min_r)], 
        closed = False, linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]
    arcs += [
      Arc((x-bridge_w/2-min_r, y+h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=0., theta2=90., 
          linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
      Arc((x+bridge_w/2+min_r, y+h/2+min_r), 2*min_r, 2*min_r, angle=0., theta1=90., theta2=180., 
          linewidth=outline_w, edgecolor = line_color, facecolor = "none"), 
    ]

  if part == "top" : 
    for p in polys : ax_keys_edge.add_patch(p)
    for a in arcs : ax_keys_edge.add_patch(a)

    if k[2][0] == "black" : 
      rect2 = FancyBboxPatch((x-w/2. + min_r + silk_dist, y-h/2. + min_r + silk_dist),
                             width = w - 2*min_r - 2*silk_dist, height = h - 2*min_r - 2*silk_dist,
                             linewidth=0.5, edgecolor = line_color, facecolor = k[2][0], 
                             boxstyle="round,pad=1"
                         )
      ax_keys_silk.add_patch(rect2)

    ax_keys_silk.text(x, y - 0.3, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[2][1])

    rect3 = FancyBboxPatch((x-w/2.+copper_dist + min_r, y-h/2.+copper_dist + min_r),
                             width = w - 2*min_r-2*copper_dist, height = h - 2*min_r-2*copper_dist,
                             linewidth=0.5, edgecolor = line_color, facecolor = "black", 
                             boxstyle="round,pad=1"
                         )
    ax_keys_bcop.add_patch(rect3)

    #for p in polys : ax_keys_silk.add_patch(p)
    #for a in arcs : ax_keys_silk.add_patch(a)

  if part == "bottom" : 
    for p in polys : ax_keys_bottom_edge.add_patch(p)
    for a in arcs : ax_keys_bottom_edge.add_patch(a)

    c1 = Arc((x-3.5, y-h/2.+1.3), 1.0, 1.0, angle=0., theta1=0., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none")

    c2 = Arc((x+3.5, y-h/2.+1.3), 1.0, 1.0, angle=0., theta1=0., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none")
    ax_keys_bottom_edge.add_patch(c1)
    ax_keys_bottom_edge.add_patch(c2)

def draw_large_key(ix, iy, k) : 
  step_x = 12.3
  step_y = 10

  dx = face_w/2-step_x*2
  dy = 11.5
  draw_key_face(dx, dy, ix, iy, large_key_w, large_key_h, k, step_x, step_y)

  dx = keys_w/2-(large_key_bottom_w + 2*min_r)*2
  dy = 14. + large_key_bottom_h/2-large_key_h/2-0.3
  draw_key(dx, dy, ix, iy, large_key_w, large_key_h, k, 4, 
           2*min_r + large_key_bottom_w-large_key_w, 2*min_r + large_key_bottom_h - large_key_h, "top")

  dx = keys_w/2-(large_key_bottom_w + 2*min_r)*2
  dy = 14.
  draw_key(dx, dy, ix, iy, large_key_bottom_w, large_key_bottom_h, k, 4, 2*min_r, 2*min_r, "bottom")

def draw_small_key(ix, iy, k) : 
  step_x = 10.2
  step_y = 9.2

  dx = face_w/2-step_x*2.5
  dy = 51.5
  draw_key_face(dx, dy, ix, iy, small_key_w, small_key_h, k, step_x, step_y)

  dx = keys_w/2-(small_key_bottom_w + 2*min_r)*2.5
  dy = 67. + small_key_bottom_h/2-small_key_h/2-0.3
  draw_key(dx, dy, ix, iy, small_key_w, small_key_h, k, 5, 
          2*min_r + small_key_bottom_w-small_key_w, 2*min_r + small_key_bottom_h - small_key_h, "top")

  dx = keys_w/2-(small_key_bottom_w + 2*min_r)*2.5
  dy = 67.
  draw_key(dx, dy, ix, iy, small_key_bottom_w, small_key_bottom_h, k, 5, 2*min_r, 2*min_r, "bottom")

def draw_large_keys(keys) : 
  for iy, row in enumerate(keys) : 
    for ix, k in enumerate(row) : 
      draw_large_key(ix, iy, k)

def draw_small_keys(keys) : 
  for iy, row in enumerate(keys) : 
    for ix, k in enumerate(row) : 
      draw_small_key(ix, iy, k)

def draw_edges() : 
  rect1 = FancyBboxPatch((2., 2.), width = face_w-4, height = face_h-4,
            linewidth=outline_w, edgecolor = line_color, facecolor = "None", 
            boxstyle = "round,pad=2")
  ax_face_edge.add_patch(rect1)

  rect2 = FancyBboxPatch((face_w/2.-disp_w_inner/2.+1., disp_y_inner+1.), width = disp_w_inner-2, height = disp_h_inner-2,
            linewidth=outline_w, edgecolor = line_color, facecolor = "None", 
            boxstyle = "round,pad=1")
  ax_face_edge.add_patch(rect2)

  rect3 = Rectangle((0., 0.), width = keys_w, height = keys_h,
            linewidth=outline_w, edgecolor = line_color, facecolor = "None")
  ax_keys_edge.add_patch(rect3)

  rect4 = Rectangle((0., 0.), width = keys_w, height = keys_h,
            linewidth=outline_w, edgecolor = line_color, facecolor = "None")
  ax_keys_bottom_edge.add_patch(rect4)

  face_circs = [
    (mounting_hole_dist, mounting_hole_dist), 
    (face_w - mounting_hole_dist, mounting_hole_dist), 
    (mounting_hole_dist, face_h - mounting_hole_dist), 
    (face_w - mounting_hole_dist, face_h - mounting_hole_dist), 
    (mounting_hole_dist, face_h/2), 
    (face_w - mounting_hole_dist, face_h/2), 
  ]

  keys_circs = [
    (4, 4), 
    (keys_w - 4, 4), 
    (4, keys_h - 4), 
    (keys_w - 4, keys_h - 4), 
  ]
  for cx, cy in face_circs : 
    c = Arc((cx, cy), 2*mounting_hole_rad, 2*mounting_hole_rad, angle=0., theta1=0., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none")
    ax_face_edge.add_patch(c)
  for cx, cy in keys_circs : 
    c = Arc((cx, cy), 3.1, 3.1, angle=0., theta1=0., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none")
    ax_keys_edge.add_patch(c)
  for cx, cy in keys_circs : 
    c = Arc((cx, cy), 3.1, 3.1, angle=0., theta1=0., theta2=360., 
        linewidth=outline_w, edgecolor = line_color, facecolor = "none")
    ax_keys_bottom_edge.add_patch(c)

draw_large_keys(large_keys)
draw_small_keys(small_keys)
draw_edges()

fig_face_edge.savefig(f"{face_edge_name}.pdf")
fig_face_edge.savefig(f"{face_edge_name}.svg")
fig_face_silk.savefig(f"{face_silk_name}.pdf")
fig_face_silk.savefig(f"{face_silk_name}.svg")
fig_face_silk.savefig(f"{face_silk_name}.png", dpi = 300)
fig_keys_edge.savefig(f"{keys_edge_name}.pdf")
fig_keys_edge.savefig(f"{keys_edge_name}.svg")
fig_keys_silk.savefig(f"{keys_silk_name}.pdf")
fig_keys_silk.savefig(f"{keys_silk_name}.svg")
fig_keys_silk.savefig(f"{keys_silk_name}.png", dpi = 300)
fig_keys_bcop.savefig(f"{keys_bcop_name}.pdf")
fig_keys_bcop.savefig(f"{keys_bcop_name}.svg")
fig_keys_bcop.savefig(f"{keys_bcop_name}.png", dpi = 300)
fig_keys_bottom_edge.savefig(f"{keys_bottom_edge_name}.pdf")
fig_keys_bottom_edge.savefig(f"{keys_bottom_edge_name}.svg")

plt.show()
