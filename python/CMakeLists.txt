# Import Eigen3
find_package(Eigen3 CONFIG REQUIRED)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module
OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind
find_package(nanobind CONFIG REQUIRED)

# Import pybind11
find_package(pybind11 CONFIG REQUIRED PATHS ${pybind11_ROOT})

# We are now ready to compile the actual extension modules
nanobind_add_module(
  # Name of the nanobind extension
  pyennui

  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI

  # Build libnanobind statically and merge it into the
  # extension (which itself remains a shared library)
  #
  # If your project builds multiple extensions, you can
  # replace this flag by NB_SHARED to conserve space by
  # reusing a shared libnanobind across libraries
  NB_STATIC

  LTO
  NOMINSIZE

  # Source code goes here
  pyennui.cpp
)

pybind11_add_module(
  # Name of the pybind11 extension
  pyennui_pybind11

  # Source code goes here
  pyennui_pybind11.cpp
)

# Link Eigen for both extensions
target_link_libraries(pyennui PUBLIC Eigen3::Eigen
    ${CMAKE_PROJECT_NAME}::types
    ${CMAKE_PROJECT_NAME}::math
    ${CMAKE_PROJECT_NAME}::mechanization
    ${CMAKE_PROJECT_NAME}::geodetic
    ${CMAKE_PROJECT_NAME}::batch_call)

target_link_libraries(pyennui_pybind11 PRIVATE Eigen3::Eigen
    ${CMAKE_PROJECT_NAME}::types
    ${CMAKE_PROJECT_NAME}::math
    ${CMAKE_PROJECT_NAME}::mechanization
    ${CMAKE_PROJECT_NAME}::geodetic
    ${CMAKE_PROJECT_NAME}::batch_call
    pybind11::module)

install(TARGETS pyennui LIBRARY DESTINATION .)
install(TARGETS pyennui_pybind11 LIBRARY DESTINATION .)
