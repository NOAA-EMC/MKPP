# Feature-local validation targets.  The executable targets are added as the portable backend and
# reference/candidate comparison implementations land.
add_custom_target(supernodal_factorization_cpu_fixture
                  COMMENT "Supernodal factorization CPU reference fixture is configured")

add_executable(supernodal_multi_mechanism test_multi_mechanism.cpp)
target_include_directories(supernodal_multi_mechanism PRIVATE ${CMAKE_SOURCE_DIR}/mkpp-generated)
target_link_libraries(supernodal_multi_mechanism PRIVATE Kokkos::kokkos)
add_test(NAME supernodal_multi_mechanism COMMAND supernodal_multi_mechanism)

include("${CMAKE_SOURCE_DIR}/src/mkpp_host/cmake/MKPPCompiledMechanism.cmake")
mkpp_add_compiled_mechanism(supernodal_chapman_kernels "${CMAKE_SOURCE_DIR}/mkpp-generated" chapman)
add_executable(supernodal_factorization_parity test_factorization_parity.cpp)
target_include_directories(supernodal_factorization_parity
                           PRIVATE ${CMAKE_SOURCE_DIR}/mkpp-generated)
target_link_libraries(supernodal_factorization_parity PRIVATE Kokkos::kokkos
                                                              supernodal_chapman_kernels)
add_test(NAME supernodal_factorization_parity COMMAND supernodal_factorization_parity)

add_executable(supernodal_sensitivity_parity test_sensitivity_parity.cpp)
target_include_directories(supernodal_sensitivity_parity PRIVATE ${CMAKE_SOURCE_DIR}/mkpp-generated)
target_compile_definitions(supernodal_sensitivity_parity PRIVATE MKPP_ENABLE_ADJOINT)
target_link_libraries(supernodal_sensitivity_parity PRIVATE Kokkos::kokkos
                                                            supernodal_chapman_kernels)
add_test(NAME supernodal_sensitivity_parity COMMAND supernodal_sensitivity_parity)

add_custom_target(
  supernodal_factorization_gpu_readiness
  COMMAND
    ${CMAKE_COMMAND} -E echo
    "GPU execution validation deferred: configure a CUDA or HIP Kokkos execution space to promote this target"
  DEPENDS supernodal_multi_mechanism supernodal_factorization_parity supernodal_sensitivity_parity
  COMMENT "Checking accelerator build-readiness without claiming GPU execution")
