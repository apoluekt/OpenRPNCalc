module rounded_parallelepiped(length, width, height, radius) {
    minkowski() {
        // Base cube
        cube([length-2*radius, width-2*radius, height/2], center = true);

        // Cylinder for rounding
        cylinder(h = height/2, r = radius, center = true, $fn=32);
    }
}

l = 71.4;
h = 139.4;
w = 3.6;
r = 2.0;
d = 5.1;
mr = 2.4/2.;
mr2 = 3.5/2.;
hole_l = 71.-5.;
hole_h = 139.-5.;


difference() {
    union() {
        // Frame 
        difference() {
            // Outer profile
            rounded_parallelepiped(l, h, w, r);
            union() {
                // Inner profile
                rounded_parallelepiped(l-2*d, h-2*d, w+1, 1.7);
                translate([ hole_l/2,  hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([ hole_l/2, -hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([ hole_l/2,         0, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([-hole_l/2,  hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([-hole_l/2, -hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([-hole_l/2,         0, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([ hole_l/2,  hole_h/2, 0.5]) cylinder(h = 2.8, r = mr2, center = true, $fn=32); 
                translate([ hole_l/2, -hole_h/2, 0.5]) cylinder(h = 2.8, r = mr2, center = true, $fn=32); 
                translate([ hole_l/2,         0, 0.5]) cylinder(h = 2.8, r = mr2, center = true, $fn=32); 
                translate([-hole_l/2,  hole_h/2, 0.5]) cylinder(h = 2.8, r = mr2, center = true, $fn=32); 
                translate([-hole_l/2, -hole_h/2, 0.5]) cylinder(h = 2.8, r = mr2, center = true, $fn=32); 
                translate([-hole_l/2,         0, 0.5]) cylinder(h = 2.8, r = mr2, center = true, $fn=32); 
            }
        }; 
        // Lid
        translate([0., 0., -w/2.+0.8/2]) cube([62.0, 130.2, 0.8], center = true); 
    }; 
    // LCD cable hole
    translate([0, h/2-4.-1.7, 0.81]) rounded_parallelepiped(15., 3.41, w, 1.7); 
    // ST-link connector hole
    translate([ 22.2, h/2-d/2, 0.81]) cube([13.7, d+0.1, w], center = true);
    // Reset button hole
    translate([-17.8,  56.1, 0.]) cylinder(h = w+1, r = 4.4/2., center = true, $fn=32); 
}
