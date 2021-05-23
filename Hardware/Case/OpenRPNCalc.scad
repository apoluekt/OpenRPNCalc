// Thickness values for the case elements
pcb_thickness = 1.6;       // PCB thickness
lcd_thickness = 2.6;       // LCD thickness needed for border around screen
battery_thickness = 5.5;   // Tallest element on the back of the PCB is battery holder

// Thickness values for elements of keyboard spacer
switch_thickness = 2.0; 
pusher_thickness = 0.6;       
spacer_spring_thickness = 0.2;

// Thickness values for elements of keypad
keypad_thickness = 0.6; 
keypad_spring_thickness = 0.4; // Optionally can make flat spring thinner than keypad
keypad_tolerance = 0.4;        // Gap between keypad and case top

face_thickness = 0.8; 
back_thickness = 0.8; 
chamfer_thickness = 2.5; 
wall_width = 3.0; 
joint_thickness = 1.6; 
joint_width = 1.4; 
joint_tolerance = 0.05; 

pcb_width = 70.; 
pcb_height = 127.;
pcb_tolerance = 0.2; 

keypad_large_row = 8.5; // Distance from bottom PCB edge to the  
                        // center of 1st (bottom) row of large keys
keypad_small_row = 50; // Distance from bottom PCB edge to the  
                        // center of 1st (bottom) row of small keys

// Derived dimensions
spacer_thickness = switch_thickness + pusher_thickness; 
keyboard_thickness = spacer_thickness + keypad_thickness + keypad_tolerance; 

top_thickness = pcb_thickness + keyboard_thickness + face_thickness; 
bottom_thickness = battery_thickness + back_thickness; 
tot_thickness = top_thickness + bottom_thickness; 
tot_width = pcb_width + 2*wall_width; 
tot_height = pcb_height + 2*wall_width; 

module top_half() {
    difference() {
        union() {
            linear_extrude(height = top_thickness-chamfer_thickness) {
                square([tot_width, tot_height], center = true); 
            }
            translate([0, 0, top_thickness-chamfer_thickness]) {
                linear_extrude(height = chamfer_thickness, scale = 0.97) {
                    square([tot_width, tot_height], center = true); 
                }
            }
        }

        linear_extrude(height = pcb_thickness + keyboard_thickness) {
            square([pcb_width + 2*pcb_tolerance, pcb_height + 2*pcb_tolerance], 
                       center = true); 
        }

        // Cut-outs for large keys
        union() { 
            for (i=[0:4]) {
                for (j=[0:3]) {
                   translate([14*(i-2), 10*j-pcb_height/2.+keypad_large_row, 
                              pcb_thickness + keyboard_thickness]) 
//                        cube([9.6, 5.6, 10], center = true); 
                        linear_extrude(height = face_thickness, scale = 1.1) 
                            square([9.6, 5.6], center = true); 

                }
            }
        }

        // Cut-outs for small keys
        union() { 
            for (i=[0:5]) {
                for (j=[0:3]) {
                   translate([11.4*(i-2.5), 
                        7.7*j-pcb_height/2.+keypad_small_row, 
                        pcb_thickness + keyboard_thickness]) 
//                        cube([8.6, 4.6, 10], center = true); 
                        linear_extrude(height = face_thickness, scale = 1.1) 
                            square([8.6, 4.6], center = true); 

                }
            }
        }
        
        // Cut-out for display
        translate([0, pcb_height/2.-7-37/2., pcb_thickness + keyboard_thickness]) 
          linear_extrude(height = face_thickness, scale = 1.03) 
            square([60, 37], center = true); 
        
        // Cut-out for display cable
        translate([0, pcb_height/2., pcb_thickness/2.]) 
          cube([12, 2, pcb_thickness*2], center = true); 
        
    }

    // Supporting edge between display and keyboard
    translate([0, pcb_height/2.-50+2.5, pcb_thickness + keyboard_thickness/2]) 
      cube([pcb_width+2*pcb_tolerance, 2.4, keyboard_thickness], 
           center = true);     

