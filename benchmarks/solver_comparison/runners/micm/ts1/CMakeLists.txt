find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(TS1_SOURCE_ROOT "${CMAKE_SOURCE_DIR}/benchmarks/solver_comparison/sources/ts1")
set(TS1_CONFIG_DIR "${TS1_SOURCE_ROOT}/musica-config")
set(TS1_IMPORTER "${TS1_SOURCE_ROOT}/micm-importer/import_ts1.py")
set(TS1_CONFIG "${TS1_CONFIG_DIR}/ts1.json")
set(TS1_INITIAL_CONDITIONS "${TS1_CONFIG_DIR}/initial_conditions.csv")
set(TS1_ENVIRONMENT "${TS1_CONFIG_DIR}/environment.yaml")
set(TS1_SCENARIO
    "${CMAKE_SOURCE_DIR}/benchmarks/solver_comparison/scenarios/ts1-measurement-v1.yaml")
set(TS1_GENERATED_HEADER "${CMAKE_CURRENT_BINARY_DIR}/generated_micm_ts1.hpp")

foreach(asset IN ITEMS "${TS1_IMPORTER}" "${TS1_CONFIG}" "${TS1_INITIAL_CONDITIONS}"
                       "${TS1_ENVIRONMENT}" "${TS1_SCENARIO}")
  if(NOT EXISTS "${asset}")
    message(FATAL_ERROR "FATAL ERROR: pinned MICM TS1 input is missing: ${asset}")
  endif()
endforeach()

file(SHA256 "${TS1_IMPORTER}" TS1_IMPORTER_SHA256)
file(SHA256 "${TS1_CONFIG}" TS1_CONFIG_SHA256)
file(SHA256 "${TS1_INITIAL_CONDITIONS}" TS1_INITIAL_CONDITIONS_SHA256)
file(SHA256 "${TS1_ENVIRONMENT}" TS1_ENVIRONMENT_SHA256)
if(NOT TS1_IMPORTER_SHA256 STREQUAL
   "603a8d449275de206e30eac77394c80af2c0054e151a802ff658a53c3ae69241")
  message(FATAL_ERROR "FATAL ERROR: pinned MICM TS1 importer hash mismatch")
endif()
if(NOT TS1_ENVIRONMENT_SHA256 STREQUAL
   "2c5206c7ded909f5c219b47e2eda5b03819c3993e9aaace8556862b5ff0a6995")
  message(FATAL_ERROR "FATAL ERROR: pinned TS1 environment hash mismatch")
endif()
if(NOT TS1_CONFIG_SHA256 STREQUAL
   "f5c31297ba5e38c17e49607ed2b7bcbf194b412fe49f819c23c66548e6f532de")
  message(FATAL_ERROR "FATAL ERROR: pinned MUSICA TS1 configuration hash mismatch")
endif()
if(NOT TS1_INITIAL_CONDITIONS_SHA256 STREQUAL
   "58db29256362fcd7fd60d47fe3d463c566dfbe14c000757202393fa7a28a9253")
  message(FATAL_ERROR "FATAL ERROR: pinned MUSICA TS1 initial-condition hash mismatch")
endif()

add_custom_command(
  OUTPUT "${TS1_GENERATED_HEADER}"
  COMMAND "${Python3_EXECUTABLE}" "${TS1_IMPORTER}" --source "${TS1_CONFIG_DIR}" --scenario
          "${TS1_SCENARIO}" --output "${TS1_GENERATED_HEADER}"
  DEPENDS "${TS1_IMPORTER}" "${TS1_CONFIG}" "${TS1_INITIAL_CONDITIONS}" "${TS1_ENVIRONMENT}"
          "${TS1_SCENARIO}"
  COMMENT "Generating audited MICM TS1 binding from pinned MUSICA inputs"
  VERBATIM)

add_executable(solver_benchmark_micm_ts1 main.cpp "${TS1_GENERATED_HEADER}")
target_include_directories(solver_benchmark_micm_ts1 PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(solver_benchmark_micm_ts1 PRIVATE micm)
target_compile_features(solver_benchmark_micm_ts1 PRIVATE cxx_std_20)
target_compile_definitions(
  solver_benchmark_micm_ts1
  PRIVATE MICM_BENCHMARK_VERSION="3.13.0"
          MICM_BENCHMARK_REVISION="97ac9e5d8aadd345c242722ee8274d71dfe0f73e")

if(BUILD_TESTING)
  add_test(NAME SolverComparison_MICM_TS1Smoke COMMAND solver_benchmark_micm_ts1)
  set_tests_properties(SolverComparison_MICM_TS1Smoke
                       PROPERTIES LABELS "solver-comparison;non-publishable")
endif()
