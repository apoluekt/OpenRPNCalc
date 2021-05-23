/*
 * sharp.c
 *
 *  Created on: Mar 9, 2021
 *      Author: apolu
 */

#include "stm32l4xx_hal.h"
#include "fonts.h"
#include "sharp.h"

uint8_t buffer[BUFFER_SIZE];

TIM_HandleTypeDef* _htim1;
//TIM_HandleTypeDef* _htim2;
SPI_HandleTypeDef* _hspi1;

void delay_us (uint16_t us)
{
	__HAL_TIM_SET_COUNTER(_htim1,0);  // set the counter value a 0
	while (__HAL_TIM_GET_COUNTER(_htim1) < us);  // wait for the counter to reach the us input in the parameter
}

void sharp_clear() {
	uint8_t b[2] = {0x04, 0x00};
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_SET);
	delay_us(6);
	HAL_SPI_Transmit(_hspi1, b, 2, 100);
	delay_us(2);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET);
	delay_us(2);
}

void sharp_init(TIM_HandleTypeDef* htim1, SPI_HandleTypeDef* hspi1) {
    _htim1 = htim1;
//    _htim2 = htim2;
    _hspi1 = hspi1;

	HAL_TIM_Base_Start(_htim1); // Start microsecond timer

//	HAL_TIM_PWM_Start(_htim2, TIM_CHANNEL_2);  // Start EXPCOMIN PWM signal
//	TIM2->CCR2 = 1000000l;  //  1/16 pulse width for EXPCOMIN

	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4, GPIO_PIN_SET);  // DISP signal to "ON"
	delay_us(10);
	sharp_clear();
}

unsigned char reverse(unsigned char b) {
   b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
   b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
   b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
   return b;
}

void sharp_send_buffer(uint16_t y, uint16_t lines) {
    buffer[0] = 0x01;
    uint16_t size = (2+lines*52);
    for (int j=0; j<lines; j++) {
		if (y+j<=240) buffer[j*52+1] = (uint8_t)(241-y-j);
    }
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_SET);
	delay_us(6);
	HAL_SPI_Transmit(_hspi1, buffer, size, 100);
	delay_us(2);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET);
	delay_us(2);
}

void sharp_string(char* str, FontDef_t *font, uint16_t dx, uint16_t dy) {
	uint8_t width = font->FontWidth;
	uint8_t height = font->FontHeight;
	uint8_t bytes = (width+7)/8;
	const char (*data)[bytes*height] = font->data;
	uint16_t xpos = dx;
	int i=0;
	while (xpos<400) {
        uint8_t c = str[i];
        if(c == 0x00) break;
        uint16_t xaddr = xpos>>3;
        uint16_t xshift = xpos & 0x0007;
        uint16_t jdy52 = dy*52;
        for (uint8_t j=0; j<height; j++) {
        	uint16_t xaddrb = xaddr;
            for (uint16_t b=0; b<bytes; b++) {
                uint16_t l = data[c][bytes*j+b] << xshift;
            	uint8_t* lb = (uint8_t*)(&l);
//                if (xaddr+b<50 && j+dy<BUFFER_LINES) buffer[(j+dy)*52+xaddr+b+2] &= ~(*(lb));
//                if (xaddr+b+1<50 && j+dy<BUFFER_LINES) buffer[(j+dy)*52+xaddr+b+3] &= ~(*(lb+1));
                if (xaddrb<50 && j+dy<BUFFER_LINES) buffer[jdy52 + 51 - xaddrb] &= reverse(~(*(lb)));
                if (xaddrb+1<50 && j+dy<BUFFER_LINES) buffer[jdy52 + 50 - xaddrb] &= reverse(~(*(lb+1)));
                xaddrb++;
            }
        	jdy52 += 52;
        }
        xpos += width;
        i++;
	}
}
