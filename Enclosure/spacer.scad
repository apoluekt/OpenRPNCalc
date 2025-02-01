module rounded_parallelepiped(length, width, height, radius) {
    minkowski() {
        // Base cube
        cube([length-2*radius, width-2*radius, height/2], center = true);

        // Cylinder for rounding
        cylinder(h = height/2, r = radius, center = true, $fn=32);
    }
}

module key(x, y) {
    translate([x, y, 0])
    union() {
        cube([7.4, 7.0, 5.], center = true); 
        translate([0,  2, 0]) cube([9.2, 1.6, 5.], center = true); 
        translate([0, -2, 0]) cube([9.2, 1.6, 5.], center = true); 
        //if (y<-57) {
        //    translate([ 3.5, -4.5, 0]) cube([3.5, 3.5, 5.], center = true); 
        //    translate([-3.5, -4.5, 0]) cube([3.5, 3.5, 5.], center = true); 
        //}
    }
}

module large_keys() {
    for (x=[0, 1, 2, 3, 4]) {
        for (y=[0, 1, 2, 3]) {
            key((x-2.)*12.3, y*10.-58.); 
        }
    }
}

module small_keys() {
    for (x=[0, 1, 2, 3, 4, 5]) {
        for (y=[0, 1, 2, 3]) {
            key((x-2.5)*10.2, y*9.2-18.); 
        }
    }
}

l = 71.4;
h = 139.4;

//w = 3.4; // - should be like this, but adjusted for my 3D printer
w = 3.2;

r = 2.0;
d = 5.0;
mr = 3.4/2.;
hole_l = 71.-5.;
hole_h = 139.-5.;
lcd_l = 63.2; 
lcd_h = 43.4; 

difference() {
    union() {
        // Frame 
        difference() {
            // Outer profile
            rounded_parallelepiped(l, h, w, r);
            union() {
                // Inner profile
                rounded_parallelepiped(l-2*d, h-2*d, w+1, 1.7);
                // Mounting holes
                translate([ hole_l/2,  hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([ hole_l/2, -hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([ hole_l/2,         0, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([-hole_l/2,  hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([-hole_l/2, -hole_h/2, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                translate([-hole_l/2,         0, 0.]) cylinder(h = w+1, r = mr, center = true, $fn=32); 
                // LCD cutout
                translate([0., h/2.-(7.+lcd_h/2.), 0.]) cube([lcd_l, lcd_h, w+1], center = true); 
            }
        }; 
        // LCD support
        translate([0., h/2.-d-50/2.+0.1, -w/2.+2.1/2]) cube([lcd_l+0.2, 50.2, 2.3], center = true); 
        translate([ 19., h/2.-7.+3./2., 0.]) cube([26., 3., w], center = true); 
        translate([-19., h/2.-7.+3./2., 0.]) cube([26., 3., w], center = true); 
        translate([0., h/2.-7.-4.7/2.-lcd_h, 0.]) cube([63., 4.7, w], center = true); 
        // Keyboard support
        translate([0., -h/2.+d+80/2.-0.1, -w/2.+1.2/2]) cube([62.0, 80.2, 1.2], center = true); 
    }; 
    // LCD cable hole
    translate([0, h/2-4.-1.7, 0.]) rounded_parallelepiped(15., 3.41, w+1, 1.7); 
    // Battery holder hole
    translate([17.2, 30.7, 0.]) cylinder(h=w+1, r = 12.2, center=true, $fn=64); 
    translate([17.2, 30.7, 0.]) rounded_parallelepiped(9.5, 30.5, w+1, 1.7); 
    // ST-link interface hole
    translate([22.2, 53.0, 0.]) rounded_parallelepiped(13.7, 3.41, w+1, 1.7); 
    // Key holes
    large_keys(); 
    small_keys(); 
}
