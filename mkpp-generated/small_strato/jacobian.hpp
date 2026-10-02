#pragma once
#include <Kokkos_Core.hpp>
namespace mkpp::generated::small_strato::detail {
KOKKOS_INLINE_FUNCTION void compute_jacobian_chunk_0(
    const double* state, double* jacobian,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  jacobian[0 * 7 + 0] = -1.069e-11*state[4] - 8.018e-17*state[6] - 1.576e-15*state[2];
  jacobian[0 * 7 + 1] = 7.11e-11*state[5];
  jacobian[0 * 7 + 2] = -1.576e-15*state[0] + 1.0*jvals[1];
  jacobian[0 * 7 + 4] = -1.069e-11*state[0] + 1.0*jvals[3];
  jacobian[0 * 7 + 5] = 7.11e-11*state[1];
  jacobian[0 * 7 + 6] = -8.018e-17*state[0] + 2.0*jvals[0];
  jacobian[1 * 7 + 1] = -7.11e-11*state[5] - 1.2e-10*state[2];
  jacobian[1 * 7 + 2] = -1.2e-10*state[1] + 1.0*jvals[2];
  jacobian[1 * 7 + 5] = -7.11e-11*state[1];
  jacobian[2 * 7 + 0] = 8.018e-17*state[6] - 1.576e-15*state[2];
  jacobian[2 * 7 + 1] = -1.2e-10*state[2];
  jacobian[2 * 7 + 2] = -6.062e-15*state[3] - 1.576e-15*state[0] - 1.2e-10*state[1] - 1.0*jvals[1] - 1.0*jvals[2];
  jacobian[2 * 7 + 3] = -6.062e-15*state[2];
  jacobian[2 * 7 + 6] = 8.018e-17*state[0];
  jacobian[3 * 7 + 0] = 1.069e-11*state[4];
  jacobian[3 * 7 + 2] = -6.062e-15*state[3];
  jacobian[3 * 7 + 3] = -6.062e-15*state[2];
  jacobian[3 * 7 + 4] = 1.069e-11*state[0] + 1.0*jvals[3];
  jacobian[4 * 7 + 0] = -1.069e-11*state[4];
  jacobian[4 * 7 + 2] = 6.062e-15*state[3];
  jacobian[4 * 7 + 3] = 6.062e-15*state[2];
  jacobian[4 * 7 + 4] = -1.069e-11*state[0] - 1.0*jvals[3];
  jacobian[6 * 7 + 0] = 1.069e-11*state[4] - 8.018e-17*state[6] + 3.152e-15*state[2];
  jacobian[6 * 7 + 1] = 2.4e-10*state[2];
  jacobian[6 * 7 + 2] = 6.062e-15*state[3] + 3.152e-15*state[0] + 2.4e-10*state[1] + 1.0*jvals[1] + 1.0*jvals[2];
  jacobian[6 * 7 + 3] = 6.062e-15*state[2];
  jacobian[6 * 7 + 4] = 1.069e-11*state[0];
  jacobian[6 * 7 + 6] = -8.018e-17*state[0] - 1.0*jvals[0];
}
}  // namespace mkpp::generated::small_strato::detail
