import matplotlib.pyplot as plt
import numpy as np

axes = plt.gca()
plt.gcf().set_size_inches(8.27,11.69)
#fig = plt.figure(figsize=(11.69,8.27))

plt.axis('off')
plt.rc('text', usetex=True)

axes.set_xlim(0., 210.*0.746)
axes.set_ylim(0., 297.*0.74)

#plt.text(5, 60, '$Y = x^2$', fontsize = 16, 
#         bbox = dict(facecolor = 'red', alpha = 0.2))

small_keys = [
  [
    (r"$\sqrt{x}$", 9, 'lightgray', 'black', r"$x^{2}$", 7, "tab:brown"), 
    (r"$1/x$", 9, 'lightgray', 'black'), 
    (r"erf", 9, 'lightgray', 'black', r"erf${}^{-1}$", 7, "tab:brown"), 
    (r"R$\rightarrow$P", 8, 'lightgray', 'black', r"P$\rightarrow$R", 7, "tab:brown"), 
    (r"$\Gamma(x)$", 8, 'lightgray', 'black',  r"$\ln\Gamma(x)$", 7, "tab:brown"), 
    (r"$C_{y}^{x}$", 8, 'lightgray', 'black',  r"$P_{y}^{x}$", 7, "tab:brown"), 
  ], 

  [
    (r"$y^x$", 9, 'lightgray', 'black', r"$\sqrt[x]{y}$", 7, "brown"), 
    (r"$\ln$", 9, 'lightgray', 'black', r"$e^{x}$", 7, "brown"), 
    (r"$\lg$", 9, 'lightgray', 'black', r"$10^{x}$", 7, "brown"), 
    (r"$\sin$", 9, 'lightgray', 'black', r"sin${}^{-1}$", 7, "brown"), 
    (r"$\cos$", 9, 'lightgray', 'black', r"cos${}^{-1}$", 7, "brown"), 
    (r"$\tan$", 9, 'lightgray', 'black', r"tan${}^{-1}$", 7, "brown"), 
  ], 

  [
    (r"Drop", 8, 'lightsteelblue', 'black'), 
    (r"X$\leftrightarrow$Y", 8, 'lightsteelblue', 'black', r"LAST$x$", 7, "tab:brown"), 
    ("DR", 9, 'tab:gray', 'white', r"D$\leftrightarrow$R", 7, "tab:brown"), 
    ("M$+$", 9, 'wheat', 'black', r"M$-$", 7, "tab:brown"), 
    ("MR", 9, 'wheat', 'black'), 
    ("MS", 9, 'wheat', 'black'), 
  ], 

  [
    ("F", 10, 'tab:brown', 'white'), 
    ("G", 10, 'tab:blue', 'white'), 
    ("Mode", 8, 'tab:gray', 'white'), 
    ("Uncr", 9, 'tab:gray', 'white'), 
    ("Prec", 9, 'tab:gray', 'white'), 
    ("On", 10, 'tab:red', 'white', r"Off", 7, "tab:brown"), 
  ], 

]

large_keys = [
  [ 
    ("0", 11, 'none', 'black'), 
    ("/-/", 10, 'none', 'black'), 
    (".", 11, 'none', 'black'), 
    ("$\pm$", 11, 'none', 'black'), 
    ("Enter", 9, 'darkgreen', 'white'), 
  ], 
  [ 
    ("1", 11, 'none', 'black', r"$\pi$", 8, "brown"), 
    ("2", 11, 'none', 'black'), 
    ("3", 11, 'none', 'black'), 
    ("$+$", 11, 'thistle', 'black'), 
    ("$-$", 11, 'thistle', 'black'), 
  ], 
  [ 
    ("4", 11, 'none', 'black'), 
    ("5", 11, 'none', 'black'), 
    ("6", 11, 'none', 'black'), 
    (r"$\times$", 11, 'thistle', 'black'), 
    ("$\div$", 11, 'thistle', 'black'), 
  ], 
  [ 
    ("7", 11, 'none', 'black'), 
    ("8", 11, 'none', 'black'), 
    ("9", 11, 'none', 'black'), 
    ("Exp", 10, 'none', 'black'), 
    ("C", 10, 'red', 'white', r"CLST", 7, "brown"), 
  ], 
]

large_key_w = 9.2*0.85
large_key_h = 5.2*0.85
large_hole_w = 10.
large_hole_h = 6.

small_key_w = 8.2*0.9
small_key_h = 4.2*0.9
small_hole_w = 9.
small_hole_h = 4.5

face_width = (70. + 6.)*0.97
face_height = (127 + 6.)*0.97

disp_width = 60*1.03
disp_height = 37*1.03

rect1 = plt.Rectangle((40 - face_width/2., 10 + 0.015*face_height - 3.), 
                         width = face_width, height = face_height, linewidth=0.25, 
                         edgecolor = 'black', facecolor = "none")

rect2 = plt.Rectangle((40 - disp_width/2., 10 + 127. - 7 - 37/2. - disp_height/2.), 
                         width = disp_width, height = disp_height, linewidth=0.25, 
                         edgecolor = 'black', facecolor = "none")

axes.add_patch(rect1)
axes.add_patch(rect2)

for i, row in enumerate(large_keys) : 
  for j, k in enumerate(row) : 

    rect2 = plt.Rectangle((40 + 14*(j-2) - large_hole_w/2., 10 + 8.5 + 10*i - large_hole_h/2.), 
                         width = large_hole_w, height = large_hole_h, linewidth=0.25, 
                         edgecolor = 'black', facecolor = 'none')

    rect1 = plt.Rectangle((40 + 14*(j-2) - large_key_w/2., 10 + 8.5 + 10*i - large_key_h/2.), 
                         width = large_key_w, height = large_key_h, linewidth=0.25, 
                         edgecolor = 'black', facecolor = k[2])

    axes.add_patch(rect2)
    axes.add_patch(rect1)
    plt.text(40 + 14*(j-2), 10 + 8.5 + 10*i -0.3, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[3])

    if len(k)>4 : 
      plt.text(40 + 14*(j-2), 10 + 8.5 + 10*i + large_hole_h/2. + 0.05, k[4],
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize = k[5], color = k[6])


for i, row in enumerate(small_keys) : 
  for j, k in enumerate(row) : 

    print(k)

    rect2 = plt.Rectangle((40 + 11.4*(j-2.5) - small_hole_w/2., 10 + 50 + 7.7*i - small_hole_h/2.), 
                         width = small_hole_w, height = small_hole_h, linewidth=0.25, 
                         edgecolor = 'black', facecolor = "none")

    rect1 = plt.Rectangle((40 + 11.4*(j-2.5) - small_key_w/2., 10 + 50 + 7.7*i - small_key_h/2.), 
                         width = small_key_w, height = small_key_h, linewidth=0.25, 
                         edgecolor = 'black', facecolor = k[2])

    axes.add_patch(rect2)
    axes.add_patch(rect1)
    plt.text(40 + 11.4*(j-2.5), 10 + 50 + 7.7*i - 0.3, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[3])

    if len(k)>4 : 
      plt.text(40 + 11.4*(j-2.5), 10 + 50 + 7.7*i + small_hole_h/2. + 0.05, k[4],
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize = k[5], color = k[6])


plt.savefig("keys_sticker.pdf")
plt.show()
