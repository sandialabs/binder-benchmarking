@echo off
REM Script for building and benchmarking
REM
REM * target: pureClib
REM * compiler: MSVC
REM * benchmark: benchmark/pureClib/benchmark_variation.py
REM              benchmark/pureClib/rk4_integration_pureCpp.cpp
REN
REM run from root project folder (not ./scripts), in conda environment

REM Prepare
REM -----------------------------------------------------------------
REM Remove old build files
echo SH: Deleting build folder (if it exists)...
call rmdir /s /q .\build

REM Build and install
REM -----------------------------------------------------------------
echo BAT: Build pureClib
cmake  -G "Visual Studio 16 2019" -T ClangCL -S ".\benchmark\pureClib" -B ".\build"
cmake --build ".\build" --config Release

REM Create empty file so python can find libs
echo. > ".\build\Release\__init__.py"

REM Benchmarks
REM -----------------------------------------------------------------
REM Run exe benchmark
echo BAT: C++ benchmark...
call .\build\bin\Release\rk4_integration_cpp

REM Run python benchmark
echo BAT: Running benchmarks from python
python ".\benchmark\pureClib\benchmark_variation.py" .\build\Release\

echo "   script complete."