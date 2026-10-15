#pragma once
#include <Kokkos_Core.hpp>
#include "accessor.hpp"
namespace mkpp::generated::chapman::detail {
KOKKOS_INLINE_FUNCTION void compute_jacobian_chunk_0(
  StrideView<const double, 1> state, StrideView<double, 2> jacobian,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  jacobian(0, 0) = -6e-34*state(3)*state(1) - 8e-12*state(2);
  jacobian(0, 1) = -6e-34*state(3)*state(0) + 2.0*jvals[0];
  jacobian(0, 2) = -8e-12*state(0) + 1.0*jvals[1];
  jacobian(0, 3) = -6e-34*state(0)*state(1);
  jacobian(1, 0) = -6e-34*state(3)*state(1) + 1.6e-11*state(2);
  jacobian(1, 1) = -6e-34*state(3)*state(0) - 1.0*jvals[0];
  jacobian(1, 2) = 1.6e-11*state(0) + 1.0*jvals[1];
  jacobian(1, 3) = -6e-34*state(0)*state(1);
  jacobian(2, 0) = 6e-34*state(3)*state(1) - 8e-12*state(2);
  jacobian(2, 1) = 6e-34*state(3)*state(0);
  jacobian(2, 2) = -8e-12*state(0) - 1.0*jvals[1];
  jacobian(2, 3) = 6e-34*state(0)*state(1);
}
}  // namespace mkpp::generated::chapman::detail
