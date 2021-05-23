/*
 * sharp.h
 *
 *  Created on: Mar 9, 2021
 *      Author: apolu
 */

#ifndef INC_SHARP_H_
#define INC_SHARP_H_

#include "stm32l4xx_hal.h"
#include "fonts.h"

#define BUFFER_LINES 64
#define BUFFER_SIZE (2+BUFFER_LINES*52)

extern uint8_t buffer[BUFFER_SIZE];

void delay_us (uint16_t us);

void sharp_clear(void);

void sharp_init(TIM_HandleTypeDef* htim1, SPI_HandleTypeDef* hspi1);

void sharp_send_buffer(uint16_t y, uint16_t size);

void sharp_string(char* str, FontDef_t *font, uint16_t dx, uint16_t dy);

#endif /* INC_SHARP_H_ */
