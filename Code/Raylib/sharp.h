/*
 * sharp.h
 *
 *  Created on: Mar 9, 2021
 *      Author: apolu
 */

#ifndef INC_SHARP_H_
#define INC_SHARP_H_

#include "fonts.h"
#include <stdint.h>

#define BUFFER_WIDTH 400
#define BUFFER_LINES 64
#define BUFFER_SIZE (3+BUFFER_LINES*52)

extern uint8_t buffer[BUFFER_SIZE];

void draw_screen(int x, int y); 

void sharp_clear(void);

void sharp_clear_buffer(uint16_t lines, unsigned char value);

void sharp_invert_buffer(uint16_t lines);

void sharp_send_buffer(uint16_t y, uint16_t size);

void sharp_string(char* str, FontDef_t *font, uint16_t dx, uint16_t dy);

void sharp_string_fast_16x26(char* str, uint8_t dx, uint8_t dy)

void sharp_filled_rectangle(size_t x, size_t y, size_t width, size_t height, uint8_t color);

void sharp_test_font(FontDef_t *font, char start_symbol);

#endif /* INC_SHARP_H_ */
