/*
 * func.h
 *
 *  Created on: Mar 12, 2021
 *      Author: apolu
 */

#ifndef INC_FUNC_H_
#define INC_FUNC_H_

/* the machine roundoff error */
#define kMACHEP  1.11022302462515654042363166809e-16

/* largest argument for TMath::Exp() */
#define kMAXLOG  709.782712893383973096206318587

#define kBig  4.503599627370496e15
#define kBiginv  2.22044604925031308085e-16


double erfinv(double x);

double igam(double a, double x);

double igamc( double a, double x);

double chisquared_cdf_c(double chi2, double ndf);

double mean_xyz(double x, double y, double z, double ex, double ey, double ez);

double chi2_xyz(double x, double y, double z, double ex, double ey, double ez);

#endif /* INC_FUNC_H_ */
