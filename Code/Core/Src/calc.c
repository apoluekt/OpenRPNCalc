#include <stdio.h>
#include <math.h>

#include "sharp.h"
#include "fonts.h"
#include "func.h"
#include "io.h"

#define MAX_STACK_SIZE 99
#define MAX_MEMORY_SIZE 99
#define MAX_PROGRAM_SIZE 99

int stack_size;
int program_size;

double stack[MAX_STACK_SIZE]; // Stack values {X, Y, Z, T}
double lastx;               // Last X value
int error_flag;             // Error flag: 1 if error occurred as a result of last operation

double stack2[MAX_STACK_SIZE]; // Stack for ERRORs in UNCERT context
double lastx2;              // Last X ERROR in UNCERT context

double variables[MAX_MEMORY_SIZE];      // Storage space for variables
double variables2[MAX_MEMORY_SIZE];     // Storage space for variable errors

uint16_t program[MAX_PROGRAM_SIZE];     // Program storage space

int trigmode;     // Trigonometric mode: 0-DEG, 1-RAD
int dispmode;     // Display mode: 0-NORM, 1-SCI, 2-ENG
double trigconv;  // Trigonometric conversion constant, 1 for RAD, (pi/180.) for DEG
int shift;
int context;           // Context: 0-NORMAL, 1-UNCERT
int precision;         // Precision in NORMAL context
int precision_uncert;  // Precision in UNCERT context
int input_uncert;      // Input mode in UNCERT context: 0-VALUE, 1-ERROR
int program_entry;     // If 1, program is being recorded
int program_step;      // If >0, program is being executed step-by-step
//uint16_t voltage;      // Battery voltage in mV
uint16_t draw_flags;   // Bitmask of flags for draw function calls after the operation is completed

// Table of maximal mantissa values for different precisions
uint64_t max_mantissa[10] = {
		9LL,
		99LL,
		999LL,
		9999LL,
		99999LL,
		999999LL,
		9999999LL,
		99999999LL,
		999999999LL,
		9999999999LL
};

#define CONTEXT_REAL 0
#define CONTEXT_UNCERT 1
#define CONTEXT_COMPLEX 2
#define CONTEXT_INTEGER 3

#define BOTTOM_YPOS 190
#define LINE_INTERVAL 54

#define DRAW_STATUS 0x0001
#define DRAW_STACK 0x0002
#define DRAW_INPUT 0x0004
#define DRAW_ERROR 0x0008
#define DRAW_CURSOR 0x0010

#define OPMODE_MASK 0xFF00
#define OPMODE_1TO1 0x1000
#define OPMODE_2TO1 0x2000
#define OPMODE_2TO2 0x3000
#define OPMODE_CONST 0x4000
#define OPMODE_ENTER 0x5000
#define OPMODE_STACK 0x6000
#define OPMODE_RCL 0x7000
#define OPMODE_STO 0x7100
#define OPMODE_MPLUS 0x7200
#define OPMODE_MMINUS 0x7300
#define OPMODE_RCLX 0x7400
#define OPMODE_STOX 0x7500
#define OPMODE_3TO1 0x8000
#define OPMODE_STAT 0x9000
#define OPMODE_PROG 0xA000
#define OPMODE_TEST 0xFF00

#define OP_ENTER_1 0x5001
#define OP_ENTER_2 0x5002
#define OP_ENTER_3 0x5003
#define OP_ENTER_4 0x5004
#define OP_ENTER_5 0x5005
#define OP_ENTER_6 0x5006
#define OP_ENTER_7 0x5007
#define OP_ENTER_8 0x5008
#define OP_ENTER_9 0x5009
#define OP_ENTER_0 0x5000
#define OP_ENTER_DECPOINT 0x500A
#define OP_ENTER_SIGN 0x500B
#define OP_ENTER_EXP 0x500C
#define OP_ENTER_BACKSPACE 0x500D
#define OP_ENTER_UNCERT 0x500E
#define OP_ENTER 0x500F

#define OP_DROP 0x6001
#define OP_SWAP 0x6002
#define OP_LASTX 0x6003
#define OP_CLEAR_STACK 0x6004
#define OP_ROTUP 0x6007
#define OP_ROTDOWN 0x6008
#define OP_CLEAR_MEM 0x6009

#define OP_NOP 0x0000

#define OP_PLUS 0x2001
#define OP_MINUS 0x2002
#define OP_MULT 0x2003
#define OP_DIV 0x2004
#define OP_POW 0x2008
#define OP_ROOTX 0x2013
#define OP_CYX 0x2014
#define OP_PYX 0x2015
#define OP_SIGNIF_XY 0x2016
#define OP_POISSON 0x2017
#define OP_CHI2_PROB 0x2018

#define OP_INV 0x1005
#define OP_SQR 0x1006
#define OP_SQRT 0x1007
#define OP_LN 0x1009
#define OP_LG 0x100A
#define OP_EXP 0x100B
#define OP_POW10 0x100C
#define OP_SIN 0x100D
#define OP_COS 0x100E
#define OP_TAN 0x100F
#define OP_ASIN 0x1010
#define OP_ACOS 0x1011
#define OP_ATAN 0x1012
#define OP_ERF 0x1014
#define OP_ERFINV 0x1015
#define OP_GAMMA 0x1016
#define OP_LOGGAMMA 0x1017
#define OP_GAMMABETA 0x1018
#define OP_BETAGAMMA 0x1019
#define OP_ETATHETA 0x101A
#define OP_THETAETA 0x101B
#define OP_SIGNIF_X 0x101C
#define OP_GAUSS_PVALUE 0x101D
#define OP_FACTORIAL 0x101E

#define OP_POLAR 0x3001
#define OP_DESCARTES 0x3002

#define OP_CONST_PI 0x4013
#define OP_CONST_E 0x4014
#define OP_CONST_PLANCK 0x4015
#define OP_CONST_PLANCKC 0x4016
#define OP_CONST_NA 0x4017
#define OP_CONST_K 0x4018
#define OP_CONST_C 0x4019

#define OP_PZXY 0x8001

#define OP_STAT_MEAN 0x9001
#define OP_STAT_CHI2 0x9002

#define OP_PROG 0xA001
#define OP_RUN 0xA002
#define OP_STEP 0xA003
#define OP_REWIND 0xA004

#define OP_TEST_1 0xFF01
#define OP_TEST_2 0xFF02
#define OP_TEST_3 0xFF03
#define OP_TEST_4 0xFF04
#define OP_TEST_5 0xFF05
#define OP_TEST_6 0xFF06
#define OP_TEST_7 0xFF07
#define OP_TEST_8 0xFF08
#define OP_TEST_9 0xFF09

