<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/calc_stickers_iso.jpg" width="200" align="left">

# OpenRPNCalc
Open-source and open-hardware scientific RPN calculator

## Introduction

OpenRPNCalc is a scientific calculator based on STM32 microcontroller. Its source code, schematics and 3D-printed case design files are released under open license. 

The hardware is inspired by the SwissMicros [DM42](https://www.swissmicros.com/product/dm42) calculator, but designed from scratch. Firmware-wise, however, there is no intention to simulate programmable HP series. Currently, the calulator features: 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/calc_stickers_face.jpg" width="200" align="right">

  * Reverse Polish notation with 4-element stack. 
  * Double-precision arithmetics. 
  * "Standard" scientific calculator functions (trigonometric, logarighms, exponentiation, square root and power). 
  * Error function (erf) and its inverse (erfinv). 
  * Fixed, scientific (SCI) and engineering (ENG) display modes (including SI prefixes in ENG mode), variable 3-10 digits precision. 
  * Calculations with uncertainties (UNCERT mode). 
  * Low power consumption (40-50 uA in standby mode from 3V CR2032 battery). 

## Hardware overview

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Hardware/Schematic/calc_schematic.png" width="200" align="right">

The calculator is based on low-power 32-bit ARM microcontroller [STM32L476](https://www.st.com/en/microcontrollers-microprocessors/stm32l476rg.html) running at 8 MHz. The display is Sharp memory LCD module [LS027B7DH01](https://www.sharpsde.com/products/displays/model/LS027B7DH01/) (400x240 pixel monochrome). Keyboard uses light-touch tactile switches Panasonic [EVQQ2B01W](https://www3.panasonic.biz/ac/e/search_num/index.jsp?c=detail&part_no=EVQQ2B01W) (50g actuation force). All electronics runs off the 3V lithium battery (CR2032) that should be sufficient to provide power for around one year of operation. 

<img src="https://github.com/apoluekt/OpenRPNCalc/blob/main/Doc/Img/case_model.png" width="200" align="left">

The case and keyboard is made of four 3D printed parts (top and bottom parts of the case, keypad and switch spacer). The two parts of the case are held together by simple snap fit joints, no screws are needed. 

## Contents of the repository

   * [Code](https://github.com/apoluekt/OpenRPNCalc/tree/main/Code): STM32 firmware created with STM32Cube IDE
   * [Hardware/Schematic](https://github.com/apoluekt/OpenRPNCalc/tree/main/Hardware/Schematic): Schematic (calc.sch) and PCB layout (calc.kicad_pcb) for KiCAD, Gerber files for PCB production. 
   * [Hardware/Case](https://github.com/apoluekt/OpenRPNCalc/tree/main/Hardware/Case): 3D models for the enclosure and keypad in OpenSCAD (OpenRPNCalc.scad
), STL files for 3D printing, python script and PDF file for printed keyboard sticker. 
   * [Doc](https://github.com/apoluekt/OpenRPNCalc/tree/main/Doc): Documentation and images. 
