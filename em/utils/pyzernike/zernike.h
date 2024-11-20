#ifndef ZERNIKE_H
#define ZERNIKE_H

#include "Grid.h"
#include "ZernikeDescriptor.h"
#include "util.h"
#include <stdexcept>


void computeDescriptors(double* in_array, int x, int y, int z, double** out_array, int* x_out);

#endif