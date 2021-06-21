# Changelog

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

