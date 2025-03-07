<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev3/Doc/images/photo_34.jpg?raw=true" width="200" align="left">

# OpenRPNCalc
Open-source and open-hardware scientific RPN calculator

## Introduction

OpenRPNCalc is a scientific calculator based on the STM32 microcontroller. Its source code, schematics, and 3D-printed case design files are released under an open license. 

The hardware is inspired by the SwissMicros [DM42](https://www.swissmicros.com/product/dm42) calculator (which itself mimics the famous HP-42) but is designed from scratch. Firmware-wise, however, there is no intention to simulate programmable HP series. Currently, the calculator features: 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev3/Doc/images/photo_front.jpg?raw=true" width="200" align="right">

  * [Reverse Polish notation](https://www.hpmuseum.org/rpn.htm) with large (up to 100 elements) stack
  * Double-precision arithmetics
  * "Standard" scientific calculator functions (trigonometric, logarithms, exponentiation, square root and power)
  * Error function (erf) and its inverse (erfinv), Gamma and log(Gamma) functions, number of combinations and permutations, p-values of Poisson, Gaussian and chi-squared distributions
  * Fixed, scientific (SCI) and engineering (ENG) display modes (including SI prefixes in ENG mode), variable 3-10 digits precision
  * Calculations with uncertainties with error propagation (UNCERT mode). Something that I've never seen in any of the hardware calculators and is very rarely present in the software ones
  * Formulas from relativistic kinematics (centre-of-mass two-body decay momentum, conversion between angle and pseudorapidity, beta and gamma factors)
  * 100 memory registers
  * Low power consumption (measured ~16 uA in standby mode with LCD on and 1-2 uA with LCD off)

## Hardware overview

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev3/Doc/images/mcu_schematic.png" width="200" align="right">

The calculator is based on a low-power 32-bit ARM microcontroller [STM32L476](https://www.st.com/en/microcontrollers-microprocessors/stm32l476rg.html) running at 16 MHz. The display is a Sharp memory LCD module [LS027B7DH01](https://www.sharpsde.com/products/displays/model/LS027B7DH01/) (400x240 pixel monochrome). The keyboard uses light-touch tactile switches Panasonic [EVQP0N02B](https://www3.panasonic.biz/ac/e/search_num/index.jsp?c=detail%E2%88%82no=EVQP0N02B) (60g actuation force). All electronics runs off the 3V lithium battery (CR2032), which should be sufficient to provide power for several years of operation. 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/rev3/Doc/images/photo_open.jpg?raw=true" width="200" align="left">

The enclosure is designed as a sandwich of several PCBs. The front and back panels are aluminium PCBs with white soldermask and black silkscreen. The keys are also made of PCB and have labels printed as silkscreen. All the parts are kept together with six M2 standoffs and 12 flat-head screws. The size of the enclosure is 135 x 73 x 7 mm. 

## Contents of the repository

   * [Code](https://github.com/apoluekt/OpenRPNCalc/tree/rev3/Code): STM32 firmware created with STM32Cube IDE
   * [Hardware](https://github.com/apoluekt/OpenRPNCalc/tree/rev3/Hardware/): Schematic and PCB design files for KiCAD
   * [Doc](https://github.com/apoluekt/OpenRPNCalc/tree/rev3/Doc): Documentation and images 

## Documentation

   * [Schematics](https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/schematics.md)
   * [MCU firmware](https://github.com/apoluekt/OpenRPNCalc/blob/main/Code/README.md)
   * [PCB design](https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/pcb_design.md)
   * [Case and keypad](https://github.com/apoluekt/OpenRPNCalc/blob/rev2/Doc/case_design.md)
