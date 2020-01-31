
#include "Grid.h"
#include "Sum.h"
#include "ZernikeMoments.h"
#include "util.h"


// zeros everything out-of-bounds
template<typename T>
static void ForceGridToSphere(Grid<T> &grid, Vec3<T> center, T radius)
{
	T xx,yy,zz;
	T sqrLen;

	size_t xdim = grid.sizeX();
	size_t ydim = grid.sizeY();
	size_t zdim = grid.sizeZ();

	// it is easier to work with squared radius, no sqrt required
	T sqrRadius = radius * radius;

	for(size_t z = 0; z < zdim; z++){
		for(size_t y = 0; y < ydim; y++){
			for(size_t x = 0; x < xdim; x++){
				if(grid.get(x,y,z) != (T)0){
					xx = (T)x - center.x;
					yy = (T)y - center.y;
					zz = (T)z - center.z;

					sqrLen = xx*xx + yy*yy + zz*zz;
					if(sqrLen > sqrRadius){
						grid.set(x,y,z,0);
					}
				}
			}
		}
	}
}

template<typename T>
static T ComputeRMSDFromCenter(Grid<T> &grid, Vec3<T> center)
{
	int nVoxels = 0; // number of nonzero voxels
	T sum = 0;

	#pragma omp parallel for collapse(3) reduction(+ : nVoxels, sum)
	for(size_t z=0; z<grid.sizeZ(); ++z){
		for(size_t y=0; y<grid.sizeY(); ++y){
			for(size_t x=0; x<grid.sizeX(); ++x){
				if(grid.get(x, y, z) != 0){
					T mx = (T)x - center.x;
					T my = (T)y - center.y;
					T mz = (T)z - center.z;
					T temp = mx*mx + my*my + mz*mz;

					sum += temp;
					nVoxels++;
				}
			}
		}
	}

	T retval = sqrt(sum/nVoxels);

	return retval;
}

// user 2*rmsd as radius
template<typename T>
static T ComputeRadius(Grid<T> &grid, Vec3<T> center)
{
	return 2 * ComputeRMSDFromCenter(grid, center);
}

// use barycenter as center
template<typename T>
static Vec3<T> ComputeCenter(Grid<T> &grid){
	GeoMoments<T> gm(grid);

	T mass = gm.getMoment(0, 0, 0);

	return {
		gm.getMoment(1, 0, 0) / mass,
		gm.getMoment(0, 1, 0) / mass,
		gm.getMoment(0, 0, 1) / mass
	};
}

template<typename T>
ZernikeDescriptor<T>::ZernikeDescriptor(){};


// consumes the grid to save memory
template<typename T>
ZernikeDescriptor<T>::ZernikeDescriptor(Grid<T> &grid, int order)
{
	maxOrder = order;

	const Vec3<T> center = ComputeCenter(grid);
	T radius = ComputeRadius(grid, center);
	if(radius == 0.0){
		throw std::runtime_error("The specified contour is too low, so no object was found.");
	}
	if(VERBOSE) cerr << "[info] Computed boundary sphere." << endl;

	ForceGridToSphere(grid, center, radius);
	if(VERBOSE) cerr << "[info] Restricted map to bounding sphere." << endl;

	auto gm = GeoMoments<double>(grid, center, 1/radius, order);
	if(VERBOSE) cerr << "[info] Computed geometric moments." << endl;

	auto zm = ZernikeMoments<double>(order, gm);
	if(VERBOSE) cerr << "[info] Computed Zernike moments." << endl;

	for(int n = 0; n <= order; n++){
		for(int l = n % 2; l <= n; l+=2){
			Sum::SumStream<T> sum;
			for(int m = -l; m <= l; m++){
				auto moment = zm.getMoment(n, l, m);
				sum << std::norm(moment);
			}
			invariants.push_back(sqrt(sum.getSum()));
		}
	}

	if(isNaN(invariants)) throw std::runtime_error("Computed a Nan!");
	if(VERBOSE) cerr << "[info] Computed invariants." << endl;
}

template<typename T>
typename vector<T>::iterator ZernikeDescriptor<T>::begin(){
	return invariants.begin();
}

template<typename T>
typename vector<T>::iterator ZernikeDescriptor<T>::end(){
	return invariants.end();
}

template<typename T>
size_t ZernikeDescriptor<T>::size() const{
	return invariants.size();
}

template<typename T>
int ZernikeDescriptor<T>::getOrder() const{
	return maxOrder;
}
