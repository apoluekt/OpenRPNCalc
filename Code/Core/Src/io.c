#include "stm32u3xx_hal.h"
#include "io.h"

void UpdateSysTick(uint32_t new_HCLK_freq) {
    HAL_SYSTICK_Config(new_HCLK_freq / 1000);  // Ensure 1 ms SysTick tick
}

uint16_t battery_voltage() {
	if (HAL_ADC_Start(&hadc1) == HAL_OK) {
		if (HAL_ADC_PollForConversion(&hadc1,100) == HAL_OK) {
			uint16_t ADC_measure_VREF = HAL_ADC_GetValue(&hadc1);
			//uint16_t ADC_cal_value = (*VREFINT_CAL_ADDR);
			//uint16_t VREF_VOLTAGE = (3000l*ADC_cal_value)/ADC_measure_VREF;
			//return VREF_VOLTAGE;
			return ADC_measure_VREF;
		}
	}
	return 1;
}