// Input structure typedef
typedef struct {
	char mantissa[12];   // Mantissa digits array
	char sign;           // Sign: 0 for "+", 1 for "-"
	char exponent[3];    // Exponent digits array
	char expsign;        // Sign of the exponent: 0 for "+", 1 for "-"
	char started;        // 1 if input mode is active
	char replace_x;      // 1 if "ENTER" or "C" key was just pressed
	// (such that we need to replace the current X value by the new number)
	char expentry;       // 1 if exponent is being entered
	int8_t point;        // Decimal point position
	int8_t mpos;         // Number of mantissa digits entered
} t_input;

t_input input; // Input structure

/*
void report_voltage(uint16_t v) {
	voltage = v;
}
*/

// Clear stack and error flag
void clear_stack() {
	stack[0] = 0.;
	stack2[0] = 0.;
	lastx = 0.;
	lastx2 = 0.;
	error_flag = 0;
	stack_size = 0;
}

void clear_variables() {
	for (uint16_t i=0; i<MAX_MEMORY_SIZE; i++) {
		variables[i] = 0;
		variables2[i] = 0;
	}
}

// Clear input structure
void clear_input() {
	input.mpos = 0;
	input.sign = 0;
	input.point = 0;
	input.started = 0;
	input.replace_x = 0;
	input.expentry = 0;
	input.exponent[0] = 0;
	input.exponent[1] = 0;
	input.exponent[2] = 0;
	input.expsign = 0;
}

// Push the number and error to stack
void stack_push(double num, double err) {
	if (stack_size < MAX_STACK_SIZE) stack_size++;
	for (int i=stack_size-1; i>0; i--) {
		stack[i] = stack[i-1];
		stack2[i] = stack2[i-1];
	}
	stack[0] = num;
	stack2[0] = err;
}

// Drop the value from stack (T register is copied, X is lost)
void stack_drop() {
	if (stack_size>0) {
		stack_size--;
		for (int i=0; i<stack_size; i++) {
			stack[i] = stack[i+1];
			stack2[i] = stack2[i+1];
		}
	}
}

// Rotate stack "upwards" (X->Y, Y->Z, Z->T, T->X)
void stack_rotate_up() {
	double tmp = stack[stack_size-1];
	double tmp2 = stack2[stack_size-1];

	for (int i=stack_size-1; i>0; i--) {
		stack[i] = stack[i-1];
		stack2[i] = stack2[i-1];
	}
	stack[0] = tmp;
	stack2[0] = tmp2;
}

// Rotate stack "downwards" (Y->X, Z->Y, T->Z, X->T)
void stack_rotate_down() {
	double tmp = stack[0];
	double tmp2 = stack2[0];

	for (int i=0; i<stack_size-1; i++) {
		stack[i] = stack[i+1];
		stack2[i] = stack2[i+1];
	}
	stack[stack_size-1] = tmp;
	stack2[stack_size-1] = tmp2;
}

// Set the trigconv constant depending on current trigonometric mode
void set_trigconv() {
	if (trigmode == 0) {
		trigconv = M_PI/180.;
	}
	if (trigmode == 1) {
		trigconv = 1;
	}
}

/*
 * Draw a single digit of mantissa/exponent, taking into account
 * context and display precision.
 * 	  x : if x<0, draw the abs(x)-th digit of mantissa
 * 	      if x==0 and ch==0, draw the "x10" part of the exponent
 * 	      if x>0, draw the x-th digit of the exponent
 * 	  pos: y-position of the digit (pos=0...3 for X...T stack registers, 4..7 for their uncertainties)
 * 	  ch: digit to draw (ch=0...9)
 */
void draw_char(int x, int pos, char ch) {
	if (context == CONTEXT_REAL) {
		if (x<0) {
			//sharp_string(str, &font_24x40, 288+24*x, 0);
			sharp_char_fast_24x40(ch, 36+3*x, 0);
		} else {
			if (x==0 && ch == 0) {
				sharp_char('\x9e', &font_12x20, 288, 12);
				sharp_string("10", &font_16x26, 300, 10);
			} else {
				sharp_char(ch, &font_16x26, 316+16*x, 0);
			}
		}
	} else if (context == CONTEXT_UNCERT) {
		int pos2 = pos/4;
		if (precision_uncert > 6) {
			if (x<0) {
				sharp_char(ch, &font_12x20, 152+12*x+192*pos2, 10);
			} else {
				if (x==0 && ch == 0) {
					sharp_char('\x9e', &font_6x8, 154+192*pos2, 20);
					sharp_string("10", &font_6x8, 160+192*pos2, 20);
				} else {
					sharp_char(ch, &font_12x20, 148+12*x+192*pos2, 0);
				}
			}
		} else {
			if (x<0) {
				sharp_char(ch, &font_16x26, 132+16*x+192*pos2, 10);
			} else {
				if (x==0 && ch == 0) {
					sharp_char('\x9e', &font_12x20, 132+192*pos2, 15);
					sharp_string("10", &font_12x20, 144+192*pos2, 15);
				} else {
					sharp_char(ch, &font_12x20, 148+12*x+192*pos2, 0);
				}
			}
		}
	}
}

void draw_decpoint(int x, int pos) {
	if (context == CONTEXT_REAL) {
		sharp_char('.', &font_24x40, 288+24*x-13, 4);
	} else if (context == CONTEXT_UNCERT) {
		int pos2 = pos/4;
		if (precision_uncert > 6) {
			sharp_char('.', &font_12x20, 152+12*x-6+192*pos2, 13);
		}
		else {
			sharp_char('.', &font_16x26, 132+16*x-8+192*pos2, 14);
		}
	}
}

void clear_cursor() {
	sharp_clear_buffer(4, 0xFF);
	sharp_send_buffer(BOTTOM_YPOS+42, 4);
}

void draw_cursor() {
	sharp_clear_buffer(4, 0xFF);
	if (context == CONTEXT_UNCERT) {
		if (precision_uncert>6) {
			if (input.expentry) {
				sharp_filled_rectangle(160 + input_uncert*192, 0, 46, 4, 0);
			} else {
				sharp_filled_rectangle(20 + input_uncert*(192+12), 0, 130-input_uncert*12, 4, 0);
			}
		} else {
			if (input.expentry) {
				sharp_filled_rectangle(146 + input_uncert*192, 0, 56, 4, 0);
			} else {
				sharp_filled_rectangle(20 + input_uncert*(192+12), 0, 110-input_uncert*12, 4, 0);
			}
		}
	} else {
		if (input.expentry) {
			sharp_filled_rectangle(300, 0, 95, 4, 0);
		} else {
			sharp_filled_rectangle(20, 0, 288-20, 4, 0);
		}
	}
	sharp_send_buffer(BOTTOM_YPOS+42, 4);
}


/* Draw stack register name for the position "pos" (pos=0...3) for "X"..."T"
 * in the string buffer. */
void draw_stack_register_name(int pos) {
	uint8_t reg[4] = {'x','y','z','t'};
	sharp_char(reg[pos], &font_16x26, 1, 1);
}

