# Design of enclosure and keypad

The case and keyboard is made of four 3D printed parts (top and bottom parts of the case, keypad and switch spacer). 
The two parts of the case are held together by simple snap fit joints, no screws are needed. 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/case_model.png" width="500">

I've printed the encosure with Creality Ender 3 V2 printer using PETG plastic. Contrary to what's written in many websites, 
I've had no issues with PETG not sticking or sticking too strongly to the heated bed. 
My settings were: 235 C extruder, 80 C bed temp (85 C for the 1st layer). 

The top and bottom parts of the enclosure were printed without raft, directly on the glass bed, 
which made the nice and smooth surface. I've made a 4mm brim around them however, because I've had an issue with warping. 

The keypad and spacer were printed with a 4 layers, 4mm width raft, and I had to add dummy 1x1x1 mm cubes 
at the edges to simulate "mouse ears" to avoid warping (Cura slicer does not have "mouse ears" option). 
Since both parts are rather thin (the spacer has 0.2 mm, only one-layer-thick, springs), 
detaching them from the raft is tricky, but doable with a thin knife. 

I had an issue that the X and Y axes of my printer were not exactly perpendicular (about 1/2 degree off), 
which resulted in the top and bottom halves to be not exactly rectangular. 
And since the top was printed upside down, once the enclosure is assembled, it caused it to be bent in a propeller-like shape. 
I had to adjust the frame of my printer really well to make the case perfectly rectangular. 

Photos of the completed case are below: 

## Top part
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/case_top_inside.jpg" width="500">
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/case_top_outside.jpg" width="500">

## Bottom part
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/case_bottom_inside.jpg" width="500">
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/case_bottom_outside.jpg" width="500">

## Keypad spacer
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/spacer_back.jpg" width="500">
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/spacer_front.jpg" width="500">
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/pcb_spacer.jpg" width="500">

## Keypad
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/keypad_back.jpg" width="500">
<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/keypad_front.jpg" width="500">