    // Supporting edges above display
    translate([6+30/2, (pcb_height + 2*pcb_tolerance)/2.-1, 
               pcb_thickness + keyboard_thickness/2]) 
       cube([30, 2, keyboard_thickness], center = true); 
    translate([-6-30/2, (pcb_height + 2*pcb_tolerance)/2.-1, 
                pcb_thickness + keyboard_thickness/2]) 
       cube([30, 2, keyboard_thickness], center = true);     

    // Supporting edge below keyboard
    translate([0, -(pcb_height + 2*pcb_tolerance)/2+1, 
               pcb_thickness + keyboard_thickness/2]) 
       cube([pcb_width + 2*pcb_tolerance, 2, keyboard_thickness], center = true);     


    // Joint around PCB
    translate([0, 0, -joint_thickness]) 
    difference() {
      linear_extrude(height = joint_thickness) {
        difference() {
            square([pcb_width + 2*pcb_tolerance+2*joint_width-joint_tolerance, 
                    pcb_height + 2*pcb_tolerance + 2*joint_width-joint_tolerance], center = true); 
            square([pcb_width + 2*pcb_tolerance, 
                    pcb_height + 2*pcb_tolerance], center = true); 
        }
      }
      // Cut-out for display cable
      translate([0, pcb_height/2., pcb_thickness/2.]) 
                  cube([12, 2, pcb_thickness*2], center = true); 
    }

    // Edge around display
    translate([0, pcb_height/2.-7-37/2., pcb_thickness + lcd_thickness]) 
    linear_extrude(height = keyboard_thickness-lcd_thickness) {
        difference() {
            square([60.+2*0.8,37+2*0.8], center = true); 
            square([60., 37], center = true); 
        }
    }

