# OpenRPNCalc
Open-source and open-hardware scientific RPN calculator

## Introduction

<img src="Doc/images/photo_front.jpg" width="200" align="right">

OpenRPNCalc is a scientific calculator based on the STM32 microcontroller. Its source code, schematics, and PCB design files are released under an open license. The goal is to develop a hardware platform with the following features: 
  * Reproducible without special tools, using only boards produced by PCB prototyping services
  * A customizable keyboard to accommodate specific needs (such as RPN or algebraic logic, custom functions)
  * Low power consumption and long battery life
  * A high-quality, compact and sturdy enclosure

The hardware is inspired by the [SwissMicros](https://www.swissmicros.com/products) calculators, but is designed from scratch. The calculator features: 

  * [Reverse Polish notation](https://www.hpmuseum.org/rpn.htm) with a large stack (up to 100 elements)
  * Double-precision arithmetic
  * "Standard" scientific calculator functions (trigonometric, logarithms, exponentiation, square root and power)
  * Error function (erf) and its inverse (erfinv), Gamma and log(Gamma) functions, combinations and permutations, p-values for Poisson, Gaussian, and chi-squared distributions
  * Fixed, scientific (SCI) and engineering (ENG) display modes (including SI prefixes in ENG mode), with adjustable precision from 3 to 10 digits
  * Calculations with uncertainties using error propagation (UNCERT mode) - a feature rarely found in software calculators and almost unheard of in hardware calculators
  * Formulas from relativistic kinematics (centre-of-mass two-body decay momentum, conversion between angle and pseudorapidity, beta and gamma factors)
  * Statistical functions: mean (or weighted mean in UNCERT mode), RMS, chi-squared of a series of values (only in UNCERT mode). 
  * 100 memory registers
  * Power consumption: 0.6mA running at 16MHz, 16 uA in standby mode with the LCD on, and 5 uA with the LCD off.
  * Optional HP48 keyboard files, with the aim to run [DB48x](https://48calc.org/) (this is still very much WIP)

## Hardware overview

<img src="Doc/images/schematic.png" width="200" align="left">

The calculator is built around a low-power 32-bit ARM microcontroller, the [STM32U385](https://www.st.com/en/microcontrollers-microprocessors/stm32u385rg.html). The display is a Sharp memory LCD module, the [LS027B7DH01](https://www.sharpsde.com/products/displays/model/LS027B7DH01/) (400x240 pixel monochrome). The keyboard uses light-touch tactile switches, specifically the Panasonic [EVPBT1C4A000](https://industry.panasonic.com/global/en/products/control/switch/light-touch/number/evpbt1c4a000) (50g actuation force). All electronics are powered by a 3V lithium battery (CR2032), which should be sufficient for several years of operation. 

<img src="Doc/images/pcb01.jpg" width="200" align="right">

The enclosure is designed as a stack of multiple PCBs. The front and back panels are aluminium PCBs with a white solder mask and black silkscreen. The keys are also made of PCB, with labels printed as silkscreen. All components are kept together with six M2 standoffs and twelve flat-head screws. The enclosure dimensions are 139 x 73 x 8 mm. 

## Repository contents

   * [Code](Code): STM32 firmware developed using STM32Cube IDE
   * [Hardware](Hardware): Schematic and PCB design files for KiCad, PCB production files
   * [Doc](Doc): Documentation and images
   * [Emulator](Emulator): Online emulator files to be deployed to github-pages or other web hosting

## Documentation

   * [Schematics and parts](Doc/schematics.md) of the PCBs and the list of electronic components and other parts with links to datasheets
   * [PCB design](Doc/pcb_design.md): images of the PCB layers and their functions
   * [Case and keyboard assembly](Doc/assembly.md): photos of the insides of the calculator, assembly instructions
   * [Firmware](Code/README.md): code structure and flashing instructions

## Emulator 

[Online emulator](https://apoluekt.github.io/OpenRPNCalc/Emulator/), based on the original calculator firmware extended with Emscripten and Raylib