/* Draw status string (status of modifier keys, voltage, etc.)
 * in the buffer and send it to display. */
void draw_status() {
	char v[34];
	/* Paint 2 top lines black */
	sharp_clear_buffer(2, 0x00);
	sharp_send_buffer(0, 2);
	/* Prepare empty buffer for status string */
	sharp_clear_buffer(20, 0xFF);

	for (int i=0; i<33; i++) v[i] = ' ';
	v[33] = 0x00;

	if (shift == 1) {
		v[0] = 'F';
	} else if (shift == 2) {
		v[0] = 'G';
	}

	sprintf(&(v[2]), "S%d", stack_size);

	if (dispmode == 1) {
		memcpy(&(v[6]), "SCI", 3);
	} else if (dispmode == 2) {
		memcpy(&(v[6]), "ENG", 3);
	}
	if (trigmode == 0) {
		memcpy(&(v[10]), "DEG", 3);
	} else if (trigmode == 1) {
		memcpy(&(v[10]), "RAD", 3);
	}
	if (context == CONTEXT_UNCERT) {
		memcpy(&(v[14]), "UNC", 3);
	}
	if (variables[0] != 0.) {
		v[18] = 'M';
	}
	if (context == CONTEXT_REAL)
	  sprintf(&(v[20]), "N%d", precision);
	if (context == CONTEXT_UNCERT)
	  sprintf(&(v[20]), "N%d", precision_uncert);

	if (program_entry)
		sprintf(&(v[24]), "P%d", program_size);
	else if (program_step)
		sprintf(&(v[24]), "R%d", program_step);
	else if (program_size>0)
		memcpy(&(v[24]), "P  ", 3);

	uint16_t voltage = battery_voltage();
	if (voltage>0 && voltage<9000) {
		//sprintf(&(v[28]), "%d", voltage/1000);
		//v[29] = '.';
		//sprintf(&(v[30]), "%02dV", (voltage%1000)/10);
		sprintf(&(v[28]), "%d", voltage);
	}
	for (int i=0; i<33; i++) if (v[i] == 0x00) v[i] = ' ';

	sharp_string(v, &font_12x20, 2, 0);
	sharp_invert_buffer(20);
	sharp_send_buffer(2, 20);
}

void draw_number_split(int pos, int64_t _mantissa, int _exponent, int pointpos, int hideexp) {
	int i;
	int64_t mantissa = _mantissa;
	int32_t exponent = _exponent;

	draw_stack_register_name(pos % 4);
	int prec = precision;
	if (context == CONTEXT_UNCERT) {
		sharp_char('\xf1', &font_12x20, 212, 11);
		prec = precision_uncert;
	}

	if (mantissa < 0) mantissa = -mantissa;
	//mantissa = abs(mantissa);
	for (i=0; i<prec; i++) {
		uint8_t ch = mantissa % 10;
		mantissa = mantissa/10;
		draw_char(-(i+1), pos, ch+'0');
		if (mantissa == 0 && pointpos + i >= prec) break;
	}
	if (_mantissa<0) draw_char(-(i+2), pos, '-');
	draw_decpoint(-(prec-pointpos), pos);

	if (exponent != 0 || !hideexp) {
		draw_char(0, pos, 0);
		if (exponent<0) draw_char(1, pos, '-');
		if (exponent<0) exponent = -exponent;
		for (i=0; i<3; i++) {
			uint8_t ch = exponent % 10;
			exponent = exponent/10;
			draw_char((4-i), pos, ch+'0');
		}
	}
}

void draw_error(int pos, int code) {
	char* message;
	if (code == 1) {
		message = "Error";
	}
	sharp_clear_buffer(40, 0xFF);
	sharp_string(message, &font_24x40, 288-24*6, 0);
	sharp_send_buffer(BOTTOM_YPOS-pos*LINE_INTERVAL, 40);
	clear_cursor();
}


void draw_number_sci(int pos, double num) {
	int exponent;
	int64_t mantissa;
	int prec = precision;
	if (context == CONTEXT_UNCERT) prec = precision_uncert;
	if (num != 0) {
		exponent = (int)floor(log10(fabs(num)));
		mantissa = (int64_t)round(fabs(num)/pow(10, exponent-prec+1));
		if (mantissa > max_mantissa[prec]) {
			mantissa /= 10;
			exponent += 1;
		}
		if (num<0) mantissa = -mantissa;
	} else {
		mantissa = 0;
		exponent = 0;
	}
	draw_number_split(pos, mantissa, exponent, 1, 0);
}

void draw_number_eng(int pos, double num) {
	int exponent;
	int64_t mantissa;
	const char si_prefix[] = "yzafpn""\xe6""m kMGTPEZY";
	int prec = precision;
	if (context == CONTEXT_UNCERT) prec = precision_uncert;
	if (num != 0) {
		exponent = (int)floor(log10(fabs(num)));
		mantissa = (int64_t)round(fabs(num)/pow(10, exponent-prec+1));
		if (mantissa > max_mantissa[prec]) {
			mantissa /= 10;
			exponent += 1;
		}
		if (num<0) mantissa = -mantissa;
	} else {
		mantissa = 0;
		exponent = 0;
	}
	int exp2;
	if (exponent >= 0) exp2 = 3*(exponent/3);
	else exp2 = -3*(1-(exponent+1)/3);
	draw_number_split(pos, mantissa, exp2, exponent-exp2+1, 0);
	int npref = exp2/3;
	if (npref>=-8 && npref<=8 && npref != 0) {
		char str[4] = "[ ]";
		str[1] = si_prefix[npref+8];
		if (context == CONTEXT_REAL) {
			sharp_string(str, &font_12x20, 364, 22);
		} else {
			int pos2 = pos/4;
			sharp_string(str, &font_12x20, 174+192*pos2, 21);
		}
	}
}

void draw_number_normal(int pos, double num) {
	int i;
	int exponent;
	int64_t mantissa;
	int pointpos=1;
	int prec = precision;
	if (context == CONTEXT_UNCERT) prec = precision_uncert;
	if (num != 0) {
		exponent = (int)floor(log10(fabs(num)));
		mantissa = (int64_t)round(fabs(num)/pow(10, exponent-prec+1));
		if (mantissa > max_mantissa[prec]) {
			mantissa /= 10;
			exponent += 1;
		}
		if (exponent < prec && exponent > 0) {
			pointpos = exponent+1;
			exponent = 0;
		}
		if (exponent < 0 && exponent > -4) {
			mantissa = (int64_t)round(fabs(num)*pow(10, prec-1));
			pointpos = 1;
			exponent = 0;
		}
		for (i=0; i<prec; i++) {
			if (mantissa % 10 == 0 && pointpos < prec) {
				mantissa /= 10;
				pointpos++;
			} else {
				break;
			}
		}
		if (num<0) mantissa = -mantissa;
	} else {
		mantissa = 0;
		exponent = 0;
		pointpos = prec;
	}
	draw_number_split(pos, mantissa, exponent, pointpos, 1);
}

