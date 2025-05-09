// Nanobind-specific wrapper

#include "rk4_integration.hpp"
#include <nanobind/nanobind.h>

namespace nb = nanobind;

NB_MODULE(rk4_integration_nanobind, m) {
  m.def("rk4_integration", &rk4_integration,
        "Runge-Kutta 4th order integration");
  m.def("rk4_integration_single_step", &rk4_integration_single_step,
        "Runge-Kutta 4th order single step");
}
