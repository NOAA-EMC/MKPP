find_package(Python3 QUIET COMPONENTS Interpreter)
include("${CMAKE_SOURCE_DIR}/src/mkpp_host/cmake/MKPPCompiledMechanism.cmake")

set(TS1_SOURCE_ROOT "${CMAKE_SOURCE_DIR}/benchmarks/solver_comparison/sources/ts1/musica-config")
set(TS1_CONFIG "${TS1_SOURCE_ROOT}/ts1.json")
set(TS1_ENVIRONMENT "${TS1_SOURCE_ROOT}/environment.yaml")
# MKPP's path policy intentionally permits generated artifacts only beneath the source workspace. Do
# not use CMAKE_CURRENT_BINARY_DIR here: controlled Docker builds commonly place it in /tmp outside
# that policy boundary.
set(MKPP_TS1_GENERATED_DIR "${CMAKE_SOURCE_DIR}/build/solver_comparison/generated_ts1")
set(MKPP_TS1_GENERATED_HEADER "${MKPP_TS1_GENERATED_DIR}/ts1.hpp")

foreach(asset IN ITEMS "${TS1_CONFIG}" "${TS1_ENVIRONMENT}")
  if(NOT EXISTS "${asset}")
    message(FATAL_ERROR "FATAL ERROR: pinned OpenAtmos TS1 input is missing: ${asset}")
  endif()
endforeach()

file(SHA256 "${TS1_CONFIG}" TS1_CONFIG_SHA256)
file(SHA256 "${TS1_ENVIRONMENT}" TS1_ENVIRONMENT_SHA256)
if(NOT TS1_CONFIG_SHA256 STREQUAL
   "f5c31297ba5e38c17e49607ed2b7bcbf194b412fe49f819c23c66548e6f532de")
  message(FATAL_ERROR "FATAL ERROR: pinned OpenAtmos TS1 configuration hash mismatch")
endif()
if(NOT TS1_ENVIRONMENT_SHA256 STREQUAL
   "2c5206c7ded909f5c219b47e2eda5b03819c3993e9aaace8556862b5ff0a6995")
  message(FATAL_ERROR "FATAL ERROR: pinned OpenAtmos TS1 environment hash mismatch")
endif()

# Both native solvers consume this exact OpenAtmos configuration.  The output header is a build
# artifact, not a second mechanism definition; --no-cache makes source/environment changes visible
# immediately to generated chemistry.
if(Python3_Interpreter_FOUND)
  # CMake must know the bounded source list when it creates the target.  Seed a missing artifact
  # here; normal incremental regeneration remains a build dependency below.  The generator is
  # deterministic, so this does not add a second mechanism representation.
  if(NOT EXISTS "${MKPP_TS1_GENERATED_HEADER}" OR NOT EXISTS
                                                  "${MKPP_TS1_GENERATED_DIR}/ts1/rates.cpp")
    execute_process(
      COMMAND "${CMAKE_COMMAND}" -E make_directory "${MKPP_TS1_GENERATED_DIR}"
      COMMAND
        "${CMAKE_COMMAND}" -E env "PYTHONPATH=${CMAKE_SOURCE_DIR}/src" "${Python3_EXECUTABLE}" -c
        "from mkpp.cli import main; main()" compile "${TS1_CONFIG}" --test-env "${TS1_ENVIRONMENT}"
        --out "${MKPP_TS1_GENERATED_DIR}" --emit-manifest --no-cache
      WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
      RESULT_VARIABLE MKPP_TS1_GENERATION_RESULT)
    if(NOT MKPP_TS1_GENERATION_RESULT EQUAL 0)
      message(FATAL_ERROR "FATAL ERROR: unable to generate OpenAtmos-derived MKPP TS1 kernels")
    endif()
  endif()
  file(
    GLOB
    MKPP_TS1_COMPILED_SOURCES
    CONFIGURE_DEPENDS
    "${MKPP_TS1_GENERATED_DIR}/ts1/rates.cpp"
    "${MKPP_TS1_GENERATED_DIR}/ts1/jacobian.cpp"
    "${MKPP_TS1_GENERATED_DIR}/ts1/factorize_*.cpp"
    "${MKPP_TS1_GENERATED_DIR}/ts1/solve.cpp"
    "${MKPP_TS1_GENERATED_DIR}/ts1/supernodal_factorize.cpp"
    "${MKPP_TS1_GENERATED_DIR}/ts1/supernodal_solve.cpp")
  if(NOT MKPP_TS1_COMPILED_SOURCES)
    message(FATAL_ERROR "FATAL ERROR: TS1 generation emitted no compiled kernel sources")
  endif()
  add_custom_command(
    OUTPUT "${MKPP_TS1_GENERATED_HEADER}" ${MKPP_TS1_COMPILED_SOURCES}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${MKPP_TS1_GENERATED_DIR}"
    COMMAND
      "${CMAKE_COMMAND}" -E env "PYTHONPATH=${CMAKE_SOURCE_DIR}/src" "${Python3_EXECUTABLE}" -c
      "from mkpp.cli import main; main()" compile "${TS1_CONFIG}" --test-env "${TS1_ENVIRONMENT}"
      --out "${MKPP_TS1_GENERATED_DIR}" --emit-manifest --no-cache
    DEPENDS "${TS1_CONFIG}" "${TS1_ENVIRONMENT}"
    COMMENT "Generating MKPP TS1 kernel from pinned OpenAtmos inputs"
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    VERBATIM)
  add_custom_target(mkpp_ts1_openatmos_binding DEPENDS "${MKPP_TS1_GENERATED_HEADER}")

  mkpp_add_compiled_mechanism(mkpp_ts1_compiled_kernels "${MKPP_TS1_GENERATED_DIR}" ts1)
  add_dependencies(mkpp_ts1_compiled_kernels mkpp_ts1_openatmos_binding)
  target_compile_features(mkpp_ts1_compiled_kernels PRIVATE cxx_std_23)
