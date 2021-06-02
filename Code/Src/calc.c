#include <stdio.h>
#include <math.h>

#include "sharp.h"
#include "fonts.h"
#include "func.h"

double stack[4];            // Stack values {X, Y, Z, T}
double lastx;               // Last X value
int error_flag;             // Error flag: 1 if error occurred as a result of last operation

double stack2[4];           // Stack for ERRORs in UNCERT context
double lastx2;              // Last X ERROR in UNCERT context

double variables[256];      // Storage space for variables

int trigmode;     // Trigonometric mode: 0-DEG, 1-RAD
int dispmode;     // Display mode: 0-NORM, 1-SCI, 2-ENG
double trigconv;  // Trigonometric conversion constant, 1 for RAD, (pi/180.) for DEG
int shift;
int context;           // Context: 0-NORMAL, 1-UNCERT
int precision;         // Precision in NORMAL context
int precision_uncert;  // Precision in UNCERT context
int input_uncert;      // Input mode in UNCERT context: 0-VALUE, 1-ERROR
int voltage;           // Battery voltage in mV

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

// Input structure typedef
typedef struct {
  char mantissa[12];   // Mantissa digits array
  char sign;           // Sign: 0 for "+", 1 for "-"
  char exponent[3];    // Exponent digits array
  char expsign;        // Sign of the exponent: 0 for "+", 1 for "-"
  char started;        // 1 if input mode is active
  char enter_pressed;  // 1 if "ENTER" key was just pressed
                       // (such that we need to replace the current X value by the new number)
  char expentry;       // 1 if exponent is being entered
  int8_t point;        // Decimal point position
  int8_t mpos;         // Number of mantissa digits entered
} t_input;

t_input input; // Input structure

void report_voltage(uint16_t v) {
	voltage = v;
}

// Clear stack and error flag
void clear_stack() {
	stack[0] = 0.;
	stack[1] = 0.;
	stack[2] = 0.;
	stack[3] = 0.;
	stack2[0] = 0.;
	stack2[1] = 0.;
	stack2[2] = 0.;
	stack2[3] = 0.;
	lastx = 0.;
	lastx2 = 0.;
	error_flag = 0;
}

// Clear input structure
void clear_input() {
	input.mpos = 0;
	input.sign = 0;
	input.point = 0;
	input.started = 0;
	input.enter_pressed = 0;
	input.expentry = 0;
	input.exponent[0] = 0;
	input.exponent[1] = 0;
	input.exponent[2] = 0;
	input.expsign = 0;
}

// Push the number to stack
void stack_push(double num) {
	stack[3] = stack[2];
	stack[2] = stack[1];
	stack[1] = stack[0];
	stack[0] = num;
}

// Push the number to ERROR stack
void stack2_push(double num) {
	stack2[3] = stack2[2];
	stack2[2] = stack2[1];
	stack2[1] = stack2[0];
	stack2[0] = num;
}

