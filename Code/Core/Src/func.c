/*
 * func.c
 *
 *  Implementation of some special functions missing in the C math library.
 *  Links to original sources are given in the comments below.
 *
 *  Created on: Mar 12, 2021
 *      Author: apolu
 */

#include <math.h>

#include "func.h"

/*
  Inverse erf implementation from https://github.com/lakshayg/erfinv
*/ 
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

// Implementation of igam, igamc functions taken from CEPHES library
// (https://www.netlib.org/cephes/doubldoc.html)
// via CERN ROOT framework



 // incomplete gamma function (complement integral)
 //  igamc(a,x)   =   1 - igam(a,x)
 //
 //                            inf.
 //                              -
 //                     1       | |  -t  a-1
 //               =   -----     |   e   t   dt.
 //                    -      | |
 //                   | (a)    -
 //                             x
 //
 //

 // In this implementation both arguments must be positive.
 // The integral is evaluated by either a power series or
 // continued fraction expansion, depending on the relative
 // values of a and x.

double igamc( double a, double x )
{

    double ans, ax, c, yc, r, t, y, z;
    double pk, pkm1, pkm2, qk, qkm1, qkm2;
    int gsign;

    // LM: for negative values returns 0.0
    // This is correct if a is a negative integer since Gamma(-n) = +/- inf
    if (a <= 0)  return 0.0;

    if (x <= 0) return 1.0;

    if( (x < 1.0) || (x < a) )
       return( 1.0 - igam(a,x) );

    ax = a * log(x) - x - lgamma_r(a, &gsign);
    if( ax < -kMAXLOG )
       return( 0.0 );

    ax = exp(ax);

 /* continued fraction */
    y = 1.0 - a;
    z = x + y + 1.0;
    c = 0.0;
    pkm2 = 1.0;
    qkm2 = x;
    pkm1 = x + 1.0;
    qkm1 = z * x;
    ans = pkm1/qkm1;

    do
    {
       c += 1.0;
       y += 1.0;
       z += 2.0;
       yc = y * c;
       pk = pkm1 * z  -  pkm2 * yc;
       qk = qkm1 * z  -  qkm2 * yc;
       if(qk)
       {
          r = pk/qk;
          t = fabs( (ans - r)/r );
          ans = r;
       }
       else
          t = 1.0;
       pkm2 = pkm1;
       pkm1 = pk;
       qkm2 = qkm1;
       qkm1 = qk;
       if( fabs(pk) > kBig )
       {
          pkm2 *= kBiginv;
          pkm1 *= kBiginv;
          qkm2 *= kBiginv;
          qkm1 *= kBiginv;
       }
    }
    while( t > kMACHEP );

    return( ans * ax );
 }

 /* left tail of incomplete gamma function:
  *
  *          inf.      k
  *   a  -x   -       x
  *  x  e     >   ----------
  *           -     -
  *          k=0   | (a+k+1)
  *
  */

double igam( double a, double x )
{
    double ans, ax, c, r;
    int gsign;

    // LM: for negative values returns 1.0 instead of zero
    // This is correct if a is a negative integer since Gamma(-n) = +/- inf
    if (a <= 0)  return 1.0;

    if (x <= 0)  return 0.0;

    if( (x > 1.0) && (x > a ) )
       return( 1.0 - igamc(a,x) );

 /* Compute  x**a * exp(-x) / gamma(a)  */
    ax = a * log(x) - x - lgamma_r(a, &gsign);
    if( ax < -kMAXLOG )
       return( 0.0 );

    ax = exp(ax);

 /* power series */
    r = a;
    c = 1.0;
    ans = 1.0;

    do
    {
       r += 1.0;
       c *= x/r;
       ans += c;
    }
    while( c/ans > kMACHEP );

    return( ans * ax/a );
}

double chisquared_cdf_c(double chi2, double ndf)
{
   return igamc ( 0.5*ndf , 0.5*chi2 );
}

void stat_mean(double *x, double *ex, int size, double* mean, double* emean)
{
   double esum = 0.;
   double sum = 0.;
   int zero_error = 0;
   int nonzero_error = 0;
   for (int i=0; i<size; i++) {
	   double v = x[i];
	   double ev = ex[i];
	   if (ev == 0. ) {
		   sum += v;
		   esum += 1.;
		   zero_error = 1;
	   } else {
		   sum += v/ev/ev;
		   esum += 1./ev/ev;
		   nonzero_error = 1;
	   }
   }
   if (zero_error && nonzero_error) {
	   *mean = NAN;
	   return;
   }
   if (zero_error) {
	   *mean = sum/esum;
       *emean = 0;
       return;
   }
   if (nonzero_error) {
	   *mean = sum/esum;
	   *emean = 1./sqrt(esum);
	   return;
   }
   *mean = NAN;
}

double stat_chi2(double *x, double *ex, int size)
{
	double mean=0;
	double emean=0;
	stat_mean(x, ex, size, &mean, &emean);
	if (!finite(mean)) return NAN;
	double sum = 0.;
	for (int i=0; i<size; i++) {
		double v = x[i];
		double ev = ex[i];
		sum += pow(v - mean, 2)/ev/ev;
	}
	return sum;
}
