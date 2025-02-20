<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/images/photo_calc_iso.jpg?raw=true" width="200" align="left">

# OpenRPNCalc
Open-source and open-hardware scientific RPN calculator

## Introduction

OpenRPNCalc is a scientific calculator based on the STM32 microcontroller. Its source code, schematics, and 3D-printed case design files are released under an open license. 

The hardware is inspired by the SwissMicros [DM42](https://www.swissmicros.com/product/dm42) calculator (which itself mimics the famous HP-42), but designed from scratch. Firmware-wise, however, there is no intention to simulate programmable HP series. Currently, the calculator features: 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/images/photo_calc_front.jpg?raw=true" width="200" align="right">

  * [Reverse Polish notation](https://www.hpmuseum.org/rpn.htm) with 4-element stack. 
  * Double-precision arithmetics. 
  * "Standard" scientific calculator functions (trigonometric, logarithms, exponentiation, square root and power). 
  * Error function (erf) and its inverse (erfinv), Gamma and log(Gamma) functions, number of combinations and permutations, p-values of Poisson, Gaussian and chi-squared distributions. 
  * Fixed, scientific (SCI) and engineering (ENG) display modes (including SI prefixes in ENG mode), variable 3-10 digits precision. 
  * Calculations with uncertainties with error propagation (UNCERT mode). Something that I've never seen in any of the hardware calculators, and very rarely is present in the software ones. 
  * Formulas from relativistic kinematics (centre-of-mass two-body decay momentum, conversion between angle and pseudorapidity, beta and gamma factors). 
  * Low power consumption (measured ~16 uA in standby mode with LCD on and 1-2 uA with LCD off). 

## Hardware overview

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/images/calc_schematic.png?raw=true" width="200" align="right">

The calculator is based on a low-power 32-bit ARM microcontroller [STM32L476](https://www.st.com/en/microcontrollers-microprocessors/stm32l476rg.html) running at 16 MHz. The display is a Sharp memory LCD module [LS027B7DH01](https://www.sharpsde.com/products/displays/model/LS027B7DH01/) (400x240 pixel monochrome). The keyboard uses light-touch tactile switches Panasonic [EVQP0N02B](https://www3.panasonic.biz/ac/e/search_num/index.jsp?c=detail%E2%88%82no=EVQP0N02B) (60g actuation force). All electronics runs off the 3V lithium battery (CR2032) which should be sufficient to provide power for several years of operation. 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/images/pcb_3d_bottom.png?raw=true" width="200" align="left">

In the present design, the front panel and keys are made of PCB with labels printed as silkscreen. The rest of the enclosure (spacer between the main PCB and front panel, and back lid) is 3D printed. All the parts are kept together with six M2 standoffs and 12 flat-head screws. The size of the enclosure is 139x72x9 mm. 

## Contents of the repository

   * [Code](https://github.com/apoluekt/OpenRPNCalc/tree/rev2/Code): STM32 firmware created with STM32Cube IDE
   * [Hardware](https://github.com/apoluekt/OpenRPNCalc/tree/rev2/Hardware/): Schematic (calc_v2.sch) and main PCB layout (calc_v2.kicad_pcb) for KiCAD, keyboard and front panel PCBs. 
   * [Enclosure](https://github.com/apoluekt/OpenRPNCalc/tree/rev2/Enclosure): Python scripts to generate silkscreen labels and PCB outlines, generated files themselves (these are imported to KiCAD to produce PCBs), as well as OpenSCAD and STL files for the 3D-printed spacer and back lid. 
   * [Doc](https://github.com/apoluekt/OpenRPNCalc/tree/rev2/Doc): Documentation and images. 

## Documentation

   * [Schematics](https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/schematics.md)
   * [MCU firmware](https://github.com/apoluekt/OpenRPNCalc/blob/main/Code/README.md)
   * [PCB design](https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/pcb_design.md)
   * [Case and keypad](https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/case_design.md)

## Emulator 

[Online emulator](https://apoluekt.github.io/OpenRPNCalc/Emulator/) based on the original calculator firmware extended with Emscripten and Raylib