#define DRAWMODE_CLEAR 1
#define DRAWMODE_FLUSH 2

void draw_number(int pos, double num, int mode) {
	int pos2 = pos % 4;
	if (mode & DRAWMODE_CLEAR) sharp_clear_buffer(44, 0xFF);
	if (stack_size>pos2) {
		// Only draw if stack is deep enough
		if (dispmode == 0) draw_number_normal(pos, num);
		if (dispmode == 1) draw_number_sci(pos, num);
		if (dispmode == 2) draw_number_eng(pos, num);
	}
	if (mode & DRAWMODE_FLUSH) sharp_send_buffer(BOTTOM_YPOS-(pos % 4)*LINE_INTERVAL, 44);
}

void draw_stack() {
	if (context == CONTEXT_REAL) {
		int cat = finite(stack[0]);
		if (!cat && stack_size>0) {
			draw_error(0, 1);
			error_flag = 1;
		} else {
			draw_number(0, stack[0], DRAWMODE_CLEAR | DRAWMODE_FLUSH);
		}
		draw_number(1, stack[1], DRAWMODE_CLEAR | DRAWMODE_FLUSH);
		draw_number(2, stack[2], DRAWMODE_CLEAR | DRAWMODE_FLUSH);
		draw_number(3, stack[3], DRAWMODE_CLEAR | DRAWMODE_FLUSH);
	} else if (context == CONTEXT_UNCERT) {
		int cat = finite(stack[0]) && finite(stack2[0]);
		if (!cat && stack_size>0) {
			draw_error(0, 1);
			error_flag = 1;
		} else {
			draw_number(0, stack[0], DRAWMODE_CLEAR);
			draw_number(4, stack2[0], DRAWMODE_FLUSH);
		}
		draw_number(1, stack[1], DRAWMODE_CLEAR);
		draw_number(5, stack2[1], DRAWMODE_FLUSH);
		draw_number(2, stack[2], DRAWMODE_CLEAR);
		draw_number(6, stack2[2], DRAWMODE_FLUSH);
		draw_number(3, stack[3], DRAWMODE_CLEAR);
		draw_number(7, stack2[3], DRAWMODE_FLUSH);
	}
	//clear_cursor();
}

void draw_input() {
	int i;
	sharp_clear_buffer(44, 0xFF);
	int pos;
	if (context == CONTEXT_UNCERT) {
		if (input_uncert) {
			pos = 4;
			draw_number(0, stack[0], 0);
		} else {
			pos = 0;
			draw_number(4, stack2[0], 0);
		}
	}

	draw_stack_register_name(0);
	if (input.mpos == 0) {
		draw_char(-1, pos, '0');
		if (input.sign) draw_char(-2, pos, '-');
	} else {
		for (i=0; i<input.mpos; i++) {
			draw_char((i-input.mpos), pos, input.mantissa[i]+'0');
		}
		if (input.point>0) {
			draw_decpoint((input.point-input.mpos), pos);
		}
		if (input.sign) draw_char(-(input.mpos+1), pos, '-');
		if (input.expentry == 1) {
			draw_char(0, pos, 0);
			for (i=0; i<3; i++) {
				draw_char((4-i), pos, input.exponent[i]+'0');
			}
			if (input.expsign) draw_char(1, pos, '-');
		}
	}
	sharp_send_buffer(BOTTOM_YPOS, 44);
	//draw_cursor();
}

void enter_number(char c) {
	if (!input.started) {
		if (!input.replace_x && !error_flag) {
			stack_push(0, 0);
			if (stack_size>1) draw_flags |= DRAW_STACK;
		}
		error_flag = 0;
		input.started = 1;
		input.replace_x = 0;
		stack2[0] = 0;
	}
	if (input.expentry == 0) {
		if (input.mpos < 10 && !(c==0 && input.point == 0 && input.mpos == 0)) {
			input.mantissa[input.mpos++] = c;
		}
	} else {
		input.exponent[2] = input.exponent[1];
		input.exponent[1] = input.exponent[0];
		input.exponent[0] = c;
	}
	draw_flags |= (DRAW_INPUT | DRAW_CURSOR);
}

void enter_backspace() {
	if (stack_size<1) return;
	if (input.started) {
		if (input.expentry == 0) {
			if (input.mpos > 0) {
				if (input.point>0 && input.point>=input.mpos) {
					input.point = 0;
				} else {
					input.mpos--;
					if (input.mpos == 0) input.sign = 0;
				}
			} else {
				input.sign = 0;
			}
		} else {
			if (input.exponent[0] == 0 && input.exponent[1] == 0 && input.exponent[2] == 0)
				input.expentry = 0;
			else {
				input.exponent[0] = input.exponent[1];
				input.exponent[1] = input.exponent[2];
				input.exponent[2] = 0;
				if (input.exponent[0] == 0 && input.exponent[1] == 0 && input.exponent[2] == 0)
					input.expsign = 0;
			}
		}
		draw_flags |= (DRAW_INPUT | DRAW_CURSOR);
	} else {
		error_flag = 0;
		input.replace_x = 1;
		stack[0] = 0;
		stack2[0] = 0;
		draw_flags |= (DRAW_STACK | DRAW_CURSOR);
	}
}

void enter_decpoint() {
	if (!input.started) {
		//error_flag = 0;
		if (!input.replace_x && !error_flag) {
			stack_push(0, 0);
			if (stack_size>1) draw_flags |= DRAW_STACK;
		}
		error_flag = 0;
		input.started = 1;
		input.replace_x = 0;
		stack2[0] = 0;
	}
	if (input.expentry == 0 && input.point == 0) {
		if (input.mpos == 0) input.mantissa[input.mpos++] = 0;
		input.point = input.mpos;
	}
	draw_flags |= (DRAW_INPUT | DRAW_CURSOR);
}

void enter_exp() {
	if (!input.started) {
		//error_flag = 0;
		if (!input.replace_x && !error_flag) {
			stack_push(0, 0);
			draw_flags |= DRAW_STACK;
		}
		error_flag = 0;
		input.started = 1;
		input.replace_x = 0;
		//stack2[0] = 0;
	}
	if(input.mpos == 0 || (input.mpos == 1 && input.mantissa[0] == 0)) {
		input.mantissa[0] = 1;
		input.mpos = 1;
	}
	input.expentry = 1;
	draw_flags |= (DRAW_INPUT | DRAW_CURSOR);
}

void enter_sign() {
	if (input.started) {
		if (input.expentry==0) {
			if (input_uncert == 0) input.sign = 1-input.sign;
		} else {
			input.expsign = 1-input.expsign;
		}
		draw_flags |= (DRAW_INPUT | DRAW_CURSOR);
	} else {
		if (error_flag) return;
		stack[0] = -stack[0];
		draw_flags |= DRAW_STACK;
		if (input.replace_x) draw_flags |= DRAW_CURSOR;
	}
}

