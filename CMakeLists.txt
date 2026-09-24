cmake_minimum_required(VERSION 3.24)
project(MKPP_Root CXX)

# When MKPP is consumed via add_subdirectory from a parent build (e.g. CATChem),
# the parent has already made Kokkos available: either as imported targets from
# find_package or as in-tree targets from FetchContent. Re-running
# find_package(Kokkos) in that situation is not a no-op -- it searches the
# config package on disk, which may resolve to a DIFFERENT Kokkos installation
# than the parent is building against, and re-including its exported targets
# collides with the parent's existing Kokkos:: targets. Adopt the parent's
# Kokkos when its targets already exist; find it ourselves only for a
# standalone MKPP build.
if(NOT TARGET Kokkos::kokkos)
  find_package(Kokkos REQUIRED)
endif()

option(MKPP_ENABLE_KOKKOS_KERNELS
       "Enable KokkosKernels integration for batched computations" OFF)

if(MKPP_ENABLE_KOKKOS_KERNELS)
  find_package(KokkosKernels 5.0 QUIET)
  if(NOT KokkosKernels_FOUND)
    find_package(KokkosKernels QUIET)
  endif()
  if(NOT KokkosKernels_FOUND)
    include(FetchContent)
    FetchContent_Declare(
      kokkos-kernels
      GIT_REPOSITORY https://github.com/kokkos/kokkos-kernels.git
      GIT_TAG 5.0.0)
    FetchContent_MakeAvailable(kokkos-kernels)
  endif()
  add_compile_definitions(MKPP_HAS_KOKKOS_KERNELS)
endif()

add_subdirectory(src/mkpp_host)

# ---------------------------------------------------------------------------
# Install targets (EE2 compliance: all, debug, install, clean)
# ---------------------------------------------------------------------------
include(GNUInstallDirs)

install(
  DIRECTORY mkpp-generated/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/mkpp
  FILES_MATCHING
  PATTERN "*.hpp"
  PATTERN "*.h"
  PATTERN "*.f90")

# ---------------------------------------------------------------------------
# Testing (guarded behind BUILD_TESTING)
# ---------------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.14.0)

option(MKPP_ENABLE_MICM_COMPARE
       "Fetch NCAR/micm and build direct C++ side-by-side comparison benchmark"
       OFF)

option(MKPP_ENABLE_ADJOINT
       "Enable adjoint and tangent-linear APIs in generated MKPP headers" OFF)

option(MKPP_ENABLE_SOLVER_COMPARISON
       "Build governed MICM, KPP, and MKPP comparison runners" OFF)

if(MKPP_ENABLE_MICM_COMPARE OR MKPP_ENABLE_SOLVER_COMPARISON)
  set(CMAKE_CXX_STANDARD
      20
      CACHE STRING "C++ standard")
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  include(FetchContent)
  FetchContent_Declare(
    micm
    GIT_REPOSITORY https://github.com/NCAR/micm.git
    # Audited comparison-subject revision. Never use a moving branch here.
    GIT_TAG 97ac9e5d8aadd345c242722ee8274d71dfe0f73e)
  FetchContent_MakeAvailable(micm)
endif()

if(MKPP_ENABLE_SOLVER_COMPARISON)
  enable_language(Fortran OPTIONAL)
  add_subdirectory(benchmarks/solver_comparison/runners)
endif()

if(BUILD_TESTING)
  FetchContent_MakeAvailable(googletest)
  enable_testing()
  add_subdirectory(tests)
endif()
