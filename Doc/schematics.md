# Schematics and parts

Rev. 4 uses a single PCB for the MCU and keyboard

<img src="images/schematic.png">

## Notes 

### MCU

* The most recent STM32U385 is used here (256kB RAM, 1MB flash, ultra-low power with only 10 uA/MHz consumption)
* JP1 must be shorted to enter the USB bootloader for the fresh (or bricked) chip. 

### MCU power

* MCU is powered by the internal SMPS supply to ensure maximum power efficiency. The relevant external elements are L2, C17, and C18.
* R3, C15 are needed only if the USB interface is used. Otherwise, VDDUSB can be pulled to ground (?)

### LCD power converter

* This circuit is needed to provide +5V for the LCD. The newer TPS61299 chip is used with only 95 nA quiescent current. The version with "true shutdown" mode is used here (i.e. +5V rail is grounded when 5V_EN signal is low). 

### Flash

* Low-power 8MB chip Macronix MX25R6435FM2IL0 in single SPI mode (faster quad SPI mode is not used). 

### LCD interface

* Standard circuitry from LS027b7DH01 datasheet.
* Note that since the LCD connector is positioned on the PCB side facing the LCD, and the flat cable is bent 180 degrees, we have to use the flat cable connector that has contacts on **top**. The part used here has contacts on both sides, but the most abundant connectors with only bottom contacts won't work! 

### USB interface

