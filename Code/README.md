# OpenRPNCalc firmware

The core is developed with STM32CubeIDE (to be specific, version 1.17 under Linux). 

To create the binary file to flash STM32 chip, go to "Project/Properties/C/C++ Build/Settings" and under "MCU/MPU Post build outputs" check "Convert to binary file (-O binary)". Then build the project ("Project/Build all") which will produce the file "Debug/OpenRPNCalc.bin". This is the binary that needs to be flashed. 

To flash STM32 chip, one needs a ST-LINK V2 USB dongle and the software programmer such as stlink-tools under Linux (can be installed via `apt install stlink-tools` under Ubuntu). To flash the file, do
```
$ st-flash --connect-under-reset write OpenRPNCalc.bin 0x08000000
```

Note: at least my cheap ST-LINK dongle cannot do "connect under reset". In that case, the following procedure helps: 
   * Press the RESET button on the calculator and hold it. 
   * Run the `st-flash` command above, which will fail.
   * Release the RESET button.
   * Run the `st-flash` command again, which will work normally this time. 
