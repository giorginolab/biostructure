PYTHON_DIR =   #  /home/manzumbado/miniconda3/envs/visual/include/python3.6m/ 
CXX = g++
CFLAGS = -std=c++11 -fpic  $(shell python3-config --includes) $(shell numpy-config --cflags)
LDFLAGS = $(shell python3-config --ldflags)
OBJ = _zernike.so

.PHONY : clean

$(OBJ) : 
	swig -c++ -python  -o zernike_wrap.cpp zernike.i
	$(CXX) $(CFLAGS) -c zernike_wrap.cpp -o zernike_wrap.o 
	$(CXX) $(CFLAGS) -c zernike.cpp -o zernike.o 
	$(CXX) -shared $(LDFLAGS) zernike_wrap.o zernike.o -o $(OBJ) 
	rm -vf zernike_wrap.o zernike.o
	cp $(OBJ) ../../utils/
	
	
	
	
clean :
	rm -vf $(OBJ)zernike_wrap.o zernike.py