#include "zernike.h"

int maxOrder = 20;
bool VERBOSE = false;


using namespace std;

void computeDescriptors(double* in_array, int x, int y, int z, double** out_array, int* x_out ){

    try{
        
        Grid<double> g(in_array, x, y, z);
        ZernikeDescriptor<double> zd(g, maxOrder);

        int invariantslen = zd.size();
        double* invariants;
        invariants = (double*) malloc( invariantslen*sizeof(double) );

        int c = 0;
        for (auto coef : zd)
        {
            invariants[c] = coef;
            c+=1;
        }
        *out_array = invariants;
        *x_out = invariantslen;

    }catch(bad_alloc &e){
		cerr << "[error] Ran out of memory (" << e.what() << ")." << endl;
		exit(1);
	}catch(runtime_error &e){
		cerr << "[error] An error occurred (" << e.what() << ")." << endl;
		exit(1);
	}catch(exception &e){
		cerr << "[error] An unknown fatal error occurred (" << e.what() << ")." << endl;
		exit(1);
	}
}