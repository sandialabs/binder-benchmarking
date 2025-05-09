@echo off
REM Script for building and benchmarking python and C++ on Windows MSVC
REM
REM * target: ennui
REM * compiler: MSVC
REM * benchmark: .\benchmark\python\time_benchmark.py
REM              .\exe\speedtest_variation.cpp
REM
REM run from root project folder (not ./scripts), in conda environment

REM Prepare
REM -----------------------------------------------------------------
REM Remove old build files
echo BAT: Deleting build folder (if it exists)...
call rmdir /s /q .\build
echo BAT: Install dependencies using conan...
call conan install . -s build_type=Release --build missing --settings:all compiler.cppstd=17

REM Build and install
REM -----------------------------------------------------------------
echo BAT: Install python package (ennui with custom bindings)
pip install .

echo BAT: Setup build generator for C++ using cmake...
call cmake --preset conan-default

echo BAT: Build C++ exe...
call cmake --build . --preset conan-release --target cpp_speedtest

REM Actual benchmarking
REM -----------------------------------------------------------------
echo BAT: python benchmark...
call python benchmark/python/time_benchmark.py

echo BAT: C++ benchmark...
call .\build\bin\Release\cpp_speedtest

echo "   script complete."
exit /b 0