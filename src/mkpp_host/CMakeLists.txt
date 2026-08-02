cmake_minimum_required(VERSION 3.24)
project(mkpp_host CXX)

find_package(Kokkos REQUIRED)

add_library(mkpp_host INTERFACE)
target_include_directories(mkpp_host INTERFACE 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(mkpp_host INTERFACE Kokkos::kokkos)
