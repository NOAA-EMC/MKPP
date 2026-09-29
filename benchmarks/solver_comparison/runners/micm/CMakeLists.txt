if(NOT TARGET micm)
  message(FATAL_ERROR "MICM comparison runner requires the pinned micm target")
endif()

add_executable(solver_benchmark_micm main.cpp)
target_link_libraries(solver_benchmark_micm PRIVATE micm)
target_compile_features(solver_benchmark_micm PRIVATE cxx_std_20)
target_compile_definitions(
  solver_benchmark_micm PRIVATE MICM_BENCHMARK_VERSION="3.13.0"
                                MICM_BENCHMARK_REVISION="97ac9e5d8aadd345c242722ee8274d71dfe0f73e")

add_subdirectory(ts1)

if(BUILD_TESTING)
  add_test(NAME SolverComparison_MICM_ChapmanSmoke COMMAND solver_benchmark_micm)
  set_tests_properties(SolverComparison_MICM_ChapmanSmoke
                       PROPERTIES LABELS "solver-comparison;non-publishable")
endif()
