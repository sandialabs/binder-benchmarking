#!/usr/bin/bash
#
# Build and run benchmarks
#
# * target: ennui
# * compiler: gcc
# * benchmark: benchmark/python/time_benchmark.py
#              benchmark/exe/benchmark_variation.cpp
#
# Run from root project folder (not ./scripts)
#
# Optionally specify "memory" to run valgrind memory benchmarks.

# Prepare
# -----------------------------------------------------------------
# Remove old build files
echo "SH: Deleting build folder (if it exists)..."
rm -rf ./build
# Install dependencies
echo "SH: Install dependencies using conan..."
conan install . -s build_type=Release --build missing --settings:all compiler=gcc --settings:all compiler.version=11 --settings:all compiler.cppstd=17

# Build and install
# -----------------------------------------------------------------
# Install python packages
echo "SH: Install python package (ennui with custom bindings)"
pip install .
# If cmake cannot find python packages, e.g. python/pip inconsistencies, can add to path explicitly
#cmake --preset conan-release -DPYTHON_MODULE=true -DCMAKE_SYSTEM_PREFIX_PATH="/usr/local/lib/python3.9/site-packages/"

# Build cpp-only exe
echo "SH: Setup build generator for C++ using cmake..."
cmake --preset conan-release
echo "SH: Build C++ exe..."
cmake --build . --preset conan-release --target cpp_speedtest

# Actual benchmarking
# -----------------------------------------------------------------
# Run python benchmark
echo "SH: python benchmark..."
python3 benchmark/python/time_benchmark.py
# Run exe benchmark
echo "SH: C++ benchmark..."
build/Release/bin/cpp_speedtest

# Optionally run memory check. Must pass argument: memory
if [ $# -eq 0 ]; then
    echo "Skipping memory test."
    exit 1
fi
case $1 in
    memory)
        echo "Running memory benchmark (slow)..."
        cd benchmark/MemoryBenchmarks
        PYTHONMALLOC=malloc valgrind --tool=massif --peak-inaccuracy=0.01 --pages-as-heap=no --stacks=yes --massif-out-file="gcc_nanobind_Cloop.out" --time-unit=B --max-snapshots=200 python3 nanobind_Cloop.py
        PYTHONMALLOC=malloc valgrind --tool=massif --peak-inaccuracy=0.01 --pages-as-heap=no --stacks=yes --massif-out-file="gcc_nanobind_pythonloop.out" --time-unit=B --max-snapshots=200 python3 nanobind_pythonloop.py
        PYTHONMALLOC=malloc valgrind --tool=massif --peak-inaccuracy=0.01 --pages-as-heap=no --stacks=yes --massif-out-file="gcc_pybind11_Cloop.out" --time-unit=B --max-snapshots=200 python3 pybind11_Cloop.py
        PYTHONMALLOC=malloc valgrind --tool=massif --peak-inaccuracy=0.01 --pages-as-heap=no --stacks=yes --massif-out-file="gcc_pybind11_pythonloop.out" --time-unit=B --max-snapshots=200 python3 pybind11_pythonloop.py
        PYTHONMALLOC=malloc valgrind --tool=massif --peak-inaccuracy=0.01 --pages-as-heap=no --stacks=yes --massif-out-file="gcc_numpy_loop.out" --time-unit=B --max-snapshots=200 python3 numpy_loop.py
        PYTHONMALLOC=malloc valgrind --tool=massif --peak-inaccuracy=0.01 --pages-as-heap=no --stacks=yes --massif-out-file="gcc_donothing.out" --time-unit=B --max-snapshots=200 python3 donothing.py
        cd ../..
        ;;
    *)
        echo "Invalid option: $1"
        echo "Skipping memory test."
        exit 1
        ;;
esac

echo "   script complete."
exit 0