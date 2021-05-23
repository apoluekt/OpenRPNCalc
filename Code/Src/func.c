/*
 * func.c
 *
 *  Created on: Mar 12, 2021
 *      Author: apolu
 */

#include <math.h>

double erfinv(double x) {

  if (x < -1 || x > 1) {
    return NAN;
  } else if (x == 1.0) {
    return INFINITY;
  } else if (x == -1.0) {
    return -INFINITY;
  }

  const  double LN2 = 6.931471805599453094172321214581e-1;

  const  double A0 = 1.1975323115670912564578e0;
  const  double A1 = 4.7072688112383978012285e1;
  const  double A2 = 6.9706266534389598238465e2;
  const  double A3 = 4.8548868893843886794648e3;
  const  double A4 = 1.6235862515167575384252e4;
  const  double A5 = 2.3782041382114385731252e4;
  const  double A6 = 1.1819493347062294404278e4;
  const  double A7 = 8.8709406962545514830200e2;

  const  double B0 = 1.0000000000000000000e0;
  const  double B1 = 4.2313330701600911252e1;
  const  double B2 = 6.8718700749205790830e2;
  const  double B3 = 5.3941960214247511077e3;
  const  double B4 = 2.1213794301586595867e4;
  const  double B5 = 3.9307895800092710610e4;
  const  double B6 = 2.8729085735721942674e4;
  const  double B7 = 5.2264952788528545610e3;

  const  double C0 = 1.42343711074968357734e0;
  const  double C1 = 4.63033784615654529590e0;
  const  double C2 = 5.76949722146069140550e0;
  const  double C3 = 3.64784832476320460504e0;
  const  double C4 = 1.27045825245236838258e0;
  const  double C5 = 2.41780725177450611770e-1;
  const  double C6 = 2.27238449892691845833e-2;
  const  double C7 = 7.74545014278341407640e-4;

  const  double D0 = 1.4142135623730950488016887e0;
  const  double D1 = 2.9036514445419946173133295e0;
  const  double D2 = 2.3707661626024532365971225e0;
  const  double D3 = 9.7547832001787427186894837e-1;
  const  double D4 = 2.0945065210512749128288442e-1;
  const  double D5 = 2.1494160384252876777097297e-2;
  const  double D6 = 7.7441459065157709165577218e-4;
  const  double D7 = 1.4859850019840355905497876e-9;

  const  double E0 = 6.65790464350110377720e0;
  const  double E1 = 5.46378491116411436990e0;
  const  double E2 = 1.78482653991729133580e0;
  const  double E3 = 2.96560571828504891230e-1;
  const  double E4 = 2.65321895265761230930e-2;
  const  double E5 = 1.24266094738807843860e-3;
  const  double E6 = 2.71155556874348757815e-5;
  const  double E7 = 2.01033439929228813265e-7;

  const  double F0 = 1.414213562373095048801689e0;
  const  double F1 = 8.482908416595164588112026e-1;
  const  double F2 = 1.936480946950659106176712e-1;
  const  double F3 = 2.103693768272068968719679e-2;
  const  double F4 = 1.112800997078859844711555e-3;
  const  double F5 = 2.611088405080593625138020e-5;
  const  double F6 = 2.010321207683943062279931e-7;
  const  double F7 = 2.891024605872965461538222e-15;

  double abs_x = fabs(x);

  if (abs_x <= 0.85) {
    double r = 0.180625 - 0.25 * x * x;
    double num = (((((((A7 * r + A6) * r + A5) * r + A4) * r + A3) * r + A2) * r + A1) * r + A0);
    double den = (((((((B7 * r + B6) * r + B5) * r + B4) * r + B3) * r + B2) * r + B1) * r + B0);
    return x * num / den;
  }

  double r = sqrt(LN2 - log(1.0 - abs_x));

  double num, den;
  if (r <= 5.0) {
    r = r - 1.6;
    num = (((((((C7 * r + C6) * r + C5) * r + C4) * r + C3) * r + C2) * r + C1) * r + C0);
    den = (((((((D7 * r + D6) * r + D5) * r + D4) * r + D3) * r + D2) * r + D1) * r + D0);
  } else {
    r = r - 5.0;
    num = (((((((E7 * r + E6) * r + E5) * r + E4) * r + E3) * r + E2) * r + E1) * r + E0);
    den = (((((((F7 * r + F6) * r + F5) * r + F4) * r + F3) * r + F2) * r + F1) * r + F0);
  }

  return copysign(num / den, x);
}
