#ifndef IO_H
#define IO_H 100

/* C++ detection */
#ifdef __cplusplus
extern C {
#endif

#include "stm32u3xx_hal.h"

extern ADC_HandleTypeDef hadc1;

uint16_t battery_voltage(void);

#endif
