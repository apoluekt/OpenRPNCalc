# Outer dimensions
pcb_width = 73.0
pcb_height = 139.0

# Upper left corner position on the PCB drawing
corner_x = 40
corner_y = 40

# LCD outline sizes + 0.2mm tolerance for LCD cutout
lcd_width = 63.+0.2
lcd_height = 43.+0.2

visible_lcd_width = 60.
visible_lcd_height = 37. 

keyboard_width = 63.
keyboard_height = 78.

# Radius of PCB outline corners
corner_rad = 2.7

large_key_w = 10.1
large_key_h = 6.8

small_key_w = 8.0
small_key_h = 5.0

def get_large_keys_coord(dx, dy, nx, ny) : 
    step_x = 12.3
    step_y = 10
    dx = corner_x + pcb_width/2. + dx
    dy = corner_y + pcb_height/2. + dy
    coord = []
    for iy in range(ny) : 
        for ix in range(nx) : 
             x = dx + step_x*(ix - (nx-1)/2.)
             y = dy + step_y*(-iy + (ny-1)/2.)
             coord += [ (x, y) ]
    print(coord)
    return coord

def get_small_keys_coord(dx, dy, nx, ny) : 
    step_x = 10.2
    step_y = 8.2
    dx = corner_x + pcb_width/2. + dx
    dy = corner_y + pcb_height/2. + dy
    coord = []
    for iy in range(ny) : 
        for ix in range(nx) : 
             x = dx + step_x*(ix - (nx-1)/2.)
             y = dy + step_y*(-iy + (ny-1)/2.)
             if (iy == 0 and ix == 5) : 
                # Special case for long "ENTER"
                coord[-1] = ((coord[-1][0] + x)/2., coord[-1][1])
             else : 
                coord += [ (x, y) ]
    return coord

large_keys_coord = get_large_keys_coord(0., 45., 5, 4)
small_keys_coord = get_small_keys_coord(0., 4.5, 6, 5)
