#pragma once
#include <Kokkos_Core.hpp>
namespace mkpp::generated::small_strato::detail {
KOKKOS_INLINE_FUNCTION void solve_plan(const double* lu, const double* rhs, double* solution) {
  constexpr int N = 7;
  double work[N];
  for (int row = 0; row < N; ++row) {
    work[row] = rhs[row];
    for (int column = 0; column < row; ++column) work[row] -= lu[row * N + column] * work[column];
  }
  for (int row = N - 1; row >= 0; --row) {
    solution[row] = work[row];
    for (int column = row + 1; column < N; ++column) solution[row] -= lu[row * N + column] * solution[column];
    solution[row] /= lu[row * N + row];
  }
}
}  // namespace mkpp::generated::small_strato::detail
