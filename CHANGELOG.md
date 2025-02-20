# Changelog

20/02/2025
  * "Infinite" stack (HP48-like) instead of the fixed 4-element one (HP42-like). Practically, it's now limited to 100 elements,
    outght to be enough for anybody, and can be extended. 
  * Statistical functions (chi2 and mean for now) work with all the elements of the stack. 
  * Small bug fixes in the stack behaviour. 

14/02/2025 
  * New functions: 
    - Chi2, mean and RMS of values in the stack with uncertainties (work only in UNCERT) mode
    - Factorial
  * Keyboard scan fully interrupt-driven (entering STOP even when waiting for key release) and a few bugfixes 
    to improve keyboard response

01/01/2025
  * Working on Rev. 2 of OpenRPNCalc. Changes in firmware, enclosure and PCB design, mostly the same schematics. 
  * Changes in firmware:
    - Improvements in the alignment of the display elements and status bar.
    - Added cursor to highlight input elements (value or uncertainty, mantissa or exponent).
    - Removed the unnecessary delay loop in the initialisation phase.
  * Major change in the enclosure design:
    - The idea is to make an enclosure as a sandwich of PCBs rather than the 3d-printed one
    - More reliable silkscreen labels instead of printed stickers
    - Keyboard with PCB-based keys and pin header "pivots" (preliminary design for now, waiting for the PCBs to arrive)

25/06/2021
  * Added ROT-Up and ROT-Down functions ("F"+"Drop" and "G"+"Drop"): stack rotation in two directions
  * Added uncertainties for Y^X and ROOT(Y, X) functions

21/06/2021 
  * Added Poisson PDF ("F"+"4") and chi-squared tail probability ("F"+"5") functions

19/06/2021
  * Small fixes in schematics to reflect what is actually implemented in hardware. 
  * Put STM32 to STOP2 mode instead of STOP1 during standby. This reduces the current 
    consumed from battery to 2-3 uA with LCD off and 10-12 uA with LCD on
    (was 40 and 55 uA, respectively, with STOP1). 
  * Add new photos of the keyboard. 
  * Add links to datasheets in Doc/schematics.md

02/06/2021
  * Added C(n,k), P(n,k) functions calculated using log(Gamma) formula. 
    No check is done that arguments are positive, integer, etc.
  * Added significance (Nsigma(x), Nsigma(x-y)) functions. Work only in 
    UNCERT context. 

28/05/2021
  * Added relativistic kinematics functions (uncertainties are not implemented yet for them): 
    * Conversion between angle and pseudorapidity (eta <-> theta)
    * Conversion between beta and gamma factors (gamma <-> beta)
    * Center-of-mass momentum for 2-body decay (P(z->xy))
  * Gamma and log Gamma functions. 
  * Conversion between degrees and radians. 
  * Slight reshuffle of function keys. 
  * Update with ST-Link is now activated with "SHIFT+Reset" (instead of "ON+Reset"). 

