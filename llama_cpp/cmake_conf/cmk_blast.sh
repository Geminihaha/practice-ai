cmake .. -G Ninja \
	-B build-android \
	-DGGML_CLBLAST=ON \
	-DCMAKE_C_FLAGS="-O3 -march=armv8.2-a+dotprod -mtune=native" \
	-DCMAKE_CXX_FLAGS="-O3 -march=armv8.2-a+dotprod -mtune=native" \
	-DGGML_OPENMP=OFF \
	-DGGML_NATIVE=OFF \
	-DCMAKE_BUILD_TYPE=Release