// Drop the value from stack (T register is copied, X is lost)
void stack_drop() {
	stack[0] = stack[1];
	stack[1] = stack[2];
	stack[2] = stack[3];

	stack2[0] = stack2[1];
	stack2[1] = stack2[2];
	stack2[2] = stack2[3];
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

void draw_char(int x, int pos, char ch, char c) {
	char str[2] = {ch, 0x00};
	if (context == CONTEXT_REAL) {
		if (x<0) {
			sharp_string(str, &font_24x40, 288+24*x, 0);
		} else {
			if (x==0 && ch == 0) {
				sharp_string("\x9e", &font_12x20, 288, 12);
				sharp_string("10", &font_16x26, 300, 10);
			} else {
				sharp_string(str, &font_16x26, 316+16*x, 0);
			}
		}
	} else if (context == CONTEXT_UNCERT) {
		int pos2 = pos/4;
		if (precision > 6) {
			if (x<0) {
				sharp_string(str, &font_12x20, 152+12*x+192*pos2, 10);
			} else {
				if (x==0 && ch == 0) {
					sharp_string("\x9e", &font_6x8, 154+192*pos2, 20);
					sharp_string("10", &font_6x8, 160+192*pos2, 20);
				} else {
					sharp_string(str, &font_12x20, 148+12*x+192*pos2, 0);
				}
			}
		} else {
			if (x<0) {
				sharp_string(str, &font_16x26, 132+16*x+192*pos2, 10);
			} else {
				if (x==0 && ch == 0) {
					sharp_string("\x9e", &font_12x20, 132+192*pos2, 15);
					sharp_string("10", &font_12x20, 144+192*pos2, 15);
				} else {
					sharp_string(str, &font_12x20, 148+12*x+192*pos2, 0);
				}
			}
		}
	}
}

void draw_decpoint(int x, int pos) {
	if (context == CONTEXT_REAL) {
		sharp_string(".", &font_24x40, 288+24*x-13, 4);
	} else if (context == CONTEXT_UNCERT) {
		int pos2 = pos/4;
		if (precision > 6) {
			sharp_string(".", &font_12x20, 152+12*x-6+192*pos2, 13);
		}
		else {
			sharp_string(".", &font_16x26, 132+16*x-8+192*pos2, 14);
		}
	}
}

void draw_stack_name(int pos) {
	char* reg[4] = {"X","Y","Z","T"};
	sharp_string(reg[pos], &font_16x26, 1, 7);
}

void draw_status() {
	memset(buffer, 0xFF, BUFFER_SIZE);
	sharp_string(" ", &font_12x20, 2, 0);
	if (shift == 1) {
		sharp_string("SHIFT", &font_12x20, 2, 0);
	} else if (shift == 2) {
		sharp_string("SHIFT2", &font_12x20, 2, 0);
	}
	if (dispmode == 1) {
		sharp_string("SCI", &font_12x20, 80, 0);
	} else if (dispmode == 2) {
		sharp_string("ENG", &font_12x20, 80, 0);
	}
	if (trigmode == 0) {
		sharp_string("DEG", &font_12x20, 130, 0);
	} else if (trigmode == 1) {
		sharp_string("RAD", &font_12x20, 130, 0);
	}
	if (context == CONTEXT_UNCERT) {
		sharp_string("UNCERT", &font_12x20, 180, 0);
	}
	if (variables[0] != 0.) {
		sharp_string("M", &font_12x20, 270, 0);
	}
    char v[8];
    sprintf(v, "%dmV", voltage);
	sharp_string(v, &font_12x20, 320, 0);
	sharp_send_buffer(2, 20);
}

void draw_number_split(int pos, int64_t _mantissa, int _exponent, int pointpos, int hideexp) {
  int i; 
  int64_t mantissa = _mantissa;
  int32_t exponent = _exponent;

  draw_stack_name(pos % 4);
  if (context == CONTEXT_UNCERT) {
	  sharp_string("\xf1", &font_12x20, 212, 11);
  }

  if (mantissa < 0) mantissa = -mantissa;
  //mantissa = abs(mantissa);
  for (i=0; i<precision; i++) {
    uint8_t ch = mantissa % 10; 
    mantissa = mantissa/10;
    draw_char(-(i+1), pos, ch+'0', 1);
    if (mantissa == 0 && pointpos + i >= precision) break;
  }
  if (_mantissa<0) draw_char(-(i+2), pos, '-', 1);
  draw_decpoint(-(precision-pointpos), pos);

  if (exponent != 0 || !hideexp) {
    draw_char(0, pos, 0, 1);
    if (exponent<0) draw_char(1, pos, '-', 1);
    if (exponent<0) exponent = -exponent;
    for (i=0; i<3; i++) {
      uint8_t ch = exponent % 10; 
      exponent = exponent/10;
      draw_char((4-i), pos, ch+'0', 1);
    }
  }
}

/*
void draw_number_uncert_split(int pos, int64_t _mantissa, int64_t _mantissa_err, int _exponent, int pointpos, int pointpos_err, int hideexp) {
  int i;
  int64_t mantissa = _mantissa;
  int64_t mantissa_err = _mantissa_err;
  int32_t exponent = _exponent;

  draw_stack_name(pos);

  if (mantissa < 0) mantissa = -mantissa;
  for (i=0; i<precision; i++) {
    uint8_t ch = mantissa % 10;
    mantissa = mantissa/10;
    draw_char(-(i+1), pos, ch+'0', 1);
    if (mantissa == 0 && pointpos + i >= precision) break;
  }
  if (_mantissa<0) draw_char(-(i+2), pos, '-', 1);
  draw_decpoint(-(precision-pointpos), pos);

  if (exponent != 0 || !hideexp) {
    draw_char(0, pos, 0, 1);
    if (exponent<0) draw_char(1, pos, '-', 1);
    if (exponent<0) exponent = -exponent;
    for (i=0; i<3; i++) {
      uint8_t ch = exponent % 10;
      exponent = exponent/10;
      draw_char((4-i), pos, ch+'0', 1);
    }
  }
}


void draw_number_uncert(int pos, double num, double err) {
  int exponent;
  int64_t mantissa;
  int64_t mantissa_err;
  if (num != 0) {
    exponent = (int)floor(log10(fabs(num)));
    mantissa = (int64_t)round(fabs(num)/pow(10, exponent-precision+1));
    mantissa_err = (int64_t)round(fabs(err)/pow(10, exponent-precision+1));
    if (mantissa > max_mantissa[precision]) {
      mantissa /= 10;
      mantissa_err /= 10;
      exponent += 1;
    }
    if (num<0) mantissa = -mantissa;
  } else {
    mantissa = 0;
    exponent = 0;
    mantissa_err = (int64_t)round(fabs(err)/pow(10, exponent-precision+1));
  }
}

*/

void draw_error(int pos, int code) {
  char* message;
  if (code == 1) {
    message = "Error";
  }
  memset(buffer, 0xFF, BUFFER_SIZE);
  sharp_string(message, &font_24x40, 288-24*6, 0);
  sharp_send_buffer(196-pos*44, 40);
}


void draw_number_sci(int pos, double num) {
  int exponent; 
  int64_t mantissa;
  if (num != 0) {
    exponent = (int)floor(log10(fabs(num)));
    mantissa = (int64_t)round(fabs(num)/pow(10, exponent-precision+1));
    if (mantissa > max_mantissa[precision]) {
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
  if (num != 0) {
    exponent = (int)floor(log10(fabs(num)));
    mantissa = (int64_t)round(fabs(num)/pow(10, exponent-precision+1));
    if (mantissa > max_mantissa[precision]) {
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

void draw_number_all(int pos, double num) {
  int i; 
  int exponent; 
  int64_t mantissa;
  int pointpos=1; 
  if (num != 0) {
    exponent = (int)floor(log10(fabs(num)));
    mantissa = (int64_t)round(fabs(num)/pow(10, exponent-precision+1));
    if (mantissa > max_mantissa[precision]) {
      mantissa /= 10;
      exponent += 1; 
    }
    if (exponent < precision && exponent > 0) {
      pointpos = exponent+1; 
      exponent = 0; 
    }
    if (exponent < 0 && exponent > -4) {
      mantissa = (int64_t)round(fabs(num)*pow(10, precision-1));
      pointpos = 1; 
      exponent = 0;
    }
    for (i=0; i<precision; i++) {
      if (mantissa % 10 == 0 && pointpos < precision) {
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
    pointpos = precision;
  }
  draw_number_split(pos, mantissa, exponent, pointpos, 1); 
}

#define DRAWMODE_CLEAR 1
#define DRAWMODE_FLUSH 2

void draw_number(int pos, double num, int mode) {
  if (mode & DRAWMODE_CLEAR) memset(buffer, 0xFF, BUFFER_SIZE);
  if (dispmode == 0) draw_number_all(pos, num);
  if (dispmode == 1) draw_number_sci(pos, num);
  if (dispmode == 2) draw_number_eng(pos, num);
  if (mode & DRAWMODE_FLUSH) sharp_send_buffer(196-(pos % 4)*44, 44);
}

void draw_stack() {
    if (context == CONTEXT_REAL) {
	  	int cat = finite(stack[0]);
    	if (!cat) {
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
	    if (!cat) {
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
}

void draw_input() {
  int i; 
  memset(buffer, 0xFF, BUFFER_SIZE);
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

  draw_stack_name(0);
  if (input.mpos == 0) {
    draw_char(-1, pos, '0', 1);
    if (input.sign) draw_char(-2, pos, '-', 1);
  } else {
    for (i=0; i<input.mpos; i++) {
      draw_char((i-input.mpos), pos, input.mantissa[i]+'0', 1);
    }
    if (input.point>0) {
      draw_decpoint((input.point-input.mpos), pos);
    }
    if (input.sign) draw_char(-(input.mpos+1), pos, '-', 1);
    if (input.expentry == 1) {
      draw_char(0, pos, 0, 1);
      for (i=0; i<3; i++) {
        draw_char((4-i), pos, input.exponent[i]+'0', 1);
      }
      if (input.expsign) draw_char(1, pos, '-', 1);
    }
  }
  sharp_send_buffer(196, 40);
}

void enter_number(char c) {
  if (!input.started) {
    if (!input.enter_pressed && !error_flag) {
      stack_push(0); 
      stack2_push(0);
      draw_stack(); 
    }
    error_flag = 0; 
    input.started = 1;
    input.enter_pressed = 0;
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
  draw_input(); 
}

void enter_backspace() {
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
    draw_input(); 
  } else {
    error_flag = 0; 
    //if (input_uncert == 0) stack[0] = 0;
    //else stack2[0] = 0;
    stack[0] = 0;
    stack2[0] = 0;
    draw_stack(); 
  }
}

void enter_decpoint() {
  if (!input.started) {
    //error_flag = 0;
    if (!input.enter_pressed && !error_flag) { 
        stack_push(0);
        stack2_push(0);
      draw_stack(); 
    }
    error_flag = 0; 
    input.started = 1;
    input.enter_pressed = 0;
    stack2[0] = 0;
  }
  if (input.expentry == 0 && input.point == 0) {
    if (input.mpos == 0) input.mantissa[input.mpos++] = 0; 
    input.point = input.mpos; 
  }
  draw_input(); 
}

void enter_exp() {
  if (!input.started) {
    //error_flag = 0;
    if (!input.enter_pressed && !error_flag) {
      stack_push(0);
      stack2_push(0);
      draw_stack(); 
    }
    error_flag = 0; 
    input.started = 1;
    input.enter_pressed = 0;
    stack2[0] = 0;
  }
  if(input.mpos == 0 || (input.mpos == 1 && input.mantissa[0] == 0)) {
    input.mantissa[0] = 1; 
    input.mpos = 1;
  }
  input.expentry = 1; 
  draw_input(); 
}

void enter_sign() {
  if (input.started) {
    if (input.expentry==0) {
    	if (input_uncert == 0) input.sign = 1-input.sign;
    } else {
      input.expsign = 1-input.expsign; 
    }
    draw_input(); 
  } else {
    if (error_flag) return; 
    stack[0] = -stack[0];
    draw_stack(); 
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
	  draw_error(0, 1);
	  error_flag = 1;
  }
  return(number); 
}

void enter_enter() {
  if (input.started) {
	  if (context != CONTEXT_UNCERT || input_uncert == 0) {
		  stack[0] = convert_input();
	  } else {
		  stack2[0] = convert_input();
	  }
	  clear_input();
  }
  input_uncert = 0;
  if (error_flag) return; 
  input.enter_pressed = 1;
  stack_push(stack[0]);
  stack2_push(stack2[0]);
  draw_stack();
}

void enter_uncert() {
  if (context != CONTEXT_UNCERT) return;
  if (input_uncert == 0) {
	  if (input.started) {
	    stack[0] = convert_input();
	    clear_input();
	  }
	  if (error_flag) return;
	  input_uncert = 1;
	  input.started = 1;
	  draw_stack();
  } else {
	  if (input.started) {
	    stack2[0] = convert_input();
	    clear_input();
	  }
	  if (error_flag) return;
	  input_uncert = 0;
	  draw_stack();
  }
}

void enter_drop() {
  error_flag = 0; 
  if (input.started) {
    clear_input(); 
  }
  input.enter_pressed = 0;
  stack_drop(); 
}

void enter_clear() {
  error_flag = 0;
  if (input.started) {
    clear_input();
  }
  input.enter_pressed = 0;
  clear_stack();
}

void enter_lastx() {
  if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
        clear_input();
  }
  input.enter_pressed = 0;
  if (!error_flag) {
	    stack_push(lastx);
	    stack2_push(lastx2);
  } else {
    error_flag = 0; 
    stack[0] = lastx; 
    stack2[0] = lastx2;
  }
}

void enter_swap_xy() {
  if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
        clear_input();
  }
  if (error_flag) return; 
  input.enter_pressed = 0;
  double tmp = stack[0]; 
  stack[0] = stack[1]; 
  stack[1] = tmp; 
  tmp = stack2[0];
  stack2[0] = stack2[1];
  stack2[1] = tmp;
}

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
#define OPMODE_3TO1 0x8000

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
#define OP_CLEAR 0x6004
#define OP_MPLUS 0x6005
#define OP_MMINUS 0x6006

#define OP_NOP 0x0000

#define OP_PLUS 0x2001
#define OP_MINUS 0x2002
#define OP_MULT 0x2003
#define OP_DIV 0x2004
#define OP_POW 0x2008
#define OP_SQRTX 0x2013
#define OP_CYX 0x2014
#define OP_PYX 0x2015
#define OP_SIGNIF_XY 0x2016

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

#define OP_POLAR 0x3001
#define OP_DESCARTES 0x3002

#define OP_CONST_PI 0x4013

#define OP_PZXY 0x8001

void change_dispmode() {
    if (error_flag) return;
    if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
      clear_input();
    }
    dispmode = (dispmode+1) % 3;
    shift = 0;
    draw_stack();
	draw_status();
}

void change_precision() {
    if (error_flag) return;
    if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
      clear_input();
    }
    if (shift == 1) precision--;
    else precision++;
    if (precision > 10) precision = 3;
    if (precision < 3) precision = 10;
    shift = 0;
    draw_stack();
	draw_status();
}

void change_trigmode() {
    trigmode = (trigmode+1) % 2;
    set_trigconv();
    if (shift == 1) { // Perform conversion
        if (input.started) {
    		if (context != CONTEXT_UNCERT || input_uncert == 0) {
    			stack[0] = convert_input();
    		} else {
    			stack2[0] = convert_input();
    		}
            clear_input();
        }
    	if (trigmode == 0) {
    		// New trig mode is DEGREES
    		stack[0] *= 180./M_PI;
    		stack2[0] *= 180./M_PI;
    	} else {
    		// New trig mode is RADIANS
    		stack[0] /= 180./M_PI;
    		stack2[0] /= 180./M_PI;
    	}
    	draw_stack();
    }
    shift = 0;
	draw_status();
}

void change_context() {
    if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
        clear_input();
    }
	context = 1-context;
	if (context != CONTEXT_UNCERT) {
		input_uncert = 0;
	}
	draw_stack();
	draw_status();
}

void enter_shift() {
	if (shift != 1) shift = 1;
	else shift = 0;
	draw_status();
}

void enter_shift2() {
	if (shift != 2) shift = 2;
	else shift = 0;
	draw_status();
}

void calc_init() {
  trigmode = 0;
  dispmode = 0; 
  shift = 0;
  context = CONTEXT_REAL;
  precision = 10;
  input_uncert = 0;

  set_trigconv(); 

  clear_input(); 
  clear_stack(); 
  draw_status();
  draw_stack(); 
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
		case OP_CLEAR: enter_clear(); break;
		default: break;
	}
}

void apply_func_1to1(uint16_t code) {
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
	case OP_LOGGAMMA: f = lgamma_r(x, &gamma_sign); break;
	case OP_GAMMABETA: f = 1./sqrt(1.-x*x); break;
	case OP_BETAGAMMA: f = sqrt(1.-1./(x*x)); break;
	case OP_ETATHETA: f = -log(tan(trigconv*x/2.)); break;
	case OP_THETAETA: f = atan(exp(-x))*2/trigconv; break;
	case OP_SIGNIF_X: if (context != CONTEXT_UNCERT) return;
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
    	case OP_LOGGAMMA: ef = 0; break;
    	case OP_SIGNIF_X: f = x/ex; break;
    	default: break;
    	}
        stack2[0] = ef;
    }
    stack[0] = f;
}

void apply_func_2to1(uint16_t code) {
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
	case OP_SQRTX: f = pow(y, 1./x); break;
	case OP_CYX: f = exp(lgamma_r(y+1, &gamma_sign) - lgamma_r(x+1, &gamma_sign) - lgamma_r(y-x+1, &gamma_sign)); break;
	case OP_PYX: f = exp(lgamma_r(y+1, &gamma_sign) - lgamma_r(y-x+1, &gamma_sign)); break;
	case OP_SIGNIF_XY: if (context != CONTEXT_UNCERT) return;
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
    	case OP_POW: ef = 0; break;   // Not implemented
    	case OP_SQRTX: ef = 0; break;
    	case OP_SIGNIF_XY: f = (y-x)/sqrt(ex*ex+ey*ey); break;
    	default: break;
    	}
        lastx2 = stack2[0];
    }
    stack_drop();
    stack[0] = f;
    if (context == CONTEXT_UNCERT) stack2[0] = ef;
}

void apply_func_3to1(uint16_t code) {
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
    if (context == CONTEXT_UNCERT) {
    	double ex = stack2[0];
    	double ey = stack2[1];
    	double ez = stack2[2];
    	switch(code) {
    	case OP_PZXY: break;
    	default: break;
    	}
        lastx2 = stack2[0];
    }
    stack_drop();
    stack_drop();
    stack[0] = f;
    if (context == CONTEXT_UNCERT) stack2[0] = ef;
}

void apply_func_2to2(uint16_t code) {
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
    if (context == CONTEXT_UNCERT) {
    	stack2[0] = efx;  // Uncertainties not implemented
    	stack2[1] = efy;
    }
}

void apply_const(uint16_t code) {
	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
	    clear_input();
	}
	input.enter_pressed = 0;
	double f = 0.;
	switch(code) {
	case OP_CONST_PI: f = M_PI; break;
	default: break;
	}

	if (!error_flag) {
	    stack_push(f);
	    stack2_push(0.);
	} else {
	    error_flag = 0;
	    stack[0] = f;
	    stack2[0] = 0;
	}
}

void apply_memory_rcl(uint16_t code) {
	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
	    clear_input();
	}
	input.enter_pressed = 0;
	double f = variables[code & 0x00FF];
	double f2 = variables[(code+1) & 0x00FF];
	if (!error_flag) {
	    stack_push(f);
		if (context == CONTEXT_UNCERT) {
		    stack2_push(f2);
		}
	} else {
	    error_flag = 0;
	    stack[0] = f;
		if (context == CONTEXT_UNCERT) {
		    stack2[0] = f2;
		}
	}
}

void apply_memory_sto(uint16_t code) {
	if (error_flag) return;
	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
	    clear_input();
	}
	input.enter_pressed = 0;
	variables[code & 0x00FF] = stack[0];
	if (context == CONTEXT_UNCERT) {
		variables[(code+1) & 0x00FF] = stack2[0];
	}
}

void apply_memory_plus(uint16_t code) {
	if (error_flag) return;
	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
	    clear_input();
	}
	input.enter_pressed = 0;
	variables[code & 0x00FF] += stack[0];
	if (context == CONTEXT_UNCERT) {
		double em = variables[(code+1) & 0x00FF];
		double ex = stack2[0];
		variables[(code+1) & 0x00FF] = sqrt(ex*ex + em*em);
	}
}

void apply_memory_minus(uint16_t code) {
	if (error_flag) return;
	if (input.started) {
		if (context != CONTEXT_UNCERT || input_uncert == 0) {
			stack[0] = convert_input();
		} else {
			stack2[0] = convert_input();
		}
	    clear_input();
	}
	input.enter_pressed = 0;
	variables[code & 0x00FF] -= stack[0];
	if (context == CONTEXT_UNCERT) {
		double em = variables[(code+1) & 0x00FF];
		double ex = stack2[0];
		variables[(code+1) & 0x00FF] = sqrt(ex*ex + em*em);
	}
}

