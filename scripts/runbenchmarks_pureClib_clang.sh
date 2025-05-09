#!/usr/bin/bash
#
# Build and run benchmarks
#
# * target: pureClib
# * compiler: clang
# * benchmark: benchmark/pureClib/benchmark_variation.py
#              benchmark/pureClib/rk4_integration_pureCpp.cpp
#
# Run from root project folder (not ./scripts)

# Prepare
# -----------------------------------------------------------------
# Remove old build files
echo "SH: Deleting build folder (if it exists)..."
rm -rf ./build

# Build and install
# -----------------------------------------------------------------
echo "SH: Setup build generator for C++ using cmake..."
cmake -S "./benchmark/pureClib" -B "./build" -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++
echo "SH: Build C++ exe..."
make -C "build" -j

# Actual benchmarking
# -----------------------------------------------------------------
# Run exe benchmark
echo "SH: Running C++ benchmark"
./build/rk4_integration_cpp

# Run python benchmark
echo "SH: Running benchmarks from python"
python3 "./benchmark/pureClib/benchmark_variation.py" ./build/

echo "   script complete."
exit 0