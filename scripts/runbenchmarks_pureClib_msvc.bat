echo off
REM Script for building and benchmarking
REM
REM * target: pureClib
REM * compiler: MSVC
REM * benchmark: benchmark/pureClib/benchmark_variation.py
REM              benchmark/pureClib/rk4_integration_pureCpp.cpp
REM
REM run from root project folder (not ./scripts), in conda environment

REM Prepare
REM -----------------------------------------------------------------
REM Remove old build files
echo "BAT: Deleting build folder (if it exists)..."
call rmdir /s /q .\build

REM Build and install
REM -----------------------------------------------------------------
echo "BAT: Setup build generator for C++ using cmake..."
cmake -S ".\benchmark\pureClib" -B ".\build"
echo "BAT: Build C++ exe..."
cmake --build ".\build" --config Release

REM Create empty file so python can find libs
echo. > ".\build\Release\__init__.py"

REM Benchmarks
REM -----------------------------------------------------------------
REM Run exe benchmark
echo "BAT: C++ benchmark..."
call .\build\Release\rk4_integration_cpp

echo "BAT: Running benchmarks from python"
python ".\benchmark\pureClib\benchmark_variation.py" .\build\Release\

echo "   script complete."
exit /b 0
