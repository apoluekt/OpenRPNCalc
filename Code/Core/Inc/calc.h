#ifndef CALC_H
#define CALC_H 100

/* C++ detection */
#ifdef __cplusplus
extern C {
#endif

void calc_init(void);

void calc_refresh(void);

void clear_shift(void);

int calc_on_key(int c);

void report_voltage(uint16_t v);

#endif
