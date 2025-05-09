#include <chrono>
#include <functional>
#include <iomanip>
#include <iostream>
#include <vector>

#include "ecef.hpp"
#include "gravitation.hpp"
#include "landmarks.hpp"
#include "wgs84.hpp"

using ennui::Matrix3x3;
using ennui::Vector3;
using ennui::geodetic::gravitation_ecef;
using ennui::geodetic::Wgs84;
using ennui::mechanization::ecef::fwd_pva_S03;

void setup() {
  prop_mean pm = WhiteHouse_mean_prop;
  Vector3 gamma;
  Vector3 position{0., 0., 0.};
  Vector3 velocity{0., 0., 0.};
  Matrix3x3 attitude{{1., 0., 0.}, {0., 1., 0.}, {0., 1., 0.}};
}

inline void propagate(prop_mean &pm, int numcycles) {
  for (int i = 0; i < numcycles; i++) {
    Vector3 gamma = gravitation_ecef<Wgs84>(pm.prior.position);
    fwd_pva_S03<Wgs84>(pm.prior.position, pm.prior.velocity, pm.prior.attitude,
                       gamma, pm.specific_force, pm.angular_rate, pm.dt,
                       pm.prior.position, pm.prior.velocity, pm.prior.attitude);
  }
}

double benchmark(std::function<void(prop_mean &, int)> func,
                 const int warmupCycles, const int benchmarkCycles,
                 const int propagationCycles) {
  // Warmup phase
  prop_mean pm;
  for (int i = 0; i < warmupCycles; ++i) {
    func(pm, propagationCycles);
  }

  // Benchmark phase
  std::chrono::duration<double> totalDuration(0);
  for (int i = 0; i < benchmarkCycles; ++i) {
    // Setup:
    pm = WhiteHouse_mean_prop;
    Vector3 gamma;
    Vector3 position{0., 0., 0.};
    Vector3 velocity{0., 0., 0.};
    Matrix3x3 attitude{{1., 0., 0.}, {0., 1., 0.}, {0., 0., 1.}};

    auto start = std::chrono::high_resolution_clock::now();
    func(pm, propagationCycles);
    auto end = std::chrono::high_resolution_clock::now();
    totalDuration += end - start;
  }

  return totalDuration.count() / benchmarkCycles; // Average time per run
}

int main() {
  int warmupCycles = 25;      // Number of warmup cycles
  int benchmarkCycles = 1000; // Number of benchmark cycles
  std::vector<int> propagationCyclesList = {
      10, 100, 1000, 10000}; // Varying propagation cycles

  int trialsPerCycle = 10;
  std::cout << "BENCHMARK TABLE: ennui_cpp" << std::endl;
  std::cout << "BENCHMARK HEADER: propagationCycles, EnnuiC++" << std::endl;
  for (int propagationCycles : propagationCyclesList) {
    for (int i = 0; i < trialsPerCycle; i++) {
      double averageTime = benchmark(propagate, warmupCycles, benchmarkCycles,
                                     propagationCycles);

      std::cout << "BENCHMARK: " << std::setw(6) << propagationCycles << ", "
                << std::scientific << std::setprecision(5) << averageTime
                << std::endl;
    }
  }

  return 0;
}
