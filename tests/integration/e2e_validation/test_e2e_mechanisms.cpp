#include <gtest/gtest.h>
#include <Kokkos_Core.hpp>
#include <fstream>
#include <vector>
#include <string>

#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)
#include TOSTRING(MECH_HEADER)

using ExecSpace = Kokkos::DefaultExecutionSpace;

#include "mkpp_host/dispatcher.hpp"

TEST(E2ESolverValidation, MechanismIntegration) {
    int cells = 1;
    // We get n_spec dynamically from the Kokkos View initialization size
    // Wait, we need to know n_spec BEFORE creating host_data.
    // Fortunately mkpp_to_kpp mappings exist in compare_baselines.py, but for the C++ harness
    // we can pass it via CMake definition `-DNUM_SPECIES_MACRO=` or we can just make it large enough.
    // However, the Kokkos array extent must match. 
    int n_spec = 0;

    

    if(n_spec == 0) n_spec = 100; // fallback, but we will pass it from CMake
    
    std::vector<double> host_data(cells * n_spec * 1 * 1, 0.0);
    for (int i=0; i<cells; i++) {
        for (int k=0; k<n_spec; k++) {
            host_data[i * n_spec + k] = 100.0;
        }
    }
    
    mkpp::concentrations_view_t state(host_data.data(), cells, n_spec, 1, 1);
    
    mkpp::host::execute_mechanism<mkpp::SolverKernels<ExecSpace>>(TOSTRING(MECH_HEADER), state, 3600.0);
    Kokkos::fence();
    
    std::ofstream out("e2e_output.csv");
    out << "time_step,species_name,concentration\n";
    for(int k=0; k<n_spec; k++) {
        out << "1," << k << "," << host_data[k] << "\n";
    }
    out.close();
}

int main(int argc, char** argv) {
    Kokkos::initialize(argc, argv);
    ::testing::InitGoogleTest(&argc, argv);
    int result = RUN_ALL_TESTS();
    Kokkos::finalize();
    return result;
}