void apply_op(uint16_t code) {
  if (code == OP_NOP) return;
  uint16_t opmode = code & OPMODE_MASK;
  if (opmode == OPMODE_ENTER) {
	  apply_enter(code);
	  return;
  }
  if (opmode == OPMODE_STACK) {
	  apply_stack(code);
	  draw_stack();
	  input_uncert = 0;
	  return;
  }
  if (opmode == OPMODE_CONST) {
	  apply_const(code);
	  draw_stack();
	  input_uncert = 0;
	  return;
  }
  if (opmode == OPMODE_RCL) {
	  apply_memory_rcl(code);
	  draw_stack();
	  input_uncert = 0;
	  return;
  }
  if (opmode == OPMODE_STO) {
	  apply_memory_sto(code);
	  draw_status();
	  input_uncert = 0;
	  return;
  }
  if (opmode == OPMODE_MPLUS) {
	  apply_memory_plus(code);
	  draw_status();
	  input_uncert = 0;
	  return;
  }
  if (opmode == OPMODE_MMINUS) {
	  apply_memory_minus(code);
	  draw_status();
	  input_uncert = 0;
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
  input.enter_pressed = 0;
  if (opmode == OPMODE_1TO1) apply_func_1to1(code);
  if (opmode == OPMODE_2TO1) apply_func_2to1(code);
  if (opmode == OPMODE_2TO2) apply_func_2to2(code);
  if (opmode == OPMODE_3TO1) apply_func_3to1(code);
  draw_stack();
}

void enter_key(uint16_t code, uint16_t code1, uint16_t code2) {
  if (shift == 0) apply_op(code);
  if (shift == 1) {
	  apply_op(code1);
	  shift = 0;
	  draw_status();
  }
  else if (shift == 2) {
	  apply_op(code2);
	  shift = 0;
	  draw_status();
  }
}

int calc_on_key(int c) {

  switch(c) {
    case  1 : enter_key(OP_ENTER_0, OP_NOP, OP_NOP); break;
    case  7 : enter_key(OP_ENTER_1, OP_CONST_PI, OP_NOP);  break;
    case  8 : enter_key(OP_ENTER_2, OP_NOP, OP_NOP);  break;
    case  9 : enter_key(OP_ENTER_3, OP_NOP, OP_NOP);  break;
    case 13 : enter_key(OP_ENTER_4, OP_NOP, OP_NOP);  break;
    case 14 : enter_key(OP_ENTER_5, OP_NOP, OP_NOP);  break;
    case 15 : enter_key(OP_ENTER_6, OP_NOP, OP_NOP);  break;
    case 19 : enter_key(OP_ENTER_7, OP_ETATHETA, OP_THETAETA);  break;
    case 20 : enter_key(OP_ENTER_8, OP_GAMMABETA, OP_BETAGAMMA);  break;
    case 21 : enter_key(OP_ENTER_9, OP_PZXY, OP_NOP);  break;
    
    case  2 : enter_key(OP_ENTER_SIGN, OP_NOP, OP_NOP);  break;
    case  3 : enter_key(OP_ENTER_DECPOINT, OP_NOP, OP_NOP);  break;
    case  4 : enter_key(OP_ENTER_UNCERT, OP_NOP, OP_NOP); break;
    case  5 : enter_key(OP_ENTER, OP_NOP, OP_NOP);  break;
    case 22 : enter_key(OP_ENTER_EXP, OP_NOP, OP_NOP);  break;
    case 23 : enter_key(OP_ENTER_BACKSPACE, OP_CLEAR, OP_NOP);  break;

    case 16 : enter_key(OP_MULT, OP_NOP, OP_NOP); break;
    case 17 : enter_key(OP_DIV, OP_NOP, OP_NOP); break;
    case 10 : enter_key(OP_PLUS, OP_SIGNIF_X, OP_NOP); break;
    case 11 : enter_key(OP_MINUS, OP_SIGNIF_XY, OP_NOP); break;

    case 25 : enter_key(OP_SQRT, OP_SQR, OP_NOP); break;
    case 26 : enter_key(OP_INV, OP_NOP, OP_NOP); break;
    case 27 : enter_key(OP_ERF, OP_ERFINV, OP_NOP); break;
    case 28 : enter_key(OP_POLAR, OP_DESCARTES, OP_NOP); break;
    case 29 : enter_key(OP_GAMMA, OP_LOGGAMMA, OP_NOP); break;
    case 30 : enter_key(OP_CYX, OP_PYX, OP_NOP); break;

    case 31 : enter_key(OP_POW, OP_SQRTX, OP_NOP); break;
    case 32 : enter_key(OP_LN, OP_EXP, OP_NOP); break;
    case 33 : enter_key(OP_LG, OP_POW10, OP_NOP); break;
    case 34 : enter_key(OP_SIN, OP_ASIN, OP_NOP); break;
    case 35 : enter_key(OP_COS, OP_ACOS, OP_NOP); break;
    case 36 : enter_key(OP_TAN, OP_ATAN, OP_NOP); break;

    case 37 : enter_key(OP_DROP, OP_NOP, OP_NOP); break;
    case 38 : enter_key(OP_SWAP, OP_LASTX, OP_NOP); break;
    case 39 : change_trigmode(); break;
    case 40 : enter_key(OPMODE_MPLUS, OPMODE_MMINUS, OP_NOP); break;
    case 41 : enter_key(OPMODE_RCL, OP_NOP, OP_NOP); break;
    case 42 : enter_key(OPMODE_STO, OP_NOP, OP_NOP); break;

    case 43 : enter_shift(); break;
    case 44 : enter_shift2(); break;
    case 45 : change_dispmode(); break;
    case 46 : change_context(); break;
    case 47 : change_precision(); break;
    case 48 : if (shift == 1) {  // ON/OFF button
  	  shift = 0;
  	  draw_status();
  	  return (0); // OFF
    }

    default: break;
  }

  return(1); 
}
