@echo off
REM Script for building and benchmarking MATLAB interface
REM
REM * target: ennui (MATLAB)
REM * compiler: MSVC
REM * benchmark: .\benchmark\matlab\time_benchmark.m"
REM
REM run from root project folder (not ./scripts)

REM Prepare
REM -----------------------------------------------------------------
REM Check if matlab is available on PATH. Error if not.
set "MATLAB_NAME=matlab"
where %MATLAB_NAME% >nul 2>&1
if %errorlevel% equ 0 (
    echo %MATLAB_NAME% is found in the PATH. Good!
) else (
    echo %MATLAB_NAME% is NOT found in the PATH.
    echo Please ensure that the executable is installed and added to the PATH.
    exit /b 1  REM Exit with an error code
)

REM Remove old build files
echo BAT: Deleting build folder (if it exists)...
call rmdir /s /q .\build
REM TODO: configure MATLAB to build out of source?!?
echo BAT: Deleting matlab dll (if it exists)...
call rmdir /s /q .\benchmark\matlab\mennui

REM Build and install
REM -----------------------------------------------------------------
echo BAT: Install dependencies using conan...
call conan install . -s build_type=Release --build missing --settings:all compiler.cppstd=17

echo BAT: Setup build generator for MATLAB dll using cmake...
call cmake --preset conan-default -DMATLAB_DLL=true

echo BAT: Build custom dll for MATLAB consumption...
call cmake --build . --preset conan-release

echo BAT: Building MATLAB interface dll...
call %MATLAB_NAME% -sd ".\benchmark\matlab" -batch "step1_generate_library_definition"

REM Benchmarks
REM -----------------------------------------------------------------
echo BAT: Run benchmark...
call %MATLAB_NAME% -sd ".\benchmark\matlab" -batch "time_benchmark"

echo "   script complete."
exit /b 0