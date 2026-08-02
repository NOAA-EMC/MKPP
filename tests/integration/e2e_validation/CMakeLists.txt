add_subdirectory(${CMAKE_SOURCE_DIR}/src/mkpp_host ${CMAKE_BINARY_DIR}/mkpp_host)
cmake_minimum_required(VERSION 3.24)

# To get the python number of species dynamically
execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import yaml; print(len(yaml.safe_load(open('../../mechanisms/chapman.yaml'))['species']))"
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE CHAPMAN_SPEC
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import yaml; print(len(yaml.safe_load(open('../../mechanisms/small_strato.yaml'))['species']))"
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE SMALL_STRATO_SPEC
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

set(MECHS "chapman" "small_strato" "carbon")

foreach(MECH ${MECHS})
    if("${MECH}" STREQUAL "chapman")
        set(NUM_SPEC ${CHAPMAN_SPEC})
    elseif("${MECH}" STREQUAL "small_strato")
        set(NUM_SPEC ${SMALL_STRATO_SPEC})
    endif()

    add_executable(e2e_${MECH}_runner test_e2e_mechanisms.cpp)
    target_include_directories(e2e_${MECH}_runner PRIVATE ${CMAKE_SOURCE_DIR}/mkpp-generated)
    target_link_libraries(e2e_${MECH}_runner PRIVATE mkpp_host Kokkos::kokkos GTest::gtest_main GTest::gtest)
    target_compile_definitions(e2e_${MECH}_runner PRIVATE MECH_HEADER=${MECH}.hpp NUM_SPECIES_MACRO=${NUM_SPEC})
    
    add_test(NAME E2ESolver_${MECH} COMMAND e2e_${MECH}_runner)

    add_test(NAME E2ECompare_${MECH} COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/compare_baselines.py --baseline ${CMAKE_CURRENT_SOURCE_DIR}/data/kpp_baseline_${MECH}.csv --target e2e_output.csv --hpp ${CMAKE_SOURCE_DIR}/mkpp-generated/${MECH}.hpp)
    set_tests_properties(E2ECompare_${MECH} PROPERTIES DEPENDS E2ESolver_${MECH})
endforeach()
