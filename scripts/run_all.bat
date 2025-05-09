@echo off
echo Running MSVC (ennui) benchmark...
CALL .\scripts\runbenchmarks_msvc.bat

echo Running matlab benchmark...
CALL .\scripts\runbenchmarks_matlab.bat

echo Running MSVC pureClib (no eigen) benchmark...
CALL .\scripts\runbenchmarks_pureClib_msvc.bat

echo "   All scripts completed."
echo "done."
