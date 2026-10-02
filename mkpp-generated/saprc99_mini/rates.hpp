#pragma once
#include <Kokkos_Core.hpp>
namespace mkpp::generated::saprc99_mini::detail {
KOKKOS_INLINE_FUNCTION void compute_rates_chunk_0(
    const double* state, double* rates,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  rates[0] = 5.779235214948339e-34*state[12]*state[13]*state[9] - 1.8183951663749815e-14*state[2]*state[0] - 3.5338644420317084e-17*state[3]*state[0] - 7.98786060795232e-15*state[0]*state[9];
  rates[1] = -1.0*state[1]*jvals[3] + 1.0*state[11]*(4.864965347266905e-32*state[12] + 1.7207046561730112e-12);
  rates[2] = 1.0*state[6]*jvals[1] - 2.6031661982774907e-11*state[2]*state[4] - 1.8183951663749815e-14*state[2]*state[0] + 1.0*state[3]*jvals[0];
  rates[3] = 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[5]/(7.709507080111506e-19*state[12] + 1.0) - 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) + 1.0*state[7]*jvals[2] + 5.206332396554981e-11*state[2]*state[4] + 1.8183951663749815e-14*state[2]*state[0] - 3.5338644420317084e-17*state[3]*state[0] - 1.0*state[3]*jvals[0];
  rates[4] = 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[5]/(7.709507080111506e-19*state[12] + 1.0) - 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]*state[4]/(1.4174820557114162e-18*state[12] + 1.0) + 1.0*state[7]*state[10]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13) - 2.6031661982774907e-11*state[2]*state[4] + 3.5338644420317084e-17*state[3]*state[0];
  rates[5] = -10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[5]/(7.709507080111506e-19*state[12] + 1.0) + 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state[12]), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state[12]*state[3]*state[4]/(1.4174820557114162e-18*state[12] + 1.0);
  rates[6] = -1.0*state[6]*jvals[1];
  rates[7] = -1.0*state[7]*state[10]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13) - 1.0*state[7]*jvals[2];
  rates[8] = 0.0;
  rates[9] = -5.779235214948339e-34*state[12]*state[13]*state[9] + 1.0*state[3]*jvals[0] - 7.98786060795232e-15*state[0]*state[9];
  rates[10] = 2.0*state[1]*jvals[3] - 1.0*state[7]*state[10]*(2.161777301914759e-32*state[12]/(4.2119062982869013e-19*state[12] + 1.0) + 1.0018153870816924e-13) + 1.0*state[7]*jvals[2] + 1.0*state[6]*jvals[1];
  rates[11] = -1.0*state[11]*(4.864965347266905e-32*state[12] + 1.7207046561730112e-12);
  rates[12] = 0.0;
  rates[13] = -5.779235214948339e-34*state[12]*state[13]*state[9] + 1.0*state[11]*(4.864965347266905e-32*state[12] + 1.7207046561730112e-12) + 1.597572121590464e-14*state[0]*state[9];
  rates[14] = 0.0;
  rates[15] = 0.0;
  rates[16] = 0.0;
}
}  // namespace mkpp::generated::saprc99_mini::detail
