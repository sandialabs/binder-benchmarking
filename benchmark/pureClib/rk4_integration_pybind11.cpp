// Pybind11-specific wrapper

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "rk4_integration.hpp"

namespace py = pybind11;

PYBIND11_MODULE(rk4_integration_pybind11, m) {
  m.def("rk4_integration", &rk4_integration,
        "Runge-Kutta 4th order integration");
  m.def("rk4_integration_single_step", &rk4_integration_single_step,
        "Runge-Kutta 4th order single step");
}
