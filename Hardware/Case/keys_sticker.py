import matplotlib.pyplot as plt
import numpy as np
import os

axes = plt.gca()
plt.gcf().set_size_inches(8.27,11.69)  # A4 size

plt.axis('off')
plt.rc('text', usetex=True)

axes.set_xlim(0., 210.*0.746)   # Adjust the factors for your printer
axes.set_ylim(0., 297.*0.74)

func_color = ("lightgray", "black")
shift_color = "tab:brown"
line_color = "black"
mode_color = ("tab:gray", "white")
memory_color = ('wheat', 'black')
input_color = ('none', 'black')
op_color = ('lightsteelblue', 'black')
c_color = ('tab:red', "white")
stack_color = ('darkgreen', 'white')

outname = "keys_sticker"

small_keys = [
  [
    (r"$\sqrt{x}$", 9, func_color, r"$x^{2}$", 7, shift_color), 
    (r"$1/x$", 9, func_color), 
    (r"$\mbox{erf}$", 9, func_color, r"$\mbox{erf}^{-1}$", 7, shift_color), 
    (r"R$\rightarrow$P", 8, func_color, r"P$\rightarrow$R", 7, shift_color), 
    (r"$\Gamma(x)$", 8, func_color,  r"$\ln\Gamma(x)$", 7, shift_color), 
    (r"$C_{y}^{x}$", 8, func_color,  r"$P_{y}^{x}$", 7, shift_color), 
  ], 

  [
    (r"$y^x$", 9, func_color, r"$\sqrt[x]{y}$", 7, shift_color), 
    (r"$\ln$", 9, func_color, r"$e^{x}$", 7, shift_color), 
    (r"$\lg$", 9, func_color, r"$10^{x}$", 7, shift_color), 
    (r"$\sin$", 9, func_color, r"$\sin^{-1}$", 7, shift_color), 
    (r"$\cos$", 9, func_color, r"$\cos^{-1}$", 7, shift_color), 
    (r"$\tan$", 9, func_color, r"$\tan^{-1}$", 7, shift_color), 
  ], 

  [
    (r"Drop", 8, stack_color, r"Rot$\uparrow$", 7, shift_color), 
    (r"X$\leftrightarrow$Y", 8, stack_color, r"LAST$x$", 7, shift_color), 
    ("DR", 9, mode_color, r"D$\leftrightarrow$R", 7, shift_color), 
    ("M$+$", 9, memory_color, r"M$-$", 7, shift_color), 
    ("MR", 9, memory_color), 
    ("MS", 9, memory_color), 
  ], 

  [
    ("F", 10, (shift_color, 'white')), 
    ("G", 10, ('tab:blue', 'white')), 
    ("Mode", 8, mode_color), 
    ("Uncr", 9, mode_color), 
    ("Prec", 9, mode_color), 
    ("On", 10, c_color, r"Off", 7, shift_color), 
  ], 

]

large_keys = [
  [ 
    ("0", 11, input_color), 
    ("/$-$/", 9, input_color), 
    (".", 11, input_color), 
    ("$\pm$", 10, input_color), 
    ("Enter", 9, stack_color), 
  ], 
  [ 
    ("1", 11, input_color, r"$\pi$", 8, shift_color), 
    ("2", 11, input_color), 
    ("3", 11, input_color), 
    ("$+$", 11, op_color, r"$N\sigma(x)$", 8, shift_color), 
    ("$-$", 11, op_color, r"$N\sigma(x-y)$", 8, shift_color), 
  ], 
  [ 
    ("4", 11, input_color, r"Pois$(\!k_{x}|\lambda_{y}\!)$", 7, shift_color), 
    ("5", 11, input_color, r"$p(\chi^2(y)\!\!>\!\!x)$", 7, shift_color), 
    ("6", 11, input_color), 
    (r"$\times$", 11, op_color), 
    ("$\div$", 11, op_color), 
  ], 
  [ 
    ("7", 11, input_color, r"$\eta(\theta)$", 8, shift_color), 
    ("8", 11, input_color, r"$\gamma(\beta)$", 8, shift_color), 
    ("9", 11, input_color, r"$p(z\to xy)$", 8, shift_color), 
    ("Exp", 10, input_color), 
    ("C", 10, c_color, r"CST", 7, shift_color), 
  ], 
]

