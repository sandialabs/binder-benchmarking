#pragma once
#include <math.h>

#include "ennui_types.hpp"
#include "rotation.hpp"

// for propagation test
#include "ecef.hpp"
#include "gravitation.hpp"
#include "wgs84.hpp"

namespace ennui {
namespace mechanization {
namespace ecef {

// Perform C++ side fast looping to inertial propagation
// Is alo not representative, as we lose performance for making copies, but gain
// some because we don't actually have a constant ref Also
void propagation_test(ConstRefVector3 &position_minus,
                      ConstRefVector3 &velocity_minus,
                      const Eigen::Ref<const Matrix3x3> &attitude_minus,
                      ConstRefVector3 &specific_force,
                      ConstRefVector3 &angular_rate, double dt,
                      RefVector3 position_plus, RefVector3 velocity_plus,
                      Eigen::Ref<Matrix3x3> attitude_plus, int numcycles) {
  // The const-ness is causing tons of nontrivial with codebase
  // Implementing propagation slightly less efficiently with intermediary copies
  position_plus = position_minus;
  velocity_plus = velocity_minus;
  for (int i = 0; i < numcycles; i++) {
    ConstRefVector3 startpos = position_plus;
    ConstRefVector3 startvel = velocity_plus;
    Vector3 gamma = ennui::geodetic::gravitation_ecef<ennui::geodetic::Wgs84>(
        position_minus);
    fwd_pva_S03<ennui::geodetic::Wgs84>(
        startpos, startvel, attitude_minus, gamma, specific_force, angular_rate,
        dt, position_plus, velocity_plus, attitude_plus);
  }
}

} // namespace ecef
} // namespace mechanization
} // namespace ennui
