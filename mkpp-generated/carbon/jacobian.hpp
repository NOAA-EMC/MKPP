#pragma once
#include <Kokkos_Core.hpp>
namespace mkpp::generated::carbon::detail {
KOKKOS_INLINE_FUNCTION void compute_jacobian_chunk_0(
    const double* state, double* jacobian,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  jacobian[0 * 11 + 0] = -1.0665177283814332e-13;
  jacobian[0 * 11 + 7] = -6.3627720033519555e-15*state[0];
  jacobian[0 * 11 + 8] = -1.0028900083479136e-13*state[0];
  jacobian[1 * 11 + 1] = -7.3679649e-14;
  jacobian[1 * 11 + 7] = -7.3679649e-14*state[1];
  jacobian[1 * 11 + 9] = 4.2566446e-15;
  jacobian[1 * 11 + 10] = 38199.012;
  jacobian[2 * 11 + 9] = 4.2566446e-15;
  jacobian[3 * 11 + 10] = 38199.012;
  jacobian[4 * 11 + 0] = 6.3627720033519555e-15;
  jacobian[4 * 11 + 7] = 6.3627720033519555e-15*state[0];
  jacobian[5 * 11 + 0] = 1.0028900083479136e-13;
  jacobian[5 * 11 + 8] = 1.0028900083479136e-13*state[0];
  jacobian[6 * 11 + 1] = 7.3679649e-14;
  jacobian[6 * 11 + 7] = 7.3679649e-14*state[1];
  jacobian[7 * 11 + 0] = -6.3627720033519555e-15;
  jacobian[7 * 11 + 1] = -7.3679649e-14;
  jacobian[7 * 11 + 7] = -6.3627720033519555e-15*state[0] - 7.3679649e-14*state[1];
  jacobian[8 * 11 + 0] = -1.0028900083479136e-13;
  jacobian[8 * 11 + 8] = -1.0028900083479136e-13*state[0];
  jacobian[9 * 11 + 9] = -4.2566446e-15;
  jacobian[10 * 11 + 10] = -38199.012;
}
}  // namespace mkpp::generated::carbon::detail
