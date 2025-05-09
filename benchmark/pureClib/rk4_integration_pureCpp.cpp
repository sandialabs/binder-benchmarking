// Standard exe, no python binding

#include <array>
#include <chrono>
#include <iostream>
#include <iomanip>


#include "rk4_integration.hpp"

double benchmark_rk4_integration(int num_steps) {
  double time = 0.0;
  double x = 0.0;
  double y = 0.0;
  double h = (20.0 - 0.0) / num_steps;

  auto start = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < 1000; ++i) {
    rk4_integration(x, y, h, 20.0);
  }
  auto end = std::chrono::high_resolution_clock::now();

  std::chrono::duration<double> duration = end - start;
  time = duration.count() / 1000.0;

  return time;
}

int main() {
  std::cout << "Full C++ Test:" << std::endl;
  std::array<int, 4> num_steps_list = {1000, 10000, 100000, 1000000};

  std::cout << "BENCHMARK TABLE: rk4_cpp" << std::endl;
  std::cout << "BENCHMARK HEADER: propagationCycles, rk4_cpp" << std::endl;
  for (int num_steps : num_steps_list) {
    for (int i = 0; i < 10; i++) {
      double time = benchmark_rk4_integration(num_steps);
      std::cout << "BENCHMARK: " << std::setw(6) << num_steps << ", "
                << std::scientific << std::setprecision(5) << time
                << std::endl;
    }
  }

  return 0;
}
