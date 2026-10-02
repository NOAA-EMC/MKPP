#pragma once
#include <Kokkos_Core.hpp>
namespace mkpp::generated::saprc99_mini::detail {
KOKKOS_INLINE_FUNCTION void compute_jacobian_chunk_0(
    const double* state, double* jacobian,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  jacobian[0 * 17 + 0] = -1.8183951663749815e-14*state[2] - 3.5338644420317084e-17*state[3] - 7.98786060795232e-15*state[9];
  jacobian[0 * 17 + 2] = -1.8183951663749815e-14*state[0];
  jacobian[0 * 17 + 3] = -3.5338644420317084e-17*state[0];
  jacobian[0 * 17 + 9] = 5.779235214948339e-34*state[12]*state[13] - 7.98786060795232e-15*state[0];
  jacobian[0 * 17 + 12] = 5.779235214948339e-34*state[13]*state[9];
  jacobian[0 * 17 + 13] = 5.779235214948339e-34*state[12]*state[9];
  jacobian[1 * 17 + 1] = -1.0*jvals[3];
  jacobian[1 * 17 + 11] = 4.864965347266905e-32*state[12] + 1.7207046561730112e-12;
  jacobian[1 * 17 + 12] = 4.864965347266905e-32*state[11];
  jacobian[2 * 17 + 0] = -1.8183951663749815e-14*state[2];
  jacobian[2 * 17 + 2] = -2.6031661982774907e-11*state[4] - 1.8183951663749815e-14*state[0];
  jacobian[2 * 17 + 3] = 1.0*jvals[0];
  jacobian[2 * 17 + 4] = -2.6031661982774907e-11*state[2];
  jacobian[2 * 17 + 6] = 1.0*jvals[1];
  jacobian[3 * 17 + 0] = 1.8183951663749815e-14*state[2] - 3.5338644420317084e-17*state[3];
  jacobian[3 * 17 + 2] = 5.206332396554981e-11*state[4] + 1.8183951663749815e-14*state[0];
  jacobian[3 * 17 + 3] = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) - 3.5338644420317084e-17*state[0] - 1.0*jvals[0];
  jacobian[3 * 17 + 4] = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]/(1.4174820557114162e-18*state[12] + 1.0) + 5.206332396554981e-11*state[2];
  jacobian[3 * 17 + 5] = 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]/(7.709507080111506e-19*state[12] + 1.0);
  jacobian[3 * 17 + 7] = 1.0*jvals[2];
  jacobian[3 * 17 + 12] = -7.953589926046845e-06*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[5]/Kokkos::pow(7.709507080111506e-19*state[12] + 1.0, 2) + 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[5]/(7.709507080111506e-19*state[12] + 1.0) + 16475768690562.62*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[5]*Kokkos::log(7.709507080111506e-19*state[12])/((7.709507080111506e-19*state[12] + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) + 4.015816030220338e-48*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]*state[4]/Kokkos::pow(1.4174820557114162e-18*state[12] + 1.0, 2) - 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[3]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) - 4.524445291995257e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[3]*state[4]*Kokkos::log(1.4174820557114162e-18*state[12])/((1.4174820557114162e-18*state[12] + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0)));
  jacobian[4 * 17 + 0] = 3.5338644420317084e-17*state[3];
  jacobian[4 * 17 + 2] = -2.6031661982774907e-11*state[4];
  jacobian[4 * 17 + 3] = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) + 3.5338644420317084e-17*state[0];
  jacobian[4 * 17 + 4] = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]/(1.4174820557114162e-18*state[12] + 1.0) - 2.6031661982774907e-11*state[2];
  jacobian[4 * 17 + 5] = 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]/(7.709507080111506e-19*state[12] + 1.0);
  jacobian[4 * 17 + 7] = 1.0*state[10]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13);
  jacobian[4 * 17 + 10] = 1.0*state[7]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13);
  jacobian[4 * 17 + 12] = -7.953589926046845e-06*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[5]/Kokkos::pow(7.709507080111506e-19*state[12] + 1.0, 2) + 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[5]/(7.709507080111506e-19*state[12] + 1.0) + 16475768690562.62*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[5]*Kokkos::log(7.709507080111506e-19*state[12])/((7.709507080111506e-19*state[12] + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) + 4.015816030220338e-48*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]*state[4]/Kokkos::pow(1.4174820557114162e-18*state[12] + 1.0, 2) - 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[3]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) - 4.524445291995257e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[3]*state[4]*Kokkos::log(1.4174820557114162e-18*state[12])/((1.4174820557114162e-18*state[12] + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) + 1.0*state[7]*state[10]*(-9.105203433428452e-51*state[12]/Kokkos::pow(4.2119062982869013e-19*state[12] + 1.0, 2) + 2.161777301914759e-32/(4.2119062982869013e-19*state[12] + 1.0));
  jacobian[5 * 17 + 3] = 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[4]/(1.4174820557114162e-18*state[12] + 1.0);
  jacobian[5 * 17 + 4] = 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]/(1.4174820557114162e-18*state[12] + 1.0);
  jacobian[5 * 17 + 5] = -10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]/(7.709507080111506e-19*state[12] + 1.0);
  jacobian[5 * 17 + 12] = 7.953589926046845e-06*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[5]/Kokkos::pow(7.709507080111506e-19*state[12] + 1.0, 2) - 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[5]/(7.709507080111506e-19*state[12] + 1.0) - 16475768690562.62*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[5]*Kokkos::log(7.709507080111506e-19*state[12])/((7.709507080111506e-19*state[12] + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) - 4.015816030220338e-48*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]*state[4]/Kokkos::pow(1.4174820557114162e-18*state[12] + 1.0, 2) + 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[3]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) + 4.524445291995257e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[3]*state[4]*Kokkos::log(1.4174820557114162e-18*state[12])/((1.4174820557114162e-18*state[12] + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0)));
  jacobian[6 * 17 + 6] = -1.0*jvals[1];
  jacobian[7 * 17 + 7] = -1.0*state[10]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13) - 1.0*jvals[2];
  jacobian[7 * 17 + 10] = -1.0*state[7]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13);
  jacobian[7 * 17 + 12] = -1.0*state[7]*state[10]*(-9.105203433428452e-51*state[12]/Kokkos::pow(4.2119062982869013e-19*state[12] + 1.0, 2) + 2.161777301914759e-32/(4.2119062982869013e-19*state[12] + 1.0));
  jacobian[9 * 17 + 0] = -7.98786060795232e-15*state[9];
  jacobian[9 * 17 + 3] = 1.0*jvals[0];
  jacobian[9 * 17 + 9] = -5.779235214948339e-34*state[12]*state[13] - 7.98786060795232e-15*state[0];
  jacobian[9 * 17 + 12] = -5.779235214948339e-34*state[13]*state[9];
  jacobian[9 * 17 + 13] = -5.779235214948339e-34*state[12]*state[9];
  jacobian[10 * 17 + 1] = 2.0*jvals[3];
  jacobian[10 * 17 + 6] = 1.0*jvals[1];
  jacobian[10 * 17 + 7] = -1.0*state[10]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13) + 1.0*jvals[2];
  jacobian[10 * 17 + 10] = -1.0*state[7]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13);
  jacobian[10 * 17 + 12] = -1.0*state[7]*state[10]*(-9.105203433428452e-51*state[12]/Kokkos::pow(4.2119062982869013e-19*state[12] + 1.0, 2) + 2.161777301914759e-32/(4.2119062982869013e-19*state[12] + 1.0));
  jacobian[11 * 17 + 11] = -4.864965347266905e-32*state[12] - 1.7207046561730112e-12;
  jacobian[11 * 17 + 12] = -4.864965347266905e-32*state[11];
  jacobian[13 * 17 + 0] = 1.597572121590464e-14*state[9];
  jacobian[13 * 17 + 9] = -5.779235214948339e-34*state[12]*state[13] + 1.597572121590464e-14*state[0];
  jacobian[13 * 17 + 11] = 4.864965347266905e-32*state[12] + 1.7207046561730112e-12;
  jacobian[13 * 17 + 12] = 4.864965347266905e-32*state[11] - 5.779235214948339e-34*state[13]*state[9];
  jacobian[13 * 17 + 13] = -5.779235214948339e-34*state[12]*state[9];
}
}  // namespace mkpp::generated::saprc99_mini::detail