else()
  # cece-dev deliberately contains the native toolchain but no Python.  Its fallback is safe only
  # for the exact pinned source hashes checked above; source changes fail CMake before a stale
  # generated kernel can be used.
  set(MKPP_TS1_GENERATED_DIR "${CMAKE_SOURCE_DIR}/mkpp-generated")
  set(MKPP_TS1_GENERATED_HEADER "${MKPP_TS1_GENERATED_DIR}/ts1.hpp")
  if(NOT EXISTS "${MKPP_TS1_GENERATED_HEADER}")
    message(FATAL_ERROR "FATAL ERROR: no verified OpenAtmos-derived MKPP TS1 header is available")
  endif()
  add_custom_target(mkpp_ts1_openatmos_binding DEPENDS "${MKPP_TS1_GENERATED_HEADER}"
                                                       "${TS1_CONFIG}" "${TS1_ENVIRONMENT}")
  mkpp_add_compiled_mechanism(mkpp_ts1_compiled_kernels "${MKPP_TS1_GENERATED_DIR}" ts1)
endif()

# The runner selects Chapman as well as TS1 through the host dispatcher.  Each selected generated
# mechanism must therefore register its implementation assets through the same artifact-discovery
# path.
mkpp_add_compiled_mechanism(mkpp_chapman_compiled_kernels "${CMAKE_SOURCE_DIR}/mkpp-generated"
                            chapman)
target_compile_features(mkpp_chapman_compiled_kernels PRIVATE cxx_std_23)

add_executable(solver_benchmark_mkpp main.cpp)
add_dependencies(solver_benchmark_mkpp mkpp_ts1_openatmos_binding)

target_compile_features(solver_benchmark_mkpp PRIVATE cxx_std_23)
target_compile_definitions(solver_benchmark_mkpp PRIVATE MKPP_HOST_SELECTED_MECHANISMS
                                                         MKPP_HOST_MECH_CHAPMAN MKPP_HOST_MECH_TS1)
target_include_directories(solver_benchmark_mkpp PRIVATE "${MKPP_TS1_GENERATED_DIR}"
                                                         ${CMAKE_SOURCE_DIR}/mkpp-generated)
target_link_libraries(solver_benchmark_mkpp PRIVATE mkpp_host Kokkos::kokkos)
target_link_libraries(solver_benchmark_mkpp PRIVATE mkpp_ts1_compiled_kernels
                                                    mkpp_chapman_compiled_kernels)
