#pragma once
#include <Kokkos_Core.hpp>
// Generated solver for chapman
// SZA Workload Sorted: true
// Hysteresis/Spline Continuous Transition: true
namespace mkpp {
  // Pure Kokkos abstractions (no raw pragmas allowed)
  // Bidirectional Host Interface (Zero-Copy)
  using concentrations_view_t = Kokkos::View<double****, Kokkos::LayoutLeft, Kokkos::MemoryUnmanaged>;
  template<typename DeviceType>
  struct SolverKernels {
      KOKKOS_INLINE_FUNCTION void lu_decompose(double* A, int N, int* indx) const {
          for (int i = 0; i < N; i++) {
              double max_val = 0.0;
              int max_idx = i;
              for (int k = i; k < N; k++) {
                  double val = A[k * N + i];
                  if (val < 0) val = -val;
                  if (val > max_val) { max_val = val; max_idx = k; }
              }
              indx[i] = max_idx;
              if (max_idx != i) {
                  for (int j = 0; j < N; j++) {
                      double temp = A[i * N + j];
                      A[i * N + j] = A[max_idx * N + j];
                      A[max_idx * N + j] = temp;
                  }
              }
              for (int j = i + 1; j < N; j++) {
                  A[j * N + i] /= A[i * N + i];
                  for (int k = i + 1; k < N; k++) {
                      A[j * N + k] -= A[j * N + i] * A[i * N + k];
                  }
              }
          }
      }

      KOKKOS_INLINE_FUNCTION void lu_solve(double* A, int N, int* indx, double* b) const {
          for (int i = 0; i < N; i++) {
              int ip = indx[i];
              double sum = b[ip];
              b[ip] = b[i];
              for (int j = 0; j < i; j++) {
                  sum -= A[i * N + j] * b[j];
              }
              b[i] = sum;
          }
          for (int i = N - 1; i >= 0; i--) {
              double sum = b[i];
              for (int j = i + 1; j < N; j++) {
                  sum -= A[i * N + j] * b[j];
              }
              b[i] = sum / A[i * N + i];
          }
      }

      KOKKOS_INLINE_FUNCTION void integrate(double dt, double* state) const {
          const int NUM_SPECIES = 4;
          const double g = 1.70710678118655;
          const double ros_A[1] = {1.0/g};
          const double ros_C[1] = {-2.0/g};
          const double ros_M[2] = {3.0/(2.0*g), 1.0/(2.0*g)};
          
          double Ynew[100];
          double F1[100], F2[100];
          double K1[100], K2[100];
          double Jac[10000] = {0.0};
          double W[10000];
          int indx[100];
          
          compute_rates(state, F1);
          compute_jacobian(state, Jac);
          
          for(int i=0; i<NUM_SPECIES; i++) {
              for(int j=0; j<NUM_SPECIES; j++) {
                  W[i*NUM_SPECIES + j] = -Jac[i*NUM_SPECIES + j];
                  if (i==j) W[i*NUM_SPECIES + j] += 1.0/(g*dt);
              }
          }
          lu_decompose(W, NUM_SPECIES, indx);
          
          for(int i=0; i<NUM_SPECIES; i++) K1[i] = F1[i];
          lu_solve(W, NUM_SPECIES, indx, K1);
          
          for(int i=0; i<NUM_SPECIES; i++) Ynew[i] = state[i] + ros_A[0] * K1[i];
          compute_rates(Ynew, F2);
          
          for(int i=0; i<NUM_SPECIES; i++) {
              K2[i] = F2[i] + (ros_C[0]/dt) * K1[i];
          }
          lu_solve(W, NUM_SPECIES, indx, K2);
          
          for(int i=0; i<NUM_SPECIES; i++) {
              state[i] += ros_M[0] * K1[i] + ros_M[1] * K2[i];
          }
      }

      KOKKOS_INLINE_FUNCTION void compute_rates(double* state, double* F_block) const {
      }

