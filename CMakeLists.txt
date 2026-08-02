cmake_minimum_required(VERSION 3.24)
project(MKPP_Root CXX)

find_package(Kokkos REQUIRED)

include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        release-1.12.1
)
FetchContent_MakeAvailable(googletest)

if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()
