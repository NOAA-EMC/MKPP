#pragma once
#include <Kokkos_Core.hpp>
#include "accessor.hpp"
namespace mkpp::generated::saprc99_mini::detail {
KOKKOS_INLINE_FUNCTION void compute_jacobian_chunk_0(
  StrideView<const double, 1> state, StrideView<double, 2> jacobian,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  jacobian(0, 0) = -1.8183951663749815e-14*state(2) - 3.5338644420317084e-17*state(3) - 7.98786060795232e-15*state(9);
  jacobian(0, 2) = -1.8183951663749815e-14*state(0);
  jacobian(0, 3) = -3.5338644420317084e-17*state(0);
  jacobian(0, 9) = 5.779235214948339e-34*state(12)*state(13) - 7.98786060795232e-15*state(0);
  jacobian(0, 12) = 5.779235214948339e-34*state(13)*state(9);
  jacobian(0, 13) = 5.779235214948339e-34*state(12)*state(9);
  jacobian(1, 1) = -1.0*jvals[3];
  jacobian(1, 11) = 4.864965347266905e-32*state(12) + 1.7207046561730112e-12;
  jacobian(1, 12) = 4.864965347266905e-32*state(11);
  jacobian(2, 0) = -1.8183951663749815e-14*state(2);
  jacobian(2, 2) = -2.6031661982774907e-11*state(4) - 1.8183951663749815e-14*state(0);
  jacobian(2, 3) = 1.0*jvals[0];
  jacobian(2, 4) = -2.6031661982774907e-11*state(2);
  jacobian(2, 6) = 1.0*jvals[1];
  jacobian(3, 0) = 1.8183951663749815e-14*state(2) - 3.5338644420317084e-17*state(3);
  jacobian(3, 2) = 5.206332396554981e-11*state(4) + 1.8183951663749815e-14*state(0);
  jacobian(3, 3) = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(4)/(1.4174820557114162e-18*state(12) + 1.0) - 3.5338644420317084e-17*state(0) - 1.0*jvals[0];
  jacobian(3, 4) = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(3)/(1.4174820557114162e-18*state(12) + 1.0) + 5.206332396554981e-11*state(2);
  jacobian(3, 5) = 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)/(7.709507080111506e-19*state(12) + 1.0);
  jacobian(3, 7) = 1.0*jvals[2];
  jacobian(3, 12) = -7.953589926046845e-06*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(5)/Kokkos::pow(7.709507080111506e-19*state(12) + 1.0, 2) + 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(5)/(7.709507080111506e-19*state(12) + 1.0) + 16475768690562.62*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(5)*Kokkos::log(7.709507080111506e-19*state(12))/((7.709507080111506e-19*state(12) + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) + 4.015816030220338e-48*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(3)*state(4)/Kokkos::pow(1.4174820557114162e-18*state(12) + 1.0, 2) - 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(3)*state(4)/(1.4174820557114162e-18*state(12) + 1.0) - 4.524445291995257e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(3)*state(4)*Kokkos::log(1.4174820557114162e-18*state(12))/((1.4174820557114162e-18*state(12) + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0)));
  jacobian(4, 0) = 3.5338644420317084e-17*state(3);
  jacobian(4, 2) = -2.6031661982774907e-11*state(4);
  jacobian(4, 3) = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(4)/(1.4174820557114162e-18*state(12) + 1.0) + 3.5338644420317084e-17*state(0);
  jacobian(4, 4) = -2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(3)/(1.4174820557114162e-18*state(12) + 1.0) - 2.6031661982774907e-11*state(2);
  jacobian(4, 5) = 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)/(7.709507080111506e-19*state(12) + 1.0);
  jacobian(4, 7) = 1.0*state(10)*(2.161777301914759e-32*state(12)/(4.2119062982869013e-19*state(12) + 1.0) + 1.0018153870816924e-13);
  jacobian(4, 10) = 1.0*state(7)*(2.161777301914759e-32*state(12)/(4.2119062982869013e-19*state(12) + 1.0) + 1.0018153870816924e-13);
  jacobian(4, 12) = -7.953589926046845e-06*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(5)/Kokkos::pow(7.709507080111506e-19*state(12) + 1.0, 2) + 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(5)/(7.709507080111506e-19*state(12) + 1.0) + 16475768690562.62*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(5)*Kokkos::log(7.709507080111506e-19*state(12))/((7.709507080111506e-19*state(12) + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) + 4.015816030220338e-48*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(3)*state(4)/Kokkos::pow(1.4174820557114162e-18*state(12) + 1.0, 2) - 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(3)*state(4)/(1.4174820557114162e-18*state(12) + 1.0) - 4.524445291995257e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(3)*state(4)*Kokkos::log(1.4174820557114162e-18*state(12))/((1.4174820557114162e-18*state(12) + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) + 1.0*state(7)*state(10)*(-9.105203433428452e-51*state(12)/Kokkos::pow(4.2119062982869013e-19*state(12) + 1.0, 2) + 2.161777301914759e-32/(4.2119062982869013e-19*state(12) + 1.0));
  jacobian(5, 3) = 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(4)/(1.4174820557114162e-18*state(12) + 1.0);
  jacobian(5, 4) = 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(3)/(1.4174820557114162e-18*state(12) + 1.0);
  jacobian(5, 5) = -10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)/(7.709507080111506e-19*state(12) + 1.0);
  jacobian(5, 12) = 7.953589926046845e-06*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(5)/Kokkos::pow(7.709507080111506e-19*state(12) + 1.0, 2) - 10316599807742.686*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(5)/(7.709507080111506e-19*state(12) + 1.0) - 16475768690562.62*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(5)*Kokkos::log(7.709507080111506e-19*state(12))/((7.709507080111506e-19*state(12) + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(7.709507080111506e-19*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0))) - 4.015816030220338e-48*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(12)*state(3)*state(4)/Kokkos::pow(1.4174820557114162e-18*state(12) + 1.0, 2) + 2.833063045870341e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(3)*state(4)/(1.4174820557114162e-18*state(12) + 1.0) + 4.524445291995257e-30*Kokkos::pow(0.45, 1.0/(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0))*state(3)*state(4)*Kokkos::log(1.4174820557114162e-18*state(12))/((1.4174820557114162e-18*state(12) + 1.0)*Kokkos::pow(Kokkos::pow(Kokkos::log(1.4174820557114162e-18*state(12)), 2)/(Kokkos::log(10.0) * Kokkos::log(10.0)) + 1.0, 2)*(Kokkos::log(10.0) * Kokkos::log(10.0)));
  jacobian(6, 6) = -1.0*jvals[1];
  jacobian(7, 7) = -1.0*state(10)*(2.161777301914759e-32*state(12)/(4.2119062982869013e-19*state(12) + 1.0) + 1.0018153870816924e-13) - 1.0*jvals[2];
  jacobian(7, 10) = -1.0*state(7)*(2.161777301914759e-32*state(12)/(4.2119062982869013e-19*state(12) + 1.0) + 1.0018153870816924e-13);
  jacobian(7, 12) = -1.0*state(7)*state(10)*(-9.105203433428452e-51*state(12)/Kokkos::pow(4.2119062982869013e-19*state(12) + 1.0, 2) + 2.161777301914759e-32/(4.2119062982869013e-19*state(12) + 1.0));
  jacobian(9, 0) = -7.98786060795232e-15*state(9);
  jacobian(9, 3) = 1.0*jvals[0];
  jacobian(9, 9) = -5.779235214948339e-34*state(12)*state(13) - 7.98786060795232e-15*state(0);
  jacobian(9, 12) = -5.779235214948339e-34*state(13)*state(9);
  jacobian(9, 13) = -5.779235214948339e-34*state(12)*state(9);
  jacobian(10, 1) = 2.0*jvals[3];
  jacobian(10, 6) = 1.0*jvals[1];
  jacobian(10, 7) = -1.0*state(10)*(2.161777301914759e-32*state(12)/(4.2119062982869013e-19*state(12) + 1.0) + 1.0018153870816924e-13) + 1.0*jvals[2];
  jacobian(10, 10) = -1.0*state(7)*(2.161777301914759e-32*state(12)/(4.2119062982869013e-19*state(12) + 1.0) + 1.0018153870816924e-13);
  jacobian(10, 12) = -1.0*state(7)*state(10)*(-9.105203433428452e-51*state(12)/Kokkos::pow(4.2119062982869013e-19*state(12) + 1.0, 2) + 2.161777301914759e-32/(4.2119062982869013e-19*state(12) + 1.0));
  jacobian(11, 11) = -4.864965347266905e-32*state(12) - 1.7207046561730112e-12;
  jacobian(11, 12) = -4.864965347266905e-32*state(11);
  jacobian(13, 0) = 1.597572121590464e-14*state(9);
  jacobian(13, 9) = -5.779235214948339e-34*state(12)*state(13) + 1.597572121590464e-14*state(0);
  jacobian(13, 11) = 4.864965347266905e-32*state(12) + 1.7207046561730112e-12;
  jacobian(13, 12) = 4.864965347266905e-32*state(11) - 5.779235214948339e-34*state(13)*state(9);
  jacobian(13, 13) = -5.779235214948339e-34*state(12)*state(9);
}
}  // namespace mkpp::generated::saprc99_mini::detail
