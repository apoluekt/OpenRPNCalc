import matplotlib.pyplot as plt
import numpy as np

axes = plt.gca()
plt.gcf().set_size_inches(8.27,11.69)
#fig = plt.figure(figsize=(11.69,8.27))

plt.axis('off')
axes.set_xlim(0., 210.*0.746)
axes.set_ylim(0., 297.*0.74)

#plt.text(5, 60, '$Y = x^2$', fontsize = 16, 
#         bbox = dict(facecolor = 'red', alpha = 0.2))

small_keys = [
  [
    (r"erf", 8, 'none', 'black'), 
    (r"$\sqrt{\;}$", 8, 'none', 'black'), 
    (r"Pol", 8, 'none', 'black'), 
    (r"$1/x$", 8, 'none', 'black'), 
    (r"Drop", 8, 'none', 'black'), 
    (r"X$\leftrightarrow$Y", 8, 'none', 'black'), 
  ], 

  [
    (r"$Y^X$", 8, 'none', 'black'), 
    (r"$\ln$", 8, 'none', 'black'), 
    (r"$\lg$", 8, 'none', 'black'), 
    (r"$\sin$", 8, 'none', 'black'), 
    (r"$\cos$", 8, 'none', 'black'), 
    (r"$\tan$", 8, 'none', 'black'), 
  ], 

  [
    (" ", 8, 'none', 'black'), 
    (" ", 8, 'none', 'black'), 
    ("R-D", 9, 'none', 'black'), 
    ("M$+$", 9, 'none', 'black'), 
    ("MR", 9, 'none', 'black'), 
    ("MS", 9, 'none', 'black'), 
  ], 

  [
    ("F", 10, 'brown', 'white'), 
    ("G", 10, 'blue', 'white'), 
    ("Mode", 8, 'none', 'black'), 
    ("Uncr", 8, 'none', 'black'), 
    ("Prec", 8, 'none', 'black'), 
    ("On", 8, 'red', 'white'), 
  ], 

]

large_keys = [
  [ 
    ("0", 10, 'none', 'black'), 
    ("/-/", 10, 'none', 'black'), 
    (".", 10, 'none', 'black'), 
    ("$\pm$", 10, 'none', 'black'), 
    ("Enter", 8, 'none', 'black'), 
  ], 
  [ 
    ("1", 10, 'none', 'black'), 
    ("2", 10, 'none', 'black'), 
    ("3", 10, 'none', 'black'), 
    ("$+$", 10, 'none', 'black'), 
    ("$-$", 10, 'none', 'black'), 
  ], 
  [ 
    ("4", 10, 'none', 'black'), 
    ("5", 10, 'none', 'black'), 
    ("6", 10, 'none', 'black'), 
    (r"$\times$", 10, 'none', 'black'), 
    ("$\div$", 10, 'none', 'black'), 
  ], 
  [ 
    ("7", 10, 'none', 'black'), 
    ("8", 10, 'none', 'black'), 
    ("9", 10, 'none', 'black'), 
    ("Exp", 10, 'none', 'black'), 
    ("C", 10, 'red', 'white'), 
  ], 
]

large_key_w = 9.2*0.85
large_key_h = 5.2*0.85

small_key_w = 8.2*0.9
small_key_h = 4.2*0.9

for i, row in enumerate(large_keys) : 
  for j, k in enumerate(row) : 

    rect = plt.Rectangle((40 + 14*(j-2), 10 + 8.5 + 10*i), 
                         width = large_key_w, height = large_key_h, linewidth=0.25, 
                         edgecolor = 'black', facecolor = k[2])

    axes.add_patch(rect)
    plt.text(40 + 14*(j-2) + large_key_w/2., 10 + 8.5 + 10*i + large_key_h/2.-0.3, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[3])

for i, row in enumerate(small_keys) : 
  for j, k in enumerate(row) : 

    rect = plt.Rectangle((40 + 11.4*(j-2.5), 10 + 50 + 7.7*i), 
                         width = small_key_w, height = small_key_h, linewidth=0.25, 
                         edgecolor = 'black', facecolor = k[2])

    axes.add_patch(rect)
    plt.text(40 + 11.4*(j-2.5) + small_key_w/2., 10 + 50 + 7.7*i + small_key_h/2.-0.3, k[0],
        horizontalalignment='center',
        verticalalignment='center',
        fontsize = k[1], color = k[3])

plt.savefig("keys_sticker.pdf")
plt.show()
