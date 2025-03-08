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

void stat_mean(double *x, double *ex, int size, double *mean, double *emean);

double stat_chi2(double *x, double *ex, int size);

#endif /* INC_FUNC_H_ */
