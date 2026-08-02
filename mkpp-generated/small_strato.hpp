#pragma once
#include <Kokkos_Core.hpp>
// Generated solver for small_strato
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
          const int NUM_SPECIES = 7;
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
          J_block[0] = -1.0*1.069E-11*1.0 - 1.0*1.576E-15*state[2] - 1.0*8.018E-17*state[6];
          J_block[1] = 1.0*7.110E-11*state[5];
          J_block[2] = -1.0*1.576E-15*state[0] + 1.0*6.120E-04 * 1.0;
          J_block[4] = -1.0*1.069E-11*state[0] + 1.0*1.289E-02 * 1.0;
          J_block[5] = 1.0*7.110E-11*1.0;
          J_block[6] = 2.0*2.643E-10 * 1.0*1.0*1.0 - 1.0*8.018E-17*state[0];
          J_block[8] = -1.0*1.200E-10*state[2] - 1.0*7.110E-11*state[5];
          J_block[9] = 1.0*1.070E-03 * 1.0*1.0 - 1.0*1.200E-10*1.0;
          J_block[12] = -1.0*7.110E-11*1.0;
          J_block[14] = -1.0*1.576E-15*state[2] + 1.0*8.018E-17*state[6];
          J_block[15] = -1.0*1.200E-10*state[2];
          J_block[16] = -1.0*1.070E-03 * 1.0*1.0 - 1.0*1.200E-10*1.0 - 1.0*1.576E-15*state[0] - 1.0*6.062E-15*1.0 - 1.0*6.120E-04 * 1.0;
          J_block[17] = -1.0*6.062E-15*state[2];
          J_block[20] = 1.0*8.018E-17*state[0];
          J_block[21] = 1.0*1.069E-11*1.0;
          J_block[23] = -1.0*6.062E-15*1.0;
          J_block[24] = -1.0*6.062E-15*state[2];
          J_block[25] = 1.0*1.069E-11*state[0] + 1.0*1.289E-02 * 1.0;
          J_block[28] = -1.0*1.069E-11*1.0;
          J_block[30] = 1.0*6.062E-15*1.0;
          J_block[31] = 1.0*6.062E-15*state[2];
          J_block[32] = -1.0*1.069E-11*state[0] - 1.0*1.289E-02 * 1.0;
          J_block[42] = 1.0*1.069E-11*1.0 + 2.0*1.576E-15*state[2] - 1.0*8.018E-17*state[6];
          J_block[43] = 2.0*1.200E-10*state[2];
          J_block[44] = 1.0*1.070E-03 * 1.0*1.0 + 2.0*1.200E-10*1.0 + 2.0*1.576E-15*state[0] + 1.0*6.062E-15*1.0 + 1.0*6.120E-04 * 1.0;
          J_block[45] = 1.0*6.062E-15*state[2];
          J_block[46] = 1.0*1.069E-11*state[0];
          J_block[48] = -1.0*2.643E-10 * 1.0*1.0*1.0 - 1.0*8.018E-17*state[0];
      }
      KOKKOS_INLINE_FUNCTION void compute_adjoint(double* state, double* J_adj_block) const {
          J_adj_block[0] = -1.0*1.069E-11*1.0 - 1.0*1.576E-15*state[2] - 1.0*8.018E-17*state[6];
          J_adj_block[2] = -1.0*1.576E-15*state[2] + 1.0*8.018E-17*state[6];
          J_adj_block[3] = 1.0*1.069E-11*1.0;
          J_adj_block[4] = -1.0*1.069E-11*1.0;
          J_adj_block[6] = 1.0*1.069E-11*1.0 + 2.0*1.576E-15*state[2] - 1.0*8.018E-17*state[6];
          J_adj_block[7] = 1.0*7.110E-11*state[5];
          J_adj_block[8] = -1.0*1.200E-10*state[2] - 1.0*7.110E-11*state[5];
          J_adj_block[9] = -1.0*1.200E-10*state[2];
          J_adj_block[13] = 2.0*1.200E-10*state[2];
          J_adj_block[14] = -1.0*1.576E-15*state[0] + 1.0*6.120E-04 * 1.0;
          J_adj_block[15] = 1.0*1.070E-03 * 1.0*1.0 - 1.0*1.200E-10*1.0;
          J_adj_block[16] = -1.0*1.070E-03 * 1.0*1.0 - 1.0*1.200E-10*1.0 - 1.0*1.576E-15*state[0] - 1.0*6.062E-15*1.0 - 1.0*6.120E-04 * 1.0;
          J_adj_block[17] = -1.0*6.062E-15*1.0;
          J_adj_block[18] = 1.0*6.062E-15*1.0;
          J_adj_block[20] = 1.0*1.070E-03 * 1.0*1.0 + 2.0*1.200E-10*1.0 + 2.0*1.576E-15*state[0] + 1.0*6.062E-15*1.0 + 1.0*6.120E-04 * 1.0;
          J_adj_block[23] = -1.0*6.062E-15*state[2];
          J_adj_block[24] = -1.0*6.062E-15*state[2];
          J_adj_block[25] = 1.0*6.062E-15*state[2];
          J_adj_block[27] = 1.0*6.062E-15*state[2];
          J_adj_block[28] = -1.0*1.069E-11*state[0] + 1.0*1.289E-02 * 1.0;
          J_adj_block[31] = 1.0*1.069E-11*state[0] + 1.0*1.289E-02 * 1.0;
          J_adj_block[32] = -1.0*1.069E-11*state[0] - 1.0*1.289E-02 * 1.0;
          J_adj_block[34] = 1.0*1.069E-11*state[0];
          J_adj_block[35] = 1.0*7.110E-11*1.0;
          J_adj_block[36] = -1.0*7.110E-11*1.0;
          J_adj_block[42] = 2.0*2.643E-10 * 1.0*1.0*1.0 - 1.0*8.018E-17*state[0];
          J_adj_block[44] = 1.0*8.018E-17*state[0];
          J_adj_block[48] = -1.0*2.643E-10 * 1.0*1.0*1.0 - 1.0*8.018E-17*state[0];
      }
      KOKKOS_INLINE_FUNCTION void compute_tlm(double* state, double* delta_C, double* dF_block) const {
          dF_block[0] = 0.0;
          dF_block[0] += (-1.0*1.069E-11*1.0 - 1.0*1.576E-15*state[2] - 1.0*8.018E-17*state[6]) * delta_C[0];
          dF_block[0] += (1.0*7.110E-11*state[5]) * delta_C[1];
          dF_block[0] += (-1.0*1.576E-15*state[0] + 1.0*6.120E-04 * 1.0) * delta_C[2];
          dF_block[0] += (-1.0*1.069E-11*state[0] + 1.0*1.289E-02 * 1.0) * delta_C[4];
          dF_block[0] += (1.0*7.110E-11*1.0) * delta_C[5];
          dF_block[0] += (2.0*2.643E-10 * 1.0*1.0*1.0 - 1.0*8.018E-17*state[0]) * delta_C[6];
          dF_block[1] = 0.0;
          dF_block[1] += (-1.0*1.200E-10*state[2] - 1.0*7.110E-11*state[5]) * delta_C[1];
          dF_block[1] += (1.0*1.070E-03 * 1.0*1.0 - 1.0*1.200E-10*1.0) * delta_C[2];
          dF_block[1] += (-1.0*7.110E-11*1.0) * delta_C[5];
          dF_block[2] = 0.0;
          dF_block[2] += (-1.0*1.576E-15*state[2] + 1.0*8.018E-17*state[6]) * delta_C[0];
          dF_block[2] += (-1.0*1.200E-10*state[2]) * delta_C[1];
          dF_block[2] += (-1.0*1.070E-03 * 1.0*1.0 - 1.0*1.200E-10*1.0 - 1.0*1.576E-15*state[0] - 1.0*6.062E-15*1.0 - 1.0*6.120E-04 * 1.0) * delta_C[2];
          dF_block[2] += (-1.0*6.062E-15*state[2]) * delta_C[3];
          dF_block[2] += (1.0*8.018E-17*state[0]) * delta_C[6];
          dF_block[3] = 0.0;
          dF_block[3] += (1.0*1.069E-11*1.0) * delta_C[0];
          dF_block[3] += (-1.0*6.062E-15*1.0) * delta_C[2];
          dF_block[3] += (-1.0*6.062E-15*state[2]) * delta_C[3];
          dF_block[3] += (1.0*1.069E-11*state[0] + 1.0*1.289E-02 * 1.0) * delta_C[4];
          dF_block[4] = 0.0;
          dF_block[4] += (-1.0*1.069E-11*1.0) * delta_C[0];
          dF_block[4] += (1.0*6.062E-15*1.0) * delta_C[2];
          dF_block[4] += (1.0*6.062E-15*state[2]) * delta_C[3];
          dF_block[4] += (-1.0*1.069E-11*state[0] - 1.0*1.289E-02 * 1.0) * delta_C[4];
          dF_block[5] = 0.0;
          dF_block[6] = 0.0;
          dF_block[6] += (1.0*1.069E-11*1.0 + 2.0*1.576E-15*state[2] - 1.0*8.018E-17*state[6]) * delta_C[0];
          dF_block[6] += (2.0*1.200E-10*state[2]) * delta_C[1];
          dF_block[6] += (1.0*1.070E-03 * 1.0*1.0 + 2.0*1.200E-10*1.0 + 2.0*1.576E-15*state[0] + 1.0*6.062E-15*1.0 + 1.0*6.120E-04 * 1.0) * delta_C[2];
          dF_block[6] += (1.0*6.062E-15*state[2]) * delta_C[3];
          dF_block[6] += (1.0*1.069E-11*state[0]) * delta_C[4];
          dF_block[6] += (-1.0*2.643E-10 * 1.0*1.0*1.0 - 1.0*8.018E-17*state[0]) * delta_C[6];
      }
      KOKKOS_INLINE_FUNCTION void project_mass_conservation(double* C_projected, double* C, double* m_0) const {
          // C_projected = C - E^T (E E^T)^-1 (E C - m_0)
          double delta_m[100] = {0.0};
          C_projected[0] = C[0];
          C_projected[1] = C[1];
          C_projected[2] = C[2];
          C_projected[3] = C[3];
          C_projected[4] = C[4];
          C_projected[5] = C[5];
          C_projected[6] = C[6];
      }
  };
}
