#pragma once
#include <Kokkos_Core.hpp>
#include "accessor.hpp"
namespace mkpp::generated::carbon::detail {
KOKKOS_INLINE_FUNCTION void compute_jacobian_chunk_0(
  StrideView<const double, 1> state, StrideView<double, 2> jacobian,
    const double* jvals, double temp, double rh) {
  (void)temp;
  (void)rh;
  jacobian(0, 0) = -1.0665177283814332e-13;
  jacobian(0, 7) = -6.3627720033519555e-15*state(0);
  jacobian(0, 8) = -1.0028900083479136e-13*state(0);
  jacobian(1, 1) = -7.3679649e-14;
  jacobian(1, 7) = -7.3679649e-14*state(1);
  jacobian(1, 9) = 4.2566446e-15;
  jacobian(1, 10) = 38199.012;
  jacobian(2, 9) = 4.2566446e-15;
  jacobian(3, 10) = 38199.012;
  jacobian(4, 0) = 6.3627720033519555e-15;
  jacobian(4, 7) = 6.3627720033519555e-15*state(0);
  jacobian(5, 0) = 1.0028900083479136e-13;
  jacobian(5, 8) = 1.0028900083479136e-13*state(0);
  jacobian(6, 1) = 7.3679649e-14;
  jacobian(6, 7) = 7.3679649e-14*state(1);
  jacobian(7, 0) = -6.3627720033519555e-15;
  jacobian(7, 1) = -7.3679649e-14;
  jacobian(7, 7) = -6.3627720033519555e-15*state(0) - 7.3679649e-14*state(1);
  jacobian(8, 0) = -1.0028900083479136e-13;
  jacobian(8, 8) = -1.0028900083479136e-13*state(0);
  jacobian(9, 9) = -4.2566446e-15;
  jacobian(10, 10) = -38199.012;
}
}  // namespace mkpp::generated::carbon::detail
