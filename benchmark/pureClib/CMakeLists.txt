cmake_minimum_required(VERSION 3.12)
project(rk4_integration)

set(CMAKE_CXX_STANDARD 17)


# Import all Python components potentially needed by nanobind
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module
OPTIONAL_COMPONENTS Development.SABIModule)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)

find_package(nanobind CONFIG REQUIRED PATHS ${nanobind_ROOT})


# Import pybind11
find_package(Python3 REQUIRED)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE pybind11_ROOT)

find_package(pybind11 CONFIG REQUIRED PATHS ${pybind11_ROOT})

pybind11_add_module(rk4_integration_pybind11 rk4_integration_pybind11.cpp rk4_integration.cpp)
nanobind_add_module(rk4_integration_nanobind
LTO
NOMINSIZE
rk4_integration_nanobind.cpp rk4_integration.cpp)


#Pure C++ benchmark
add_executable(rk4_integration_cpp rk4_integration_pureCpp.cpp rk4_integration.cpp)