double convert_input() {
	int i;
	double number = 0.;
	double shift = 1;

	for (i=0; i<input.mpos; i++) {
		number += input.mantissa[input.mpos-i-1]*shift;
		shift *= 10;
	}
	int exponent = 100*input.exponent[2] + 10*input.exponent[1] + input.exponent[0];
	if (input.expsign) exponent = -exponent;
	if (input.point) exponent -= (input.mpos-input.point);

	number *= pow(10, exponent);
	if (input.sign) number = -number;

	if (!finite(number)) {
		draw_flags |= DRAW_ERROR;
		error_flag = 1;
	}
	return(number);
}

void maybe_convert_input() {
	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
		clear_input();
	}
}


void enter_enter() {
	maybe_convert_input();
	input_uncert = 0;
	if (error_flag) return;
	input.replace_x = 1;
	stack_push(stack[0], stack2[0]);
	draw_flags |= (DRAW_STACK | DRAW_CURSOR);
}

void enter_uncert() {
	if (context != CONTEXT_UNCERT) return;
	if (stack_size<1) return;
	if (input_uncert == 0) {
		if (input.started) {
			stack[0] = convert_input();
			clear_input();
		}
		if (error_flag) return;
		input_uncert = 1;
		input.started = 1;
		draw_flags |= (DRAW_STACK | DRAW_CURSOR);
	} else {
		if (input.started) {
			stack2[0] = convert_input();
			clear_input();
		}
		if (error_flag) return;
		input_uncert = 0;
		draw_flags |= DRAW_STACK;
	}
}

void enter_drop() {
	error_flag = 0;
	if (input.started) {
		clear_input();
	}
	input.replace_x = 0;
	stack_drop();
}

void enter_rotate_up() {
	maybe_convert_input();
	if (error_flag) return;
	input.replace_x = 0;
	stack_rotate_up();
}

void enter_rotate_down() {
	maybe_convert_input();
	if (error_flag) return;
	input.replace_x = 0;
	stack_rotate_down();
}

void enter_clear() {
	error_flag = 0;
	if (input.started) {
		clear_input();
	}
	input.replace_x = 0;
	sharp_clear();
	clear_stack();
}

void enter_clear_mem() {
	error_flag = 0;
	clear_variables();
}

void enter_lastx() {
	maybe_convert_input();
	input.replace_x = 0;
	if (!error_flag) {
		stack_push(lastx, lastx2);
	} else {
		error_flag = 0;
		stack[0] = lastx;
		stack2[0] = lastx2;
	}
}

void enter_swap_xy() {
	if (stack_size<2) return;
	maybe_convert_input();
	if (error_flag) return;
	input.replace_x = 0;
	double tmp = stack[0];
	stack[0] = stack[1];
	stack[1] = tmp;
	tmp = stack2[0];
	stack2[0] = stack2[1];
	stack2[1] = tmp;
}

void change_dispmode() {
	if (error_flag) return;
	maybe_convert_input();
	dispmode = (dispmode+1) % 3;
	shift = 0;
	input_uncert = 0;
	draw_flags |= DRAW_STACK;
}

void change_precision() {
	if (error_flag) return;
	maybe_convert_input();
	int prec = precision;
	if (context == CONTEXT_UNCERT) prec = precision_uncert;
	if (shift == 1) prec--;
	else prec++;
	if (prec > 10) prec = 3;
	if (prec < 3) prec = 10;
	if (context == CONTEXT_UNCERT) precision_uncert = prec;
	else precision = prec;
	shift = 0;
	input_uncert = 0;
	draw_flags |= DRAW_STACK;
}

void change_trigmode() {
	trigmode = (trigmode+1) % 2;
	set_trigconv();
	if (shift == 1) { // Perform conversion
		maybe_convert_input();
		if (trigmode == 0) {
			// New trig mode is DEGREES
			stack[0] *= 180./M_PI;
			stack2[0] *= 180./M_PI;
		} else {
			// New trig mode is RADIANS
			stack[0] /= 180./M_PI;
			stack2[0] /= 180./M_PI;
		}
		draw_flags |= DRAW_STACK;
	}
	shift = 0;
	draw_flags |= DRAW_STATUS;
}

void change_context() {
	maybe_convert_input();
	context = 1-context;
	if (context != CONTEXT_UNCERT) {
		input_uncert = 0;
	}
	draw_flags |= DRAW_STACK;
}

void clear_shift() {
	shift = 0;
}

void enter_shift() {
	if (shift != 1) shift = 1;
	else shift = 0;
	draw_flags |= DRAW_STATUS;
}

void enter_shift2() {
	if (shift != 2) shift = 2;
	else shift = 0;
	draw_flags |= DRAW_STATUS;
}

void calc_init() {
	trigmode = 0;
	dispmode = 0;
	shift = 0;
	context = CONTEXT_REAL;
	precision = 10;
	precision_uncert = 6;
	input_uncert = 0;
	program_entry = 0;
	program_step = 0;

	set_trigconv();

	clear_input();
	clear_stack();
	clear_variables();
	draw_stack();
	draw_status();
}

void calc_refresh() {
	shift = 0;
	clear_input();
	draw_stack();
	draw_status();
}

void apply_enter(uint16_t code) {
	switch(code) {
	case OP_ENTER_0 : enter_number(0); break;
	case OP_ENTER_1 : enter_number(1); break;
	case OP_ENTER_2 : enter_number(2); break;
	case OP_ENTER_3 : enter_number(3); break;
	case OP_ENTER_4 : enter_number(4); break;
	case OP_ENTER_5 : enter_number(5); break;
	case OP_ENTER_6 : enter_number(6); break;
	case OP_ENTER_7 : enter_number(7); break;
	case OP_ENTER_8 : enter_number(8); break;
	case OP_ENTER_9 : enter_number(9); break;
	case OP_ENTER_DECPOINT: enter_decpoint(); break;
	case OP_ENTER_SIGN: enter_sign(); break;
	case OP_ENTER_EXP: enter_exp(); break;
	case OP_ENTER_BACKSPACE: enter_backspace(); break;
	case OP_ENTER_UNCERT: enter_uncert(); break;
	case OP_ENTER: enter_enter(); break;
	default: break;
	}
}

void apply_stack(uint16_t code) {
	switch(code) {
	case OP_SWAP: enter_swap_xy(); break;
	case OP_LASTX: enter_lastx(); break;
	case OP_DROP: enter_drop(); break;
	case OP_CLEAR_STACK: enter_clear(); break;
	case OP_ROTUP: enter_rotate_up(); break;
	case OP_ROTDOWN: enter_rotate_down(); break;
	case OP_CLEAR_MEM: enter_clear_mem(); break;
	default: break;
	}
}

void apply_func_1to1(uint16_t code) {
	if (stack_size<1) return;
	double f = 0;
	double x = stack[0];
	int gamma_sign;
	switch(code) {
	case OP_SIN: f = sin(trigconv*x); break;
	case OP_COS: f = cos(trigconv*x); break;
	case OP_TAN: f = tan(trigconv*x); break;
	case OP_ASIN: f = asin(x)/trigconv; break;
	case OP_ACOS: f = acos(x)/trigconv; break;
	case OP_ATAN: f = atan(x)/trigconv; break;
	case OP_LG: f = log10(x); break;
	case OP_LN: f = log(x); break;
	case OP_EXP: f = exp(x); break;
	case OP_POW10: f = pow(10., x); break;
	case OP_SQRT: f = sqrt(x); break;
	case OP_SQR: f = x*x; break;
	case OP_INV: f = 1./x; break;
	case OP_ERF: f = erf(x); break;
	case OP_ERFINV: f = erfinv(x); break;
	case OP_GAMMA: f = tgamma(x); break;
	case OP_FACTORIAL: f = tgamma(x+1.); break;
	case OP_LOGGAMMA: f = lgamma_r(x, &gamma_sign); break;
	case OP_GAMMABETA: f = 1./sqrt(1.-x*x); break;
	case OP_BETAGAMMA: f = sqrt(1.-1./(x*x)); break;
	case OP_ETATHETA: f = -log(tan(trigconv*x/2.)); break;
	case OP_THETAETA: f = atan(exp(-x))*2/trigconv; break;
	case OP_SIGNIF_X: if (context != CONTEXT_UNCERT) return;
	case OP_GAUSS_PVALUE: f = erfinv(1.-x)*sqrt(2.); break;
	default: break;
	}
	lastx = stack[0];
	if (context == CONTEXT_UNCERT) {
		double ef = 0;
		double ex = stack2[0];
		switch(code) {
		case OP_SIN: ef = trigconv*fabs(cos(trigconv*x))*ex; break;
		case OP_COS: ef = trigconv*fabs(sin(trigconv*x))*ex; break;
		case OP_TAN: ef = trigconv/pow(cos(trigconv*x),2)*ex; break;
		case OP_ASIN: ef = ex/sqrt(1.-x*x)/trigconv; break;
		case OP_ACOS: ef = ex/sqrt(1.-x*x)/trigconv; break;
		case OP_ATAN: ef = ex/(1+x*x)/trigconv; break;
		case OP_LG: ef = ex/fabs(x)/log(10.); break;
		case OP_LN: ef = ex/fabs(x); break;
		case OP_EXP: ef = ex*exp(x); break;
		case OP_POW10: ef = pow(10., x)*log(10.)*ex; break;
		case OP_SQRT: ef = 0.5*ex/sqrt(x); break;
		case OP_SQR: ef = 2.*fabs(x)*ex; break;
		case OP_INV: ef = ex/x/x; break;
		case OP_ERF: ef = 0; break;     // Not implemented
		case OP_ERFINV: ef = 0; break;
		case OP_GAMMA: ef = 0; break;
		case OP_FACTORIAL: ef = 0; break;
		case OP_LOGGAMMA: ef = 0; break;
		case OP_SIGNIF_X: f = x/ex; break;
		default: break;
		}
		stack2[0] = ef;
	}
	stack[0] = f;
}

void apply_func_2to1(uint16_t code) {
	if (stack_size<2) return;
	double f = 0;
	double ef = 0;
	double x = stack[0];
	double y = stack[1];
	int gamma_sign;

	switch(code) {
	case OP_PLUS: f = x+y; break;
	case OP_MINUS: f = y-x; break;
	case OP_MULT: f = y*x; break;
	case OP_DIV: f = y/x; break;
	case OP_POW: f = pow(y, x); break;
	case OP_ROOTX: f = pow(y, 1./x); break;
	case OP_CYX: f = exp(lgamma_r(y+1, &gamma_sign) - lgamma_r(x+1, &gamma_sign) - lgamma_r(y-x+1, &gamma_sign)); break;
	case OP_PYX: f = exp(lgamma_r(y+1, &gamma_sign) - lgamma_r(y-x+1, &gamma_sign)); break;
	case OP_SIGNIF_XY: if (context != CONTEXT_UNCERT) return;
	case OP_POISSON :  f = x < 0 ? NAN : exp(x*log(y) - y - lgamma_r(x+1, &gamma_sign)); break;
	case OP_CHI2_PROB :  f = chisquared_cdf_c(x, y); break;
	default: break;
	}
	lastx = stack[0];
	if (context == CONTEXT_UNCERT) {
		double ex = stack2[0];
		double ey = stack2[1];
		switch(code) {
		case OP_PLUS:
		case OP_MINUS: ef = sqrt(ex*ex+ey*ey); break;
		case OP_MULT: ef = sqrt(x*x*ey*ey + y*y*ex*ex); break;
		case OP_DIV: ef = sqrt(ey*ey/x/x + ex*ex/x/x/x/x*y*y); break;
		case OP_POW: ef = sqrt(ex*ex*pow(log(y)*pow(y, x), 2) + ey*ey*pow(x*pow(y, x-1), 2)); break;
		case OP_ROOTX: ef = sqrt(ex*ex*pow(1./x/x*log(y)*pow(y, 1./x), 2) + ey*ey*pow(1./x*pow(y, 1./x-1), 2)); break;
		case OP_SIGNIF_XY: f = (y-x)/sqrt(ex*ex+ey*ey); break;
		default: break;
		}
		lastx2 = stack2[0];
	}
	stack_drop();
	stack[0] = f;
	stack2[0] = ef;
}

void apply_func_3to1(uint16_t code) {
	if (stack_size<3) return;
	double f = 0;
	double ef = 0;
	double x = stack[0];
	double y = stack[1];
	double z = stack[2];
	switch(code) {
	case OP_PZXY: f = sqrt((z*z - (x+y)*(x+y))*(z*z - (x-y)*(x-y)))/2./z; break;
	default: break;
	}
	lastx = stack[0];
	lastx2 = stack2[0];
	stack_drop();
	stack_drop();
	stack[0] = f;
	stack2[0] = ef;
}

void apply_func_stat(uint16_t code) {
	if (stack_size<1) return;
	double f = 0;
	double ef = 0;
	switch(code) {
	case OP_STAT_MEAN:
		stat_mean(stack, stack2, stack_size, &f, &ef);
		break;
	case OP_STAT_CHI2:
		if (context == CONTEXT_UNCERT) f = stat_chi2(stack, stack2, stack_size);
		else return;
		break;
	}
	lastx = stack[0];
	lastx2 = stack2[0];
	stack_push(f, ef);
}

void apply_func_2to2(uint16_t code) {
	if (stack_size<2) return;
	double fx = 0;
	double efx = 0;
	double fy = 0;
	double efy = 0;
	double x = stack[0];
	double y = stack[1];
	switch (code) {
	case OP_POLAR     : fx = sqrt(x*x + y*y); fy = atan2(y, x)/trigconv; break;
	case OP_DESCARTES : fx = x*cos(trigconv*y); fy = x*sin(trigconv*y); break;
	default: break;
	}
	lastx = stack[0];
	stack[0] = fx;
	stack[1] = fy;
	stack2[0] = efx;  // Uncertainties not implemented
	stack2[1] = efy;
}

void apply_const(uint16_t code) {
	maybe_convert_input();
	input.replace_x = 0;
	double f = 0.;
	switch(code) {
	case OP_CONST_PI: f = M_PI; break;
	case OP_CONST_PLANCK: f = 6.582119569e-22; break;
	case OP_CONST_PLANCKC: f = 197.3269804; break;
	case OP_CONST_E: f = 1.602176634e-19; break;
	case OP_CONST_NA: f = 6.02214076e23; break;
	case OP_CONST_K: f = 8.617333262e-5; break;
	case OP_CONST_C: f = 299792458.; break;
	default: break;
	}

	if (!error_flag) {
		stack_push(f, 0.);
	} else {
		error_flag = 0;
		stack[0] = f;
		stack2[0] = 0;
	}
}

void apply_memory_rcl() {
	maybe_convert_input();
	input.replace_x = 0;
	double f = variables[0];
	double f2 = variables2[0];
	if (!error_flag) {
		stack_push(f, f2);
	} else {
		error_flag = 0;
		stack[0] = f;
		stack2[0] = f2;
	}
}

int get_register_number() {
	double f = stack[0];
	if (f<0. || f>=MAX_MEMORY_SIZE) return -1;
	uint16_t index = (int)floor(f);
	return index;
}

void apply_memory_rcl_x() {
	if (stack_size<1) return;
	maybe_convert_input();
	input.replace_x = 0;
	int16_t index = get_register_number();
	if (index<0) {
		stack_drop();
	} else {
		stack[0] = variables[index];
		stack2[0] = variables2[index];
	}
}

void apply_memory_sto() {
	if (error_flag) return;
	maybe_convert_input();
	input.replace_x = 0;
	variables[0] = stack[0];
	if (context == CONTEXT_UNCERT) {
		variables2[0] = stack2[0];
	}
}

void apply_memory_sto_x() {
	if (error_flag) return;
	if (stack_size<2) return;
	maybe_convert_input();
	input.replace_x = 0;
	uint16_t index = get_register_number();
	if (index>=0) {
		variables[index] = stack[1];
		variables2[index] = stack2[1];
	}
	stack_drop();
	draw_flags |= DRAW_STACK;
}

void apply_memory_plus() {
	if (error_flag) return;
	maybe_convert_input();
	input.replace_x = 0;
	variables[0] += stack[0];
	if (context == CONTEXT_UNCERT) {
		double em = variables2[0];
		double ex = stack2[0];
		variables2[0] = sqrt(ex*ex + em*em);
	}
}

void apply_memory_minus() {
	if (error_flag) return;
	maybe_convert_input();
	input.replace_x = 0;
	variables[0] -= stack[0];
	if (context == CONTEXT_UNCERT) {
		double em = variables2[0];
		double ex = stack2[0];
		variables2[0] = sqrt(ex*ex + em*em);
	}
}

void apply_test(uint16_t code) {
	switch(code) {
	case OP_TEST_1: sharp_test_font(&font_6x8, 0); break;
	case OP_TEST_2: sharp_test_font(&font_7x12b, 0); break;
	case OP_TEST_3: sharp_test_font(&font_12x20, 0); break;
	case OP_TEST_4: sharp_test_font(&font_16x26, 0); break;
	case OP_TEST_5: sharp_test_font(&font_24x40, 0); break;
	case OP_TEST_6: sharp_test_font(&font_24x40, 96); break;
	case OP_TEST_7: sharp_test_font(NULL, 0); break;
	default: break;
	}
}

void apply_op(uint16_t code);

void apply_prog(uint16_t code) {
	switch(code) {
	case OP_PROG :
		// Enter/exit programming mode
		draw_flags |= DRAW_STATUS;
		if (program_entry) {
			program_entry = 0;
			return;
		} else {
			maybe_convert_input();
			input.replace_x = 0;
			program_entry = 1;
			program_size = 0;
			return;
		}
	case OP_RUN :
		// Run the program
		//set_clock_1mhz();
		maybe_convert_input();
		input.replace_x = 0;
		for (uint16_t step=0; step < program_size; step++) {
			uint16_t c = program[step];
			uint16_t opmode = c & OPMODE_MASK;
			if (opmode != OPMODE_PROG) // Make sure we don't enter infinite nested loop
				apply_op(c);
		}
		draw_flags &= ~(DRAW_INPUT | DRAW_CURSOR);
		//set_clock_8mhz();
		break;
	case OP_STEP:
		if (program_entry) return;
		if (program_step == 0) { // Convert input only at the start of the program
			maybe_convert_input();
			input.replace_x = 0;
		}
		if (program_step < program_size) {
			uint16_t c = program[program_step];
			uint16_t opmode = c & OPMODE_MASK;
			if (opmode != OPMODE_PROG) // Make sure we don't enter infinite nested loop
				apply_op(c);
			program_step++;
		}
		if (program_step >= program_size) program_step = 0; // Rewind to start
		break;
	case OP_REWIND:
		if (program_entry) return;
		program_step = 0;
		break;

	default: break;
	}
}

// Process the operation given its code
void apply_op(uint16_t code) {
	uint16_t opmode = code & OPMODE_MASK;
	if (program_entry && opmode != OPMODE_PROG) {
		// Recording program
		if (program_size < MAX_PROGRAM_SIZE) {
			program[program_size] = code;
			program_size++;
		} else {
			// Exceeded maximum program size
			program_entry = 0;
		}
		draw_flags |= DRAW_STATUS;
	}

	if (code == OP_NOP) return;
	if (opmode == OPMODE_ENTER) {
		apply_enter(code);
		return;
	}
	if (opmode == OPMODE_STACK) {
		apply_stack(code);
		draw_flags |= DRAW_STACK;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_CONST) {
		apply_const(code);
		draw_flags |= DRAW_STACK;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_RCL) {
		apply_memory_rcl();
		draw_flags |= DRAW_STACK;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_STO) {
		apply_memory_sto();
		draw_flags |= DRAW_STATUS;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_RCLX) {
		apply_memory_rcl_x();
		draw_flags |= DRAW_STACK;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_STOX) {
		apply_memory_sto_x();
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_MPLUS) {
		apply_memory_plus();
		draw_flags |= DRAW_STATUS;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_MMINUS) {
		apply_memory_minus();
		draw_flags |= DRAW_STATUS;
		input_uncert = 0;
		return;
	}
	if (opmode == OPMODE_PROG) {
		apply_prog(code);
		return;
	}

	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
		input_uncert = 0;
		clear_input();
	}
	if (error_flag) return;
	input.replace_x = 0;
	if (opmode == OPMODE_1TO1) apply_func_1to1(code);
	if (opmode == OPMODE_2TO1) apply_func_2to1(code);
	if (opmode == OPMODE_2TO2) apply_func_2to2(code);
	if (opmode == OPMODE_3TO1) apply_func_3to1(code);
	if (opmode == OPMODE_STAT) apply_func_stat(code);
	if (opmode == OPMODE_TEST)
		apply_test(code);
	else
		draw_flags |= DRAW_STACK;
}

// Process the key codes depending on shift modifier state
//   "code" : no shift keys
//   "code1" : with "F" shift
//   "code2" : with "G" shift
void enter_key(uint16_t code, uint16_t code1, uint16_t code2) {
	if (shift == 0) apply_op(code);
	if (shift == 1) {
		apply_op(code1);
		shift = 0;
		draw_flags |= DRAW_STATUS;
	}
	else if (shift == 2) {
		apply_op(code2);
		shift = 0;
		if ((code2 & OPMODE_MASK) != OPMODE_TEST) draw_flags |= DRAW_STATUS;
	}
}

// Main callback to process the key press
// Return 0 if we need to switch OFF, otherwise 1
int calc_on_key(int c) {

	draw_flags = 0; // Reset all drawing function flags
	// They will be set inside the functions processing key presses

	switch(c) {
	case  1 : enter_key(OP_ENTER_0, OP_NOP, OP_NOP); break;
	case  7 : enter_key(OP_ENTER_1, OP_CONST_PI, OP_CONST_C);  break;
	case  8 : enter_key(OP_ENTER_2, OP_NOP, OP_CONST_PLANCK);  break;
	case  9 : enter_key(OP_ENTER_3, OP_NOP, OP_CONST_PLANCKC);  break;
	case 13 : enter_key(OP_ENTER_4, OP_POISSON, OP_CONST_E);  break;
	case 14 : enter_key(OP_ENTER_5, OP_CHI2_PROB, OP_CONST_NA);  break;
	case 15 : enter_key(OP_ENTER_6, OP_GAUSS_PVALUE, OP_CONST_K);  break;
	case 19 : enter_key(OP_ENTER_7, OP_ETATHETA, OP_THETAETA);  break;
	case 20 : enter_key(OP_ENTER_8, OP_GAMMABETA, OP_BETAGAMMA);  break;
	case 21 : enter_key(OP_ENTER_9, OP_PZXY, OP_NOP);  break;

	case  2 : enter_key(OP_ENTER_SIGN, OP_NOP, OP_NOP);  break;
	case  3 : enter_key(OP_ENTER_DECPOINT, OP_NOP, OP_NOP);  break;
	case  4 : enter_key(OP_ENTER_UNCERT, OP_NOP, OP_NOP); break;
	case  5 : enter_key(OP_NOP, OP_NOP, OP_NOP);  break;
	case 22 : enter_key(OP_ENTER_EXP, OP_STAT_CHI2, OP_NOP);  break;
	case 23 : enter_key(OP_ENTER_BACKSPACE, OP_CLEAR_STACK, OP_CLEAR_MEM);  break;

	case 16 : enter_key(OP_MULT, OP_STAT_MEAN, OP_NOP); break;
	case 17 : enter_key(OP_DIV, OP_NOP, OP_NOP); break;
	case 10 : enter_key(OP_PLUS, OP_SIGNIF_X, OP_NOP); break;
	case 11 : enter_key(OP_MINUS, OP_SIGNIF_XY, OP_NOP); break;

	case 25 : enter_key(OP_PROG, OP_REWIND, OP_NOP);  break;
	case 26 : enter_key(OP_RUN, OP_STEP, OP_NOP);  break;
	case 27 : enter_key(OP_NOP, OP_NOP, OP_NOP);  break;
	case 28 : enter_key(OP_NOP, OP_NOP, OP_NOP);  break;
	case 29 : enter_key(OP_ENTER, OP_NOP, OP_NOP);  break;

	case 31 : enter_key(OP_SQRT, OP_SQR, OP_TEST_7); break;
	case 32 : enter_key(OP_INV, OP_FACTORIAL, OP_NOP); break;
	case 33 : enter_key(OP_ERF, OP_ERFINV, OP_NOP); break;
	case 34 : enter_key(OP_POLAR, OP_DESCARTES, OP_NOP); break;
	case 35 : enter_key(OP_GAMMA, OP_LOGGAMMA, OP_NOP); break;
	case 36 : enter_key(OP_CYX, OP_PYX, OP_NOP); break;

	case 37 : enter_key(OP_POW, OP_ROOTX, OP_TEST_1); break;
	case 38 : enter_key(OP_LN, OP_EXP, OP_TEST_2); break;
	case 39 : enter_key(OP_LG, OP_POW10, OP_TEST_3); break;
	case 40 : enter_key(OP_SIN, OP_ASIN, OP_TEST_4); break;
	case 41 : enter_key(OP_COS, OP_ACOS, OP_TEST_5); break;
	case 42 : enter_key(OP_TAN, OP_ATAN, OP_TEST_6); break;

	case 43 : enter_key(OP_DROP, OP_ROTUP, OP_ROTDOWN); break;
	case 44 : enter_key(OP_SWAP, OP_LASTX, OP_NOP); break;
	case 45 : change_trigmode(); break;
	case 46 : enter_key(OPMODE_MPLUS, OPMODE_MMINUS, OP_NOP); break;
	case 47 : enter_key(OPMODE_RCL, OPMODE_RCLX, OP_NOP); break;
	case 48 : enter_key(OPMODE_STO, OPMODE_STOX, OP_NOP); break;

	case 49 : enter_shift(); break;
	case 50 : enter_shift2(); break;
	case 51 : change_dispmode(); break;
	case 52 : change_context(); break;
	case 53 : change_precision(); break;
	case 54 : if (shift == 1) {  // ON/OFF button
		shift = 0;
		draw_status();
		return (0); // Signal the main loop we switch OFF
	}

	default: break;
	}

	// Check drawing flags and call drawing functions
	//clear_cursor();
	if (!(input.started && input.replace_x == 0)) clear_cursor();
	if (draw_flags & DRAW_STACK) draw_stack();
	if (draw_flags & DRAW_INPUT) {
		draw_status(); // Dummy call that magically fixes LCD update
		draw_input();
	}
	if (draw_flags & DRAW_CURSOR) draw_cursor();
	if (draw_flags & DRAW_ERROR) draw_error(0, 1);
	if ((draw_flags & DRAW_STATUS) || (draw_flags & DRAW_STACK)) draw_status();

	return(1); // Do not switch OFF
}
