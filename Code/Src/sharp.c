/*
 * sharp.c
 *
 * Functions to work with Sharp Memory LCD of type LS027B7DH01.
 *
 * The display in OpenRPNCalc is installed upside down for convenience of PCB routing,
 * so this has to be taken into account in the firmware.
 *
 *  Created on: Mar 9, 2021
 *      Author: apolu
 */

#include "stm32l4xx_hal.h"
#include "fonts.h"
#include "sharp.h"

/* String buffer (maximum 64 pixels high) */
uint8_t buffer[BUFFER_SIZE];

TIM_HandleTypeDef* _htim1;
//TIM_HandleTypeDef* _htim2;
SPI_HandleTypeDef* _hspi1;

/* Microsecond delay */
void delay_us (uint16_t us)
{
	__HAL_TIM_SET_COUNTER(_htim1,0);  // set the counter value a 0
	while (__HAL_TIM_GET_COUNTER(_htim1) < us);  // wait for the counter to reach the us input in the parameter
}

/* Clear display */
void sharp_clear() {
	uint8_t b[2] = {0x04, 0x00};
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_SET);
	delay_us(6);
	HAL_SPI_Transmit(_hspi1, b, 2, 100);
	delay_us(2);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET);
	delay_us(2);
}

/* Initialise display: start timers, send "ON" signal, and call clear function.  */
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

/* Auxiliary function to reverse the bits in 8-bit word.
 * Useful to deal with upside-down display. */
unsigned char reverse(unsigned char b) {
   b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
   b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
   b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
   return b;
}

/* Send the string buffer content to the display via SPI interface.
 *   y : vertical coordinate of the top pixel of the string (0...239)
 *   lines : number of lines to send from the buffer (up to 64)
 */
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

/* Draw string in the string buffer (without sending it to screen).
 *   str : string to be drawn
 *   font: pointer to the font structure
 *   dx: x coordinate of the start of the string
 *   dy: y coordinate of the start of the string in the buffer
 *       (keep in mind that the buffer itself can be drawn at the arbitrary
 *       location later in the call to sharp_send_buffer(). )
 *   */
void sharp_string(char* str, FontDef_t *font, uint16_t dx, uint16_t dy) {
	uint8_t width = font->FontWidth;
	uint8_t height = font->FontHeight;
	uint8_t bytes = (width+7)/8;
	const char (*data)[bytes*height] = font->data;
	uint16_t xpos = dx;
	uint16_t dy52 = dy*52;
	int i=0;
	while (xpos<400) {
        uint8_t c = str[i];
        if(c == 0x00) break;
        const char *cdata = data[c];
        uint16_t xaddr = xpos>>3;
        uint16_t xshift = xpos & 0x0007;
        uint16_t jdy52 = dy52;
    	uint16_t faddr = 0;
        for (uint8_t j=0; j<height; j++) {
        	if (j+dy >= BUFFER_LINES) break;
            uint16_t xaddrb = jdy52 + 50 - xaddr;
        	for (uint16_t b=0; b<bytes; b++) {
        		uint16_t l = ~(cdata[faddr] << xshift);
        		uint8_t* lb = (uint8_t*)(&l);
            	if (xaddrb>jdy52) buffer[xaddrb + 1] &= reverse(*(lb));
            	if (xaddrb>jdy52+1) buffer[xaddrb] &= reverse(*(lb+1));
            	xaddrb--;
            	faddr++;
        	}
        	jdy52 += 52;
        }
        xpos += width;
        i++;
	}
}

// Draws a filled rectangle in a monochrome buffer.
// Parameters:
// - dx: X-coordinate of the top-left corner of the rectangle.
// - dy: Y-coordinate of the top-left corner of the rectangle.
// - width: Width of the rectangle in pixels.
// - height: Height of the rectangle in pixels.
// - color: 1 for white, 0 for black.
void sharp_filled_rectangle(size_t dx, size_t dy, size_t width, size_t height,
                           uint8_t color) {
    int x = BUFFER_WIDTH-1-dx-width;
    int y = dy;
	if (width == 0 || height == 0) return;

    // Limit the rectangle to the buffer boundaries
    size_t max_x = x + width > BUFFER_WIDTH ? BUFFER_WIDTH : x + width;
    size_t max_y = y + height > BUFFER_LINES ? BUFFER_LINES : y + height;

    size_t start_offset = x % 8;
    size_t end_offset = max_x % 8;

    for (size_t row = y; row < max_y; row++) {
        size_t start_byte = row*52 + x / 8 + 2;
        size_t end_byte = row*52 + (max_x - 1) / 8 + 2;

        // Handle the first partial byte if necessary
        if (start_byte == end_byte) {
            uint8_t mask = reverse((0xFF >> start_offset) & (0xFF << (8 - end_offset)));
            if (color) {
                buffer[start_byte] |= mask;
            } else {
                buffer[start_byte] &= ~mask;
            }
        } else {
            if (start_offset != 0) {
                uint8_t start_mask = reverse(0xFF >> start_offset);
                if (color) {
                    buffer[start_byte] |= start_mask;
                } else {
                    buffer[start_byte] &= ~start_mask;
                }
                start_byte++;
            }

            // Fill whole bytes in between
            for (size_t byte = start_byte; byte < end_byte; byte++) {
                buffer[byte] = color ? 0xFF : 0x00;
            }

            // Handle the last partial byte if necessary
            if (end_offset != 0) {
                uint8_t end_mask = reverse(0xFF << (8 - end_offset));
                if (color) {
                    buffer[end_byte] |= end_mask;
                } else {
                    buffer[end_byte] &= ~end_mask;
                }
            }
        }
    }
}
