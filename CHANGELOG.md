# Changelog

## 20/05/2025.
  * Bug fixes to Rev 4: 
    * Spacer2: Adjusted key soldering jig; increased gap between the battery holder and the spacer
    * EnterStab: Adjusted hole positions
    * Main: Corrected footprints for TPS61299 and diodes
  * Added HP48 keyboard layout in addition to the custom one: 
    * PCBs in Hardware/PCBs with _hp48 suffix
    * production files in Hardware/production with _hp48 suffix

## 27/04/2025. Revision 4
  * Hardware modifications in Rev 4:
    * [STM32U385](https://www.st.com/en/microcontrollers-microprocessors/stm32u385rg.html) processor
    * Added USB interface (USB-C connector) with optional support of [SWD over USB-C](https://hackaday.io/project/192857-swd-over-usb-type-c-new-way-of-programming-boards)
    * Added external flash ([Macronix MX25R6435F](https://www.macronix.com/Lists/Datasheet/Attachments/8868/MX25R6435F,%20Wide%20Range,%2064Mb,%20v1.6.pdf), 8Mbytes)
    * Added coin cell booster with supercaps buffer ([Nexperia NBM5100A](https://www.nexperia.com/product/NBM5100ABQ) and 2x0.3F caps)
    * New 5V booster for LCD ([TPS61299](https://www.ti.com/product/TPS61299))
    * External/battery voltage commutation with a pair of "ideal diodes" ([LM66100-Q1](https://www.ti.com/product/LM66100-Q1))
    * Keyboard layout modifications: additional row of function keys, wide "Enter"
    * Different model of tactile switches (Panasonic EVP-BT1C4A000) to avoid 3D-printed pads for the keys
    * CR2032 coin cell by default

## 28/03/2025
  * Firmware: 
    * Rudimentary programming capability: record up to 100 operations and run the recorded sequence either all at once or step-by-step. 
      No loops or branching.
    * Increase delays in keyboard scan for stability with high-impedance pull-ups
    * Speed up LCD output
    * Independent setting of precision (number of significant digits) for NORMAL and UNCERT contexts
  * Hardware: 
    * Updated front panel labels to reflect the firmware update (added programming functions).

## 07/03/2025
  * Hardware: Rev. 3 of the schematics and enclosure. 
  * Firmware:
    * 100 memory registers accessible via F-RCL and F-STO functions, with the address of the memory register passed in the X register of the stack
    * Changes for Rev. 3 of hardware (upright LCD screen instead of upside-down in the old revisions; external pull-ups for key matrix)
    * Enscripten/raylib code for the online emulator

## 20/02/2025
  * "Infinite" stack (HP48-like) instead of the fixed 4-element one (HP42-like). Practically, it's now limited to 100 elements,
    outght to be enough for anybody, and can be extended. 
  * Statistical functions (chi2 and mean for now) work with all the elements of the stack. 
  * Small bug fixes in the stack behaviour. 

## 14/02/2025 
  * New functions: 
    - Chi2, mean and RMS of values in the stack with uncertainties (work only in UNCERT) mode
    - Factorial
  * Keyboard scan fully interrupt-driven (entering STOP even when waiting for key release) and a few bugfixes 
    to improve keyboard response

## 01/01/2025
  * Working on Rev. 2 of OpenRPNCalc. Changes in firmware, enclosure and PCB design, mostly the same schematics. 
  * Changes in firmware:
    - Improvements in the alignment of the display elements and status bar.
    - Added cursor to highlight input elements (value or uncertainty, mantissa or exponent).
    - Removed the unnecessary delay loop in the initialisation phase.
  * Major change in the enclosure design:
    - The idea is to make an enclosure as a sandwich of PCBs rather than the 3d-printed one
    - More reliable silkscreen labels instead of printed stickers
    - Keyboard with PCB-based keys and pin header "pivots" (preliminary design for now, waiting for the PCBs to arrive)

## 25/06/2021
  * Added ROT-Up and ROT-Down functions ("F"+"Drop" and "G"+"Drop"): stack rotation in two directions
  * Added uncertainties for Y^X and ROOT(Y, X) functions

## 21/06/2021 
  * Added Poisson PDF ("F"+"4") and chi-squared tail probability ("F"+"5") functions

## 19/06/2021
  * Small fixes in schematics to reflect what is actually implemented in hardware. 
  * Put STM32 to STOP2 mode instead of STOP1 during standby. This reduces the current 
    consumed from battery to 2-3 uA with LCD off and 10-12 uA with LCD on
    (was 40 and 55 uA, respectively, with STOP1). 
  * Add new photos of the keyboard. 
  * Add links to datasheets in Doc/schematics.md

## 02/06/2021
  * Added C(n,k), P(n,k) functions calculated using log(Gamma) formula. 
    No check is done that arguments are positive, integer, etc.
  * Added significance (Nsigma(x), Nsigma(x-y)) functions. Work only in 
    UNCERT context. 

## 28/05/2021
  * Added relativistic kinematics functions (uncertainties are not implemented yet for them): 
    * Conversion between angle and pseudorapidity (eta <-> theta)
    * Conversion between beta and gamma factors (gamma <-> beta)
    * Center-of-mass momentum for 2-body decay (P(z->xy))
  * Gamma and log Gamma functions. 
  * Conversion between degrees and radians. 
  * Slight reshuffle of function keys. 
  * Update with ST-Link is now activated with "SHIFT+Reset" (instead of "ON+Reset"). 