    // Latches
    translate([-pcb_width/3, pcb_height/2. + pcb_tolerance + joint_width-0.2, -joint_thickness+0.4]) rotate(a = [0, 90, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([+pcb_width/3, pcb_height/2. + pcb_tolerance + joint_width-0.2, -joint_thickness+0.4]) rotate(a = [0, 90, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/3, -pcb_height/2. - pcb_tolerance - joint_width+0.2, -joint_thickness+0.4]) rotate(a = [0, 90, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([+pcb_width/3, -pcb_height/2. - pcb_tolerance - joint_width+0.2, -joint_thickness+0.4]) rotate(a = [0, 90, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/2 - pcb_tolerance - joint_width+0.2, pcb_height/3., -joint_thickness+0.4]) rotate(a = [90, 0, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/2 - pcb_tolerance - joint_width+0.2, -pcb_height/3., -joint_thickness+0.4]) rotate(a = [90, 0, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([ pcb_width/2 + pcb_tolerance + joint_width-0.2, pcb_height/3., -joint_thickness+0.4]) rotate(a = [90, 0, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([ pcb_width/2 + pcb_tolerance + joint_width-0.2, -pcb_height/3., -joint_thickness+0.4]) rotate(a = [90, 0, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/2 - pcb_tolerance - joint_width+0.2, 0, -joint_thickness+0.4]) rotate(a = [90, 0, 0]) cylinder(15, r=0.4, $fn=16, center = true); 
    translate([ pcb_width/2 + pcb_tolerance + joint_width-0.2, 0, -joint_thickness+0.4]) rotate(a = [90, 0, 0]) cylinder(15, r=0.4, $fn=16, center = true); 

}; 
    
module bottom_half() {
    difference() {
        union() {
            linear_extrude(height = bottom_thickness - chamfer_thickness) {
                square([tot_width, tot_height], center = true); 
            }
            translate([0, 0, bottom_thickness - chamfer_thickness]) {
                linear_extrude(height = chamfer_thickness, scale = 0.97) {
                    square([tot_width, tot_height], center = true); 
                }
            }
        }
        linear_extrude(height = battery_thickness) {
                square([pcb_width+2*pcb_tolerance, pcb_height+2*pcb_tolerance], 
                   center = true); 
        }

      // Joint around PCB
      translate([0, 0, 0]) 
        linear_extrude(height = joint_thickness) {
          difference() {
            square([pcb_width + 2*pcb_tolerance+2*joint_width + joint_tolerance, 
                    pcb_height + 2*pcb_tolerance + 2*joint_width + joint_tolerance], center = true); 
            square([pcb_width + 2*pcb_tolerance, 
                    pcb_height + 2*pcb_tolerance], center = true); 
          }
        }

    translate([-pcb_width/3, pcb_height/2. + pcb_tolerance + joint_width-0.2 + joint_tolerance, joint_thickness-0.4]) rotate(a = [0, 90, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([+pcb_width/3, pcb_height/2. + pcb_tolerance + joint_width-0.2 + joint_tolerance, joint_thickness-0.4]) rotate(a = [0, 90, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/3, -pcb_height/2. - pcb_tolerance - joint_width+0.2 - joint_tolerance, joint_thickness-0.4]) rotate(a = [0, 90, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([+pcb_width/3, -pcb_height/2. - pcb_tolerance - joint_width+0.2 - joint_tolerance, joint_thickness-0.4]) rotate(a = [0, 90, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/2 - pcb_tolerance - joint_width+0.2- joint_tolerance, pcb_height/3., joint_thickness-0.4]) rotate(a = [90, 0, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/2 - pcb_tolerance - joint_width+0.2- joint_tolerance, -pcb_height/3., joint_thickness-0.4]) rotate(a = [90, 0, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([ pcb_width/2 + pcb_tolerance + joint_width-0.2+joint_tolerance, pcb_height/3., joint_thickness-0.4]) rotate(a = [90, 0, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([ pcb_width/2 + pcb_tolerance + joint_width-0.2+joint_tolerance, -pcb_height/3., joint_thickness-0.4]) rotate(a = [90, 0, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([-pcb_width/2 - pcb_tolerance - joint_width+0.2-joint_tolerance, 0, joint_thickness-0.4]) rotate(a = [90, 0, 0]) cylinder(17, r=0.4, $fn=16, center = true); 
    translate([ pcb_width/2 + pcb_tolerance + joint_width-0.2+joint_tolerance, 0, joint_thickness-0.4]) rotate(a = [90, 0, 0]) cylinder(17, r=0.4, $fn=16, center = true); 


    }
    
    for (i=[0:3]) {
      translate([0, 10-i*65/3., battery_thickness/2.]) cube([pcb_width, 3, battery_thickness], center = true);
    }
    
    translate([-pcb_width/2.+3/2., pcb_height/4., battery_thickness/2.]) cube([3, pcb_height/3., battery_thickness], center = true);
}; 

module large_key(s) {
  translate([0, 0, keypad_thickness/2]) {
    difference() {
      cube([14, 10, keypad_thickness], center = true); 
      cube([11.2,  8, keypad_thickness ], center = true); 
    }
  }; 
  translate([-2.5, -4, 0]) cube([5, 1, keypad_spring_thickness]); 
  translate([0, 0, keypad_thickness/2.]) cube([10,  6, keypad_thickness ], center = true); 
  difference() {
    linear_extrude(height = 2.2, scale = 0.85) square([9.2, 5.2], center = true); 
    //translate([0, 0, 3/2.]) cube([9, 5, 3 ], center = true); 
    translate([0, 0, 2.4]) {
        linear_extrude(height = 0.8) {
            text(s, font = "Liberation Sans:style=Bold", size = 3, halign = "center"        , valign = "center");
        }
    }
  }
}

module small_key(s) {
  translate([0, 0, 0.6/2]) {
    difference() {
      cube([12, 8.6, 0.6], center = true); 
      cube([10,  7.0, 1. ], center = true); 
    }
  }; 
  translate([-2., -3.5, 0]) cube([4, 1, 0.4]); 
  translate([0, 0, 0.6/2.]) cube([9., 5.5, 0.6 ], center = true); 
  difference() {
    linear_extrude(height = 2.2, scale = 0.9) square([8.2, 4.2], 
      center = true); 
    //translate([0, 0, 3/2.]) cube([9, 5, 3 ], center = true); 
    translate([0, 0, 2.2]) {
        linear_extrude(height = 0.8) {
            text(s, font = "Liberation Sans:style=Bold", size = 2.4, halign = "center"        , valign = "center");
        }
    }
  }
}

module large_keypad() {

  labels = [
  "0", "/-/", ".", "+/-", "Ent", 
  "1", "2", "3", "+", "-", 
  "4", "5", "6", "*", "/", 
  "7", "8", "9", "E", "C"
  ]; 

  for (i=[0:4]) {
    for (j=[0:3]) {
      translate([14*(i-2), 10*j-pcb_height/2.+keypad_large_row, 
              pcb_thickness + spacer_thickness]) 
//        large_key(labels[5*j+i]); 
        large_key(""); 
    }
  }

}


module small_keypad() {

  labels = [
  "Erf", "Sqrt", "Pol", "1/x", "Drp", "X-Y", 
  "y^x", "ln", "lg", "sin", "cos", "tan", 
  "", "", "R-G", "M+", "MR", "MS", 
  "F", "G", "Mod", "Unc", "Prc", "On"
  ]; 

  for (i=[0:5]) {
    for (j=[0:3]) {
      translate([11.4*(i-2.5), 7.7*j-pcb_height/2.+keypad_small_row, 
               pcb_thickness + spacer_thickness]) 
//        small_key(labels[6*j+i]); 
        small_key(""); 
    }
  }
  
  // Additional width on left and right
  translate([pcb_width/2.-0.5, -8.6/2.-pcb_height/2.+keypad_small_row, 
               pcb_thickness + spacer_thickness]) 
    cube([0.5, 7.7*4 + 8.6-7.7, 0.6]); 
  
  translate([-pcb_width/2., -8.6/2.-pcb_height/2.+keypad_small_row, 
               pcb_thickness + spacer_thickness]) 
    cube([0.5, 7.7*4 + 8.6-7.7, 0.6]); 
  
}

module keypad() {

  large_keypad(); 
  small_keypad(); 

  // Connection between two keypads
  translate([0., 10*4-pcb_height/2.+4.6, pcb_thickness + spacer_thickness + 0.6/2.]) cube([pcb_width, 2.2, 0.6], center = true); 
}

module large_spacer_element() {
  
    difference() {
      cube([14, 10, spacer_thickness], center = true); 
      cube([11, 7, spacer_thickness], center = true); 
    }
    translate([0, 0, spacer_thickness/2-pusher_thickness/2]) 
//      cube([3.2, 2.6, pusher_thickness], center = true); 
      cylinder(pusher_thickness, r = 1.6, center = true, $fn = 16);
    translate([0, -2.5, spacer_thickness/2-spacer_spring_thickness/2])  
      cube([3.0, 5, spacer_spring_thickness], center = true); 
}

module small_spacer_element() {
  
    difference() {
      cube([13, 8.6, spacer_thickness], center = true); 
      cube([10, 6.5, spacer_thickness], center = true); 
    }
    translate([0, 0, spacer_thickness/2-pusher_thickness/2]) 
//      cube([3.2, 2.6, pusher_thickness], center = true); 
      cylinder(pusher_thickness, r = 1.6, center = true, $fn = 16);
    translate([0, -8.6/4., spacer_thickness/2-spacer_spring_thickness/2])  
      cube([3.0, 8.6/2., spacer_spring_thickness], center = true); 
}

module spacer() {

  for (i=[0:4]) {
    for (j=[0:3]) {
      translate([14*(i-2), 10*j-pcb_height/2.+keypad_large_row, 
              pcb_thickness + spacer_thickness/2.]) 
        large_spacer_element(); 
    }
  }

  for (i=[0:5]) {
    for (j=[0:3]) {
      translate([11.4*(i-2.5), 7.7*j-pcb_height/2.+keypad_small_row, 
               pcb_thickness + spacer_thickness/2.]) 
        small_spacer_element(); 
    }
  }

  translate([0, -18.9, pcb_thickness + spacer_thickness/2.]) 
    cube([pcb_width, 2.2, spacer_thickness], center = true); 
}


// Tests 
//translate([0., 5.,  spacer_thickness/2.]) mirror([0,0,1]) small_spacer_element(); 
//translate([0., -5., 0]) small_key("y^x"); 



// Finally, make all parts
// Comment out if needed

translate([0., 0., 0]) spacer(); 

translate([0., 0., 10]) keypad();   

translate([0., 0., 30]) top_half(); 

translate([0., 0., -10]) mirror([0,0,1]) bottom_half(); 

//cube([1, 1, 1], center = true); // Dummy cube for "mouse ears" in slicer