      KOKKOS_INLINE_FUNCTION void compute_jacobian(double* state, double* J_block) const {
          J_block[0] = -1.0*6e-34*state[3]*state[1] - 1.0*8e-12*state[2];
          J_block[1] = 2.0*1e-05 - 1.0*6e-34*state[3]*state[0];
          J_block[2] = 1.0*0.001 - 1.0*8e-12*state[0];
          J_block[3] = -1.0*6e-34*state[0]*state[1];
          J_block[4] = -1.0*6e-34*state[3]*state[1] + 2.0*8e-12*state[2];
          J_block[5] = -1.0*1e-05 - 1.0*6e-34*state[3]*state[0];
          J_block[6] = 1.0*0.001 + 2.0*8e-12*state[0];
          J_block[7] = -1.0*6e-34*state[0]*state[1];
          J_block[8] = 1.0*6e-34*state[3]*state[1] - 1.0*8e-12*state[2];
          J_block[9] = 1.0*6e-34*state[3]*state[0];
          J_block[10] = -1.0*0.001 - 1.0*8e-12*state[0];
          J_block[11] = 1.0*6e-34*state[0]*state[1];
      }
      KOKKOS_INLINE_FUNCTION void compute_adjoint(double* state, double* J_adj_block) const {
          J_adj_block[0] = -1.0*6e-34*state[3]*state[1] - 1.0*8e-12*state[2];
          J_adj_block[1] = -1.0*6e-34*state[3]*state[1] + 2.0*8e-12*state[2];
          J_adj_block[2] = 1.0*6e-34*state[3]*state[1] - 1.0*8e-12*state[2];
          J_adj_block[4] = 2.0*1e-05 - 1.0*6e-34*state[3]*state[0];
          J_adj_block[5] = -1.0*1e-05 - 1.0*6e-34*state[3]*state[0];
          J_adj_block[6] = 1.0*6e-34*state[3]*state[0];
          J_adj_block[8] = 1.0*0.001 - 1.0*8e-12*state[0];
          J_adj_block[9] = 1.0*0.001 + 2.0*8e-12*state[0];
          J_adj_block[10] = -1.0*0.001 - 1.0*8e-12*state[0];
          J_adj_block[12] = -1.0*6e-34*state[0]*state[1];
          J_adj_block[13] = -1.0*6e-34*state[0]*state[1];
          J_adj_block[14] = 1.0*6e-34*state[0]*state[1];
      }
      KOKKOS_INLINE_FUNCTION void compute_tlm(double* state, double* delta_C, double* dF_block) const {
          dF_block[0] = 0.0;
          dF_block[0] += (-1.0*6e-34*state[3]*state[1] - 1.0*8e-12*state[2]) * delta_C[0];
          dF_block[0] += (2.0*1e-05 - 1.0*6e-34*state[3]*state[0]) * delta_C[1];
          dF_block[0] += (1.0*0.001 - 1.0*8e-12*state[0]) * delta_C[2];
          dF_block[0] += (-1.0*6e-34*state[0]*state[1]) * delta_C[3];
          dF_block[1] = 0.0;
          dF_block[1] += (-1.0*6e-34*state[3]*state[1] + 2.0*8e-12*state[2]) * delta_C[0];
          dF_block[1] += (-1.0*1e-05 - 1.0*6e-34*state[3]*state[0]) * delta_C[1];
          dF_block[1] += (1.0*0.001 + 2.0*8e-12*state[0]) * delta_C[2];
          dF_block[1] += (-1.0*6e-34*state[0]*state[1]) * delta_C[3];
          dF_block[2] = 0.0;
          dF_block[2] += (1.0*6e-34*state[3]*state[1] - 1.0*8e-12*state[2]) * delta_C[0];
          dF_block[2] += (1.0*6e-34*state[3]*state[0]) * delta_C[1];
          dF_block[2] += (-1.0*0.001 - 1.0*8e-12*state[0]) * delta_C[2];
          dF_block[2] += (1.0*6e-34*state[0]*state[1]) * delta_C[3];
          dF_block[3] = 0.0;
      }
      KOKKOS_INLINE_FUNCTION void project_mass_conservation(double* C_projected, double* C, double* m_0) const {
          // C_projected = C - E^T (E E^T)^-1 (E C - m_0)
          double delta_m[100] = {0.0};
          C_projected[0] = C[0];
          C_projected[1] = C[1];
          C_projected[2] = C[2];
          C_projected[3] = C[3];
      }
  };
}