large_key_w = 9.1*0.85
large_key_h = 5.1*0.85
large_hole_w = 10.1
large_hole_h = 6.1

small_key_w = 8.1*0.9
small_key_h = 4.1*0.9
small_hole_w = 9.1
small_hole_h = 4.6

face_width = (70. + 6.)*0.97
face_height = (127 + 6.)*0.97

disp_width = 60.2*1.03
disp_height = 37.2*1.03

def draw_sticker(dx = 40, dy = 10, onlykeys = False) : 

  step_x = 14
  step_y = 10
  shift_y = 8.5
  if (onlykeys) : 
    step_x = large_key_w
    step_y = large_key_h
    shift_y = 0.

  if not onlykeys : 
    rect1 = plt.Rectangle((dx - face_width/2., dy + 0.015*face_height - 3.), 
                         width = face_width, height = face_height, linewidth=0.25, 
                         edgecolor = line_color, facecolor = "none")

    rect2 = plt.Rectangle((dx - disp_width/2., dy + 127. - 7 - 37/2. - disp_height/2.), 
                         width = disp_width, height = disp_height, linewidth=0.25, 
                         edgecolor = line_color, facecolor = "none")

    axes.add_patch(rect1)
    axes.add_patch(rect2)

  for i, row in enumerate(large_keys) : 
    for j, k in enumerate(row) : 

      if not onlykeys : 
        rect2 = plt.Rectangle((dx + step_x*(j-2) - large_hole_w/2., dy + shift_y + step_y*i - large_hole_h/2.), 
                         width = large_hole_w, height = large_hole_h, linewidth=0.25, 
                         edgecolor = line_color, facecolor = 'none')
        axes.add_patch(rect2)


      rect1 = plt.Rectangle((dx + step_x*(j-2) - large_key_w/2., dy + shift_y + step_y*i - large_key_h/2.), 
                         width = large_key_w, height = large_key_h, linewidth=0.25, 
                         edgecolor = line_color, facecolor = k[2][0])

      axes.add_patch(rect1)
      plt.text(dx + step_x*(j-2), dy + shift_y + step_y*i - 0.15, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[2][1])

      if (not onlykeys) and (len(k)>3) : 
        plt.text(dx + step_x*(j-2), dy + shift_y + step_y*i + large_hole_h/2. + 0.3, k[3],
          horizontalalignment='center',
          verticalalignment='bottom',
          fontsize = k[4], color = k[5])


  step_x = 11.4
  step_y = 7.7
  shift_y = 50.
  if (onlykeys) : 
    step_x = small_key_w
    step_y = small_key_h
    shift_y = 19.

  for i, row in enumerate(small_keys) : 
    for j, k in enumerate(row) : 

      if not onlykeys : 
        rect2 = plt.Rectangle((dx + step_x*(j-2.5) - small_hole_w/2., dy + shift_y + step_y*i - small_hole_h/2.), 
                         width = small_hole_w, height = small_hole_h, linewidth=0.25, 
                         edgecolor = line_color, facecolor = "none")
        axes.add_patch(rect2)

      rect1 = plt.Rectangle((dx + step_x*(j-2.5) - small_key_w/2., dy + shift_y + step_y*i - small_key_h/2.), 
                         width = small_key_w, height = small_key_h, linewidth=0.25, 
                         edgecolor = line_color, facecolor = k[2][0])

      axes.add_patch(rect1)
      plt.text(dx + step_x*(j-2.5), dy + shift_y + step_y*i - 0.15, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[2][1])

      if (not onlykeys) and (len(k)>3) : 
        plt.text(dx + step_x*(j-2.5), dy + shift_y + step_y*i + small_hole_h/2. + 0.15, k[3],
          horizontalalignment='center',
          verticalalignment='bottom',
          fontsize = k[4], color = k[5])

# Draw two stickers side-by-side
draw_sticker(40, 85)
draw_sticker(115, 85)

# Place the only-keys stickers inside the display area to save sticker film
draw_sticker(40, 171.5, onlykeys = True)
draw_sticker(115, 171.5, onlykeys = True)

# ps2pdf creates a much smaller PDF file than matplotlib directly
# So saving PS and converting to PDF afterwards
plt.savefig(outname + ".pdf")
os.system(f"pdftops {outname}.pdf")
os.system(f"ps2pdf14 {outname}.ps")
os.system(f"rm {outname}.ps")

plt.show()