* USB-C connector in USB-2.0 mode.
* SBU1 and SBU2 contacts can optionally be connected to the ST-LINK interface lines by installing the bridges R29 and R30 (not populated by default). This should allow for using the [SWD over USB-C](https://hackaday.io/project/192857-swd-over-usb-type-c-new-way-of-programming-boards) programmer and debugger. 

### ST-LINK interface

* 2.5mm pitch connector. Can use either 5V or 3.3V (?) lines from the ST-LINK probe to power the calculator. 

### +3.3V linear regulator

* Simple LDO regulator that produces stabilised +3.3V from either USB or ST-LINK input.

### Coin cell and switch

* The power switch is installed to completely switch the power off without removing the battery. Normally, the MCU is always in the idle (STOP) mode waiting for the external interrupt, so operating the switch in normal operation is not needed. 

### Battery/external power commutation

* A pair of "ideal diodes" which take the power from the source with a higher voltage. The USB_ON signal tells the MCU that external power is connected.
* U5 and U6 are optional. Instead, one can install the bridges R22 and R16 to manually switch the power between the battery and external (USB/ST-LINK) sources. 
* D3, R27 and R28 make a switchable divider to measure the battery voltage when VSENS is pulled low. When VSENS is disconnected (most of the time), there is no current drain. One has to make sure that the MCU is operated at the voltage (VDD) not lower than the battery voltage, otherwise the current will flow via the internal protection diodes in the MCU. 

### Coin cell controller and supercaps buffer

* NBM5100A is the coin cell life booster with supercap buffer. It limits the maximal current drawn from the coin cell to a programmable value (can be as low as 2 mA), with the excess taken from the supercaps during periods of high power consumption. It also provides stabilised voltage to power the STM32 and other circuitry.
* NBM5100A is optional. Instead of installing it, together with the surrounding passive elements, one can install the brige R31 to directly connect the calculator circuit to the coin cell or external power. Possibly, one can also install one of the supercaps and add the bridge R26 (not two supercaps sequentially, due to the absence of balancing). Make sure the supercap can survive 3.3V input voltage in this case. 
* Output voltage for NBM5100A should be set to 3V to make sure that the switchable voltage divider (see above) works correctly. 

### External pull-ups

* 1M pull-ups are used instead of STM32 internal 40k pull-ups to limit the current draw when the keys are pressed.
* It seems that the input pin capacitance and parasitic capacitance of the keyboard traces are high enough that a quick scan of the keyboard matrix is impossible with such high-impedance pull-ups. Therefore, the firmware should use them only when waiting for an external interrupt in the idle mode (waiting for a key press event), but to do the keyboard scan to determine which key was pressed, one has to switch the internal pull-ups in addition. 

### Test pads

* LCD signals and voltages 

### Keyboard matrix

* No diodes are added, so only up to two simultaneous key presses can be registered without ghosting. 

## Parts and datasheets

Electronic components from the KiCAD BOM: 

| Quantity | Value/model | Package | Comment |
|-|-|-|-|
| 1	| [STM32U385RGT6Q](https://www.st.com/en/microcontrollers-microprocessors/stm32u385rg.html) | LQFP64 | Microcontroller | 
| 1	| [MX25R6435FM2IL0](https://www.macronix.com/Lists/Datasheet/Attachments/8868/MX25R6435F,%20Wide%20Range,%2064Mb,%20v1.6.pdf)	| SOP-8L | 8MB flash memory | 
| 1	| [Nexperia NBM5100A](https://www.nexperia.com/product/NBM5100ABQ) | DHVQFN-16 | Coin cell controller | 
| 1	| [TI TPS61299](https://www.ti.com/product/TPS61299)	| SOT-5X3 (DRL) | 5V step-up converter | 
| 1	| [TI TLV73333PDBVR](https://www.ti.com/product/TLV733P/part-details/TLV73333PDBVR) | SOT-23 (DBV0005A) | LDO voltage regulator | 
| 2	| [TI LM66100QDCKRQ1](https://www.ti.com/product/LM66100-Q1/part-details/LM66100QDCKRQ1) | SOT-SC70 (DCK0006A) | Ideal diode | 
| 1	| [TL1014BF160QG](https://www.e-switch.com/wp-content/uploads/2022/06/TL1014.pdf) | | Button switch |
| 49 | [Panasonic EVPBT1C4A000](https://industry.panasonic.com/global/en/products/control/switch/light-touch/number/evpbt1c4a000)	| | Button switch |
| 1	| [Nidec CUS-12TB](https://www.nidec-components.com/us/product/detail/00000195/) | | Slide switch | 
| 1	| [BC-2013](https://www.batteryholders.com/part.php?pn=BC-2013&original=&override=)	| | CR2430 coin cell battery holder |
| 1	| [HARWIN M20-8890545R](https://www.harwin.com/products/M20-8890545R) | | SMT pin header, 5 pins, 2.5mm pitch |
| 1	| [USB4110GFA](https://gct.co/connector/usb4110) | | USB-C connector | 
| 1	| [AMPHENOL F3311A7H121010E200](https://www.amphenol-cs.com/product/f3311a7h121010e200.html) | | Flat cable connector, 10 pins, 0.5mm pitch, top and bottom contacts | 
| 1	| 32768 Hz | 2012 | Quartz resonator | 
| 3	| CDBU0340	| 0603 | Schottky diode | 
| 1	| 1 uH | 0805 | Inductor | 
| 1	| 2.2 uH | 0805 | Inductor | 
| 2	| 4.7 uH | 0805 | Inductor | 
| 1	| 15 uH	| 0805 | Inductor | 
| 9	| 100 nF	| 0603 | Ceramic capacitor |
| 2	| 47 pF	| 0603 | Ceramic capacitor |
| 3	| 10 uF	| 0603 | Ceramic capacitor |
| 4	| 2.2 uF | 0603 | Ceramic capacitor |
| 2	| 1 uF | 0603 | Ceramic capacitor |
|	2 | 100 uF | 0805 | Ceramic capacitor |
| 1	| 560 pF | 0603 | Ceramic capacitor |
| 2	| 0.3F | 4x10mm | Supercapacitor | 
| 5	| 10k	| 0603 | Resistor | 
| 9	| 1M | 0603 | Resistor | 
| 3	| 100k | 0603 | Resistor | 
| 2	| 1k | 0603 | Resistor |
| 2	| 5.1k | 0603 | Resistor |
| 2	| 33 | 0603 | Resistor |
| 1	| 0	| 0603 | Resistor |

Other components

| Quantity | Part |  
| - | - | 
| 1 | Sharp Memory LCD, model [LS027B7DH01](https://www.alldatasheet.com/datasheet-pdf/pdf/433405/SHARP/LS027B7DH01.html) |
| 1 | CR2032 coin cell battery | 
| 6 | M2 x 4mm brass standoff, Round or hex, should tightly fit into 3.4mm holes on the PCB | 
| 14 | M2 x 4mm screw | 
| 4-5 | M3 screw and nut for the keycap soldering jig | 
| 2 | M2 x 1.6mm hex nut |
| 1 | ST-LINK v2 programmer with 2.5mm pitch pin header cable | 
| 1 | USB-C cable | 
