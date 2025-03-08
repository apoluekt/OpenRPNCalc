module rounded_parallelepiped(length, width, height, radius) {
    minkowski() {
        // Base cube
        cube([length-2*radius, width-2*radius, height/2], center = true);

        // Cylinder for rounding
        cylinder(h = height/2, r = radius, center = true, $fn=32);
    }
}

union() {
    for(x=[0:4]) {
        for (y=[0:4]) {
            translate([ 10*x,  7.*y, 0.7/2.+0.9]) cylinder(h = 0.7, r = 1.2, center = true, $fn=32); 
            translate([ 10*x,  7.*y, 0.9/2.]) rounded_parallelepiped(9., 6., 0.9, 1.5); 
        }
    }
}
