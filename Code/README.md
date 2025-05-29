# OpenRPNCalc firmware

The code is developed with STM32CubeIDE (specifically, version 1.17 under Linux). 

To create the binary file to flash the STM32 chip, go to "Project/Properties/C/C++ Build/Settings" and under "MCU/MPU Post build outputs" check "Convert to a binary file (-O binary)". Then build the project ("Project/Build all") which will produce the file "Debug/OpenRPNCalc.bin". This is the binary that needs to be flashed. 

STM32U3 series is not yet supported by the `st-link` tools in Linux. Use proprietary STM32CubeProgrammer. 