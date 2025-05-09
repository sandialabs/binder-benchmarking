// Common RK4 integration functions

#include "rk4_integration.hpp"

double f(double x, double y) { return x * x; }

//note, setting variables to volatile to prevent compiler pre-computation of values
//Volatile may prevent optimizations (like vectorization).  Improved optimization would be to have the integration function defined externally to prevent the compiler from precomputing at compile time, but also allowing vector optimization.
double rk4_integration(double x0, double y0, double h, double xf) {
  double x = x0;
  double y = y0;

  while (x < xf) {
    volatile double k1 = h * f(x, y);
    volatile double k2 = h * f(x + h / 2, y + k1 / 2);
    volatile double k3 = h * f(x + h / 2, y + k2 / 2);
    volatile double k4 = h * f(x + h, y + k3);

    y += (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    x += h;
  }

  return y;
}

double rk4_integration_single_step(double x, double y, double h) {
  double k1 = h * f(x, y);
  double k2 = h * f(x + h / 2, y + k1 / 2);
  double k3 = h * f(x + h / 2, y + k2 / 2);
  double k4 = h * f(x + h, y + k3);

  double result = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
  return result;
}
