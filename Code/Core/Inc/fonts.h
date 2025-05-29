#ifndef FONTS_H
#define FONTS_H 120

/* C++ detection */
#ifdef __cplusplus
extern C {
#endif

#include "stm32u3xx_hal.h"
#include "string.h"

typedef struct {
	uint8_t FontWidth;    /*!< Font width in pixels */
	uint8_t FontHeight;   /*!< Font height in pixels */
	const void *data;    /*!< Pointer to data font data array */
} FontDef_t;

extern FontDef_t font_6x8;

extern FontDef_t font_7x12b;

extern FontDef_t font_12x20;

extern FontDef_t font_16x26;

extern FontDef_t font_24x40;

/* C++ detection */
#ifdef __cplusplus
}
#endif

#endif
