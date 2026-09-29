cmake_minimum_required(VERSION 3.24)

add_executable(test_batch_abi test_batch_abi.cpp)
target_link_libraries(test_batch_abi PRIVATE mkpp_host Kokkos::kokkos GTest::gtest)
add_test(NAME test_batch_abi COMMAND test_batch_abi)
