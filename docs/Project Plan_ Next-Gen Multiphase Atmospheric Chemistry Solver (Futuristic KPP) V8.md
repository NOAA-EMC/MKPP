# **Master Architectural Specification & Project Charter: Multiphase KPP (MKPP) Engine**

**Target Framework Integration:** ufs-community/catchem (Native C++ Core)
**Document Type:** Master System Architecture Specification & Project Implementation Charter
**Version:** 8.0.0-FINAL
**Date:** July 2026

## ---

**1\. Project Charter & Executive Summary**

### **1.1 Context and Problem Statement**

Legacy atmospheric chemistry Ordinary Differential Equation (ODE) solvers (such as traditional Fortran-based KPP) introduce prohibitive performance bottlenecks on modern heterogeneous Exascale supercomputing architectures. These limitations stem from CPU-bound legacy code paths, rigid operator splitting, highly branched conditional logic in thermodynamics (causing GPU warp divergence), and bandwidth-bound linear algebra that exhausts GPU registers on massive mechanisms.

### **1.2 The MKPP Solution**

The MultiphaseKinetic PreProcessor (MKPP) fundamentally re-architects chemical ODE solving by shifting computational overhead from runtime abstractions to an Ahead-Of-Time (AOT) Python compilation frontend. It emits highly optimized, block-sparse Kokkos C++ headers that leverage KokkosBatched for dense micro-matrix math. Furthermore, the Python frontend automatically generates Adjoint and Tangent Linear Models (TLM) for seamless integration with Data Assimilation frameworks (e.g., JEDI).
MKPP connects to the host model via **Exaero**, a bidirectional physical description interface that standardizes aerosol diagnostics and cloud coupling so external physics modules can interpret the chemical state without breaking encapsulation.

### **1.3 Scientific Background: The "Whole Atmosphere" Multiphase Bottleneck**

Atmospheric chemistry is the most computationally demanding component of modern Earth System Models. Legacy architectures struggle due to three fundamental bottlenecks across the vertical column:
**A. The Chemical Complexity Explosion:** Modern mechanisms track an exploding number of chemical species, from Volatile Chemical Products (VCPs) in the troposphere to catalytic halogen cycles in the stratosphere. Solving fast radicals alongside slow-decaying trace gases requires highly complex implicit matrix math that chokes legacy CPU solvers.
**B. The Operator Splitting Fallacy:** In reality, gases oxidize and condense simultaneously (tropospheric SOA) or adsorb onto ice (stratospheric halogen activation). Legacy models use "operator splitting"—pausing the chemistry solver to run aerosol modules—which introduces severe time-truncation errors and data-transfer bottlenecks.
**C. The Thermodynamic Branching Crisis:** Aerosols undergo extreme phase changes, from salt deliquescence to Polar Stratospheric Cloud (PSC) nucleation at 195 K. Legacy thermodynamic modules rely on massive if/else decision trees. On GPUs, this causes thread warp divergence, forcing serialized calculations and destroying parallel speed.
**D. The MKPP Paradigm Shift:** MKPP utilizes a **Unified Jacobian** to treat phase changes as kinetic differential equations, eliminating operator splitting. It replaces rigid if/else thresholds with continuous, analytically differentiable curves (sigmoids), handles sunrise photolysis dynamically, and uses **Kokkos Hierarchical Parallelism** to keep GPU threads perfectly synchronized.

### **1.4 References useful for this work are in this shared folder.**

[References\_chem](https://drive.google.com/drive/folders/1jIqpw6tYIYxptYfh2wPuyVW1gw-CY37o?usp=drive_link)

## ---

**2\. Core Architectural Pillars**

\+---------------------------------------------------------------------------------------------------+
|                                 BUILD-TIME FRONTEND (Python DSL)                                  |
|  \[ YAML \] \---\> \[ SymPy Calculus \] \---\> \[ Representation Mappers \] \---\> \[ C++ Code Generator \]     |
|                   (Auto-generates Adjoint/TLM Kernels for Data Assimilation)                      |
\+---------------------------------------------------------------------------------------------------+
                                                                    |
                                                                    v (Emits KokkosBatched Headers)
\+---------------------------------------------------------------------------------------------------+
|                                  RUNTIME EXECUTION (CATChem C++)                                  |
|                                                                                                   |
|   CATChem C++ Driver \---\> Allocates State Memory via Kokkos::DefaultExecutionSpace::array\_layout  |
|                                           |                                                       |
|                      \[ SZA Workload Sorter (The "Terminator" Balancer) \]                          |
|                                           |                                                       |
|                     \+---------------------+---------------------+                                 |
|                     |     \[ Explicit Nucleation Source Kernel \] |                                 |
|                     v                                           v                                 |
|    (KokkosBatched Implicit Rosenbrock)              (Kokkos::TeamPolicy Explicit RK2)             |
|     Fast Species \+ Kinetic Condensation                Slow Species (VOC Precursors)              |
|     Representation-Agnostic Aerosol Math               Dynamic Sub-stepping Safeguards            |
|     Prognostic Continuous Thermodynamics                                                          |
|                     |                                           |                                 |
|                     \+---------------------+---------------------+                                 |
|                                           |                                                       |
|                      \[ Proportional Elemental Mass Reconciliation \]                               |
|                                           |                                                       |
|                      \[ Bidirectional Exaero Physical Description Interface \]                      |
|                        (Ingests Cloud Water, Outputs Optical Diagnostics)                         |
\+---------------------------------------------------------------------------------------------------+

### **2.1 Block-Sparse Build-Time Compilation (KokkosBatched) & Auto-Adjoints**

Unrolling a massive 400-species Jacobian into a single flat array assignment exhausts GPU registers, stalling the compiler. MKPP uses graph analysis to map the chemical mechanism into dense micro-blocks (e.g., 16x16 highly coupled species clusters). The emitted C++ utilizes KokkosBatched::TeamLU and KokkosBatched::TeamTrsv. Because the Jacobian is analytically derived via SymPy, the compiler also auto-generates the analytical Adjoint/TLM kernels, providing out-of-the-box compatibility for advanced 4D-Var Data Assimilation without manual developer effort.

### **2.2 Representation-Agnostic Aerosol Math**

Domain scientists can swap aerosol representations in the YAML declaration without touching C++ execution logic. The Unified Jacobian adapts its mathematical formulation automatically:

> * **Bulk/Bin:** Phase transfer is handled via flat, multi-bin kinetic flux ODEs.
> * **Modal (e.g., MAM4):** Mass and number are coupled. As mass condenses, the median diameter shifts continuously. Derivatives accommodating this shifting diameter are folded directly into the Jacobian.
> * **Sectional (e.g., SALSA):** To prevent trapped mass, condensation is coupled with an auto-injected 1D Upwind Advection flux across size boundaries.

### **2.3 Prognostic Continuous Thermodynamics (Hysteresis)**

To capture thermodynamic hysteresis (e.g., salts melting at 80% RH but freezing at 35% RH), the aqueous fraction is treated as a **Prognostic State Variable** inside the primary Kokkos::View. The Python compiler generates a differential equation accounting for both deliquescence and efflorescence triggers, allowing the implicit solver to naturally carry the metastable phase state forward in time without branching.

### **2.4 Hierarchical Multi-Rate Partitioning & Workload Sorting**

MKPP partitions species into Fast (implicit) and Slow (explicit) groups. To prevent the "Terminator Problem"—where daytime grid cells require heavy sub-stepping while nighttime cells sit idle—the host model implements a **Sorting Kernel** to sort grid cells by Solar Zenith Angle (SZA). Cells with similar computational intensity are grouped into the same Kokkos::TeamPolicy, guaranteeing perfectly balanced GPU workloads. If a team detects numerical stiffness, it dynamically triggers a nested Kokkos::TeamThreadRange to sub-step the explicit solver.

### **2.5 Strict Separation of Concerns & Proportional Mass Conservation**

**Emissions, transport, and boundary fluxes are strictly decoupled from the MKPP solver.** MKPP aligns fully with the NCAR MUSICA ecosystem, acknowledging that physical processes are mathematically distinct from chemical kinetics.

* **CECE (Community Emissions Computing Engine):** Upstream emissions processing (anthropogenic fluxes, biomass burning plume injections, lightning $NO_x$) is handled entirely by CECE. CECE passes dynamic production rates to the host model, which then feeds them into MKPP as environmental driver inputs. MKPP does not calculate emissions.
* **Extreme Environment Fuzzer:** Before the compiler’s Tarjan SCC algorithm partitions the mechanism into fast (implicit) and slow (explicit) solver blocks, the AOT compiler runs candidate mechanisms through a 0-D fuzzer. This tests extreme edge-case environments (e.g., severe wildfire smoke plumes, urban smog spikes, polar night) to guarantee no "slow" species become dynamically stiff and crash the explicit RK2 solver during runtime.
* **Algebraic Elemental Mass Conservation:** Within MKPP, internal multi-rate integration drift is not handled by crude atomic additions. Instead, SymPy automatically derives exact linear elemental balance relations for Carbon, Sulfur, Nitrogen, and Halogens. The compiler injects a zero-overhead algebraic projection step at the conclusion of the micro-block solve to enforce strict elemental conservation without skewing kinetics:

$$\mathbf{C}_{\text{projected}} = \mathbf{C} - \mathbf{E}^T \left(\mathbf{E} \mathbf{E}^T\right)^{-1} \left(\mathbf{E} \mathbf{C} - \mathbf{m}_0\right)$$



*(where $\mathbf{E}$ is the elemental stoichiometry matrix and $\mathbf{m}_0$ is the total elemental mass vector).*

### **2.6 Bidirectional Exaero & Aqueous Cloud Chemistry**

Exaero acts as a bidirectional universal translator. It abstracts raw chemical arrays into physical diagnostics (e.g., optical depth) for the host's radiation module. Concurrently, Exaero ingests Cloud Liquid Water (CLW) from the host's microphysics module. The Python DSL flags specific aqueous reactions (like in-cloud sulfate production), which the Rosenbrock solver dynamically activates proportional to the ingested CLW, accurately modeling in-cloud chemistry.

### **2.7 Spline-Interpolated Photolysis Forcing**

To prevent numerical crashes at sunrise, the host model passes photolysis rates as a time derivative (slope). The Kokkos kernel evaluates J-rates dynamically as a continuous function of time inside the implicit micro-steps, allowing the Rosenbrock solver to curve gracefully through the sunrise terminator.

### **2.8 Inputs**

Use the same inputs as MICM is using so that these files are easily interchangeable. This is fully described here (https://mechanismconfiguration.readthedocs.io/en/latest/v1/[)](https://mechanismconfiguration.readthedocs.io/en/latest/v0/index.html). More specifically, we would want options for chemical species (https://mechanismconfiguration.readthedocs.io/en/latest/v1/chemical\_species/index.html), phases (https://mechanismconfiguration.readthedocs.io/en/latest/v1/phases/index.html), and chemical reactions ([https://mechanismconfiguration.readthedocs.io/en/latest/v1/phases/index.html](https://mechanismconfiguration.readthedocs.io/en/latest/v1/phases/index.html)). No species or rates should be hard-coded. Certain phases will represent key features. For example, the “gas” phase will tell you which species should be solved by the ODE solver. The “organic” phase will tell you which species need to undergo SOA partitioning. We would also want an option to use the standard kinetic units that was available in v0 of the tool and is described here: [https://mechanismconfiguration.readthedocs.io/en/latest/v0/index.html](https://mechanismconfiguration.readthedocs.io/en/latest/v0/index.html). For simplicity, like MICM you can solve all chemistry and processes in SI units to reduce errors with unit conversions. As a second step, to make the tool more user-friendly you can add an option to convert from standard kinetic units into SI units as a second step. Examples for what this looks like for the AM4.1 mechanism are here: [https://github.com/NOAA-CSL/CATChem\_mechanisms/tree/main/mech/AM4.1](https://github.com/NOAA-CSL/CATChem_mechanisms/tree/main/mech/AM4.1). Standard kinetic units are described in [NASA-JPL\_Evaluation\_19-5.pdf](https://drive.google.com/file/d/1iAbvLc4zPVZOsfbooBPeHGymeFxkyA3-/view?usp=drive_link). These are also examples of the types of reactions that the tool must be able to ingest.

### **2.8 KPP**

You can learn about KPP here: [https://kpp.readthedocs.io/en/stable/](https://kpp.readthedocs.io/en/stable/) and the code is here: [https://github.com/KineticPreProcessor/KPP](https://github.com/KineticPreProcessor/KPP). We would like to have all of the capabilities currently available in KPP, but also adding in capabilities for multiphase chemistry applications that KPP did not have prior.

### **2.9 Solvers**

We definitely need the standard Rosenbrock solver capability available in the tool. This is described here: [https://kpp.readthedocs.io/en/stable/num\_methods/rosenbrock-methods.html](https://kpp.readthedocs.io/en/stable/num_methods/rosenbrock-methods.html) and the code is here: [https://github.com/KineticPreProcessor/KPP/blob/main/int/rosenbrock.c](https://github.com/KineticPreProcessor/KPP/blob/main/int/rosenbrock.c)

We also want this more advanced Rosenbrock solver that does Mechanism auto-reduction. This is described here: [https://kpp.readthedocs.io/en/stable/num\_methods/rosenbrock-methods.html\#rosenbrock-with-mechanism-auto-reduction](https://kpp.readthedocs.io/en/stable/num_methods/rosenbrock-methods.html#rosenbrock-with-mechanism-auto-reduction) and the code is here, but it is only available in .f90 right now so this would need to be converted to C++: [https://github.com/KineticPreProcessor/KPP/blob/main/int/rosenbrock\_autoreduce.f90.](https://github.com/KineticPreProcessor/KPP/blob/main/int/rosenbrock_autoreduce.f90) You can learn more about this Rosenbrock mechanism auto-reduction solver through this paper: [J Adv Model Earth Syst - 2023 - Lin - An Adaptive Auto‐Reduction Solver for Speeding Up Integration of Chemical Kinetics in.pdf](https://drive.google.com/file/d/1CsYqdH65sqjta3s9FOFuc_yNH3TSefHb/view?usp=drive_link)

Barry are you interested in this adjoint option: [https://kpp.readthedocs.io/en/stable/num\_methods/rosenbrock-methods.html\#rosenbrock-discrete-adjoint-model](https://kpp.readthedocs.io/en/stable/num_methods/rosenbrock-methods.html#rosenbrock-discrete-adjoint-model)?

### **2.10 Secondary Organic Aerosol**

Unlike the original version of KPP, we would like to be able to have processes built in to do key multiphase reactions within the tool in a generalized way. One of these processes is using Raoult’s equilibrium law through operator splitting to solve for secondary organic aerosol partitioning from the gas-phase to the particle phase using vapor pressure. This process will take inputs from the chemical ODE solver step. See this code to see how the SOA is described in CMAQ: [https://github.com/USEPA/CMAQ/blob/main/CCTM/src/aero/aero6/SOA\_DEFN.F](https://github.com/USEPA/CMAQ/blob/main/CCTM/src/aero/aero6/SOA_DEFN.F) . … \[Still working on this.\]  which relies on the SOA data described here: [https://github.com/USEPA/CMAQ/blob/main/CCTM/src/aero/aero6/AERO\_DATA.F](https://github.com/USEPA/CMAQ/blob/main/CCTM/src/aero/aero6/AERO_DATA.F). We would want this code generalized and not hard-coded for various species like it is now.

We would also like to be able to incorporate simple approaches to SOA chemistry that are even more computationally efficient. One of these approaches is used in the AM4.1 mechanism and this paper describes how the SOA is implemented into the model: [J Adv Model Earth Syst - 2020 - Horowitz - The GFDL Global Atmospheric Chemistry‐Climate Model AM4 1  Model Description and (1).pdf](https://drive.google.com/file/d/1X4ld7m8YNgLL7sUQICt-jeRlj7RJU7Ku/view?usp=drive_link). The code is here: [https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/gfdl\_soa\_mod.F90](https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/gfdl_soa_mod.F90)

### **2.11 Heterogenous chemistry**

**CRACMM example**
We would like to be able to include the complicated heterogenous chemistry that is included in CMAQ’s CRACMM mechanism. The CRACMM code is here: [https://github.com/USEPA/CRACMM/tree/CRACMM2/chemistry/cracmm2](https://github.com/USEPA/CRACMM/tree/CRACMM2/chemistry/cracmm2) for the basic reactions, but much of the heterogenous reactions are hard-coded into the CMAQ code as described below. You can learn more about CRACMM in this paper: [CRACMM\_Description-2023.pdf](https://drive.google.com/file/d/1V704VSBLS9cawB2OqmJon1riOE-1WVag/view?usp=drive_link)and the corresponding supplement: [CRACMM\_description-2023-supplement.pdf](https://drive.google.com/file/d/1MsJLSDQ-D-0jcMlK10sg8hgZLSDLNsjv/view?usp=drive_link).

The CMAQ code includes even more details on the CRACMM mechanism here: [https://github.com/USEPA/CMAQ/tree/main/CCTM/src/MECHS/cracmm2](https://github.com/USEPA/CMAQ/tree/main/CCTM/src/MECHS/cracmm2)
As you can see in the CRACMM mechanism file: [https://github.com/USEPA/CRACMM/blob/main/chemistry/cracmm2/mech\_cracmm2.def](https://github.com/USEPA/CRACMM/blob/main/chemistry/cracmm2/mech_cracmm2.def) there are heterogenous reactions defined (HETERO\_\*). And then these heterogenous reactions are calculated in the CMAQ model using code here: [https://github.com/USEPA/CMAQ/blob/main/CCTM/src/aero/aero6/AEROSOL\_CHEMISTRY.F](https://github.com/USEPA/CMAQ/blob/main/CCTM/src/aero/aero6/AEROSOL_CHEMISTRY.F)

We would like to be able to seamlessly call these heterogeneous reactions in a general way in MKPP unlike the traditional approach of solving these Fortran code file heterogenous reactions first and then feeding the rates into a chemical solver to solve them with the gas-phase chemistry.

**AM4.1 example**
An even simpler method of this concept can be seen with the AM4.1 chemistry. You can learn more about the AM4.1 chemistry in this paper: [J Adv Model Earth Syst - 2020 - Horowitz - The GFDL Global Atmospheric Chemistry‐Climate Model AM4 1  Model Description and (1).pdf](https://drive.google.com/file/d/1X4ld7m8YNgLL7sUQICt-jeRlj7RJU7Ku/view?usp=drive_link) and the supporting information including a table of chemical species: [am4.1 supporting information table1.pdf](https://drive.google.com/file/d/1aAHIm1D99Lm_owqSYOVLBSaoSOmXv0DX/view?usp=drive_link), photolysis reactions: [jame21213-sup-0003-2019ms002032-table\_si-s02.pdf](https://drive.google.com/file/d/1WXU_DLNjcpKSSU3PhvFloEgSB3Ncan7h/view?usp=drive_link), and chemical reactions: [jame21213-sup-0004-2019ms002032-table\_si-s03.pdf](https://drive.google.com/file/d/18yI3L6WW1rG51QS7LkS0q3D_bXWHg-Cw/view?usp=drive_link).

The AM4.1 chemistry is described here: [https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/AM4\_v20180614.inp](https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/AM4_v20180614.inp)

Like in the CRACMM example, there are some reactions that do not have rates listed in the file and are named with \[\]. These correspond to user reactions that are defined separately outside of the solver here. So the traditional code solves these fortran code reactions and then provides the rates to the chemical solver as a secondary step. We would like to combine these steps in MKPP in a generalized way: [https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/mo\_usrrxt.F90](https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/mo_usrrxt.F90).

The even more complicated stratospheric chemistry options are described in this file: [https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/strat\_chem\_utilities.F90](https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/strat_chem_utilities.F90)

### **2.12 Aqueous Phase Cloud Chemistry**

Many models also include Aqueous Phase Cloud chemistry outside of the chemical solver step. We would like MKPP to also be able to solve Aqueous Phase Cloud chemistry.

For CRACMM these processes are described here: https://github.com/USEPA/CMAQ/tree/main/CCTM/src/cloud/acm\_ae6/

For AM4.1 these processes are described here: https://github.com/jianheACM/CATChem/blob/dev-am4/src/gfdlam4chem/cloud\_chem.F90

## ---

**3\. Reference Implementation & Software Artifacts**

### **3.1 Representation-Agnostic YAML Specification (cracmm\_sectional.yaml)**

mechanism:
  name: CRACMM\_Exascale\_Sectional
  description: Multiphase mechanism with Sectional Advection and Aqueous Cloud Chemistry.

aerosol\_representation:
  type: sectional
  num\_sections: 8
  diameter\_bounds: \[0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 10.0\]
  track\_number: true

species:
  \- name: SO2
    phase: gas
    elements: { S: 1, O: 2 }
  \- name: SULFATE\_AERO
    phase: aerosol
    elements: { S: 1, O: 4 }

reactions:
  \- type: sectional\_condensation
    gas\_species: SO2
    section\_prefix: SULFATE\_AERO
    advection\_scheme: upwind\_1d

  \- type: aqueous\_cloud
    equation: "SO2 \+ H2O2 \-\> SULFATE\_AERO"
    activation\_trigger: "exaero.cloud\_liquid\_water \> 1.0e-6"

### **3.2 Bidirectional Exaero Interface Header (catchem\_exaero.hpp)**

\#ifndef CATCHEM\_EXAERO\_HPP\_
\#define CATCHEM\_EXAERO\_HPP\_

\#include \<Kokkos\_Core.hpp\>

namespace catchem {

    template \<typename MemorySpace\>
    struct ExaeroDiagnostics {
        using StateView \= Kokkos::View\<const double\*\*\*, Kokkos::LayoutRight, MemorySpace, Kokkos::MemoryUnmanaged\>;
        using CloudView \= Kokkos::View\<const double\*, Kokkos::LayoutRight, MemorySpace, Kokkos::MemoryUnmanaged\>;

        StateView raw\_chemical\_state;
        CloudView cloud\_liquid\_water;  // Ingested dynamically from Host Microphysics

        static constexpr int OPTICAL\_IDX \= 0;
        static constexpr int RADIUS\_IDX  \= 1;

        KOKKOS\_INLINE\_FUNCTION
        double get\_optical\_depth(const int cell, const int bin, const double wavelength\_factor) const {
            return raw\_chemical\_state(cell, bin, OPTICAL\_IDX) \* wavelength\_factor;
        }

        KOKKOS\_INLINE\_FUNCTION
        double get\_local\_clw(const int cell) const {
            return cloud\_liquid\_water(cell);
        }
    };

} // namespace catchem

\#endif // CATCHEM\_EXAERO\_HPP\_

### **3.3 Architecture-Aware C++ Multi-Rate Kernel (MKPP\_solver\_kernel.hpp)**

\#ifndef MKPP\_SOLVER\_KERNEL\_HPP\_
\#define MKPP\_SOLVER\_KERNEL\_HPP\_

\#include \<Kokkos\_Core.hpp\>
\#include \<KokkosBatched\_LU\_Decl.hpp\>
\#include \<KokkosBatched\_Trsv\_Decl.hpp\>

namespace catchem {
namespace MKPP {

    constexpr int NUM\_SPECIES \= 400;
    constexpr int BLOCK\_SIZE  \= 16;

    template \<typename ExecSpace\>
    struct MKPPTeamSolver {
        // Architecture-Aware Layout: Automatically selects SoA (LayoutLeft) for GPUs
        // and AoS (LayoutRight) for CPUs to guarantee 100% memory bandwidth utilization.
        using StateView \= Kokkos::View\<double\*\*, typename ExecSpace::array\_layout, typename ExecSpace::memory\_space\>;
        using TeamPolicy \= Kokkos::TeamPolicy\<ExecSpace\>;
        using MemberType \= typename TeamPolicy::member\_type;

        StateView state;
        double dt\_phys;

        KOKKOS\_INLINE\_FUNCTION
        void operator()(const MemberType& team\_member) const {
            const int cell\_idx \= team\_member.league\_rank(); // SZA-Sorted Cell Index

            // 1\. Explicit Nucleation Source Kernel
            // ... explicit gas-to-particle clustering ...

            // 2\. Explicit Slow Species with Dynamic Sub-stepping Safeguard
            double local\_error \= estimate\_rk2\_error(cell\_idx);
            int sub\_steps \= (local\_error \> 1.0e-3) ? 10 : 1;

            Kokkos::parallel\_for(Kokkos::TeamThreadRange(team\_member, sub\_steps), \[&\](const int& s) {
                // ... sub-stepped RK2 math for Slow Partition ...
            });
            team\_member.team\_barrier();

            // 3\. Implicit Fast Species (KokkosBatched Block-Sparse Solve)
            double J\_block\[BLOCK\_SIZE\]\[BLOCK\_SIZE\];

            // Evaluates Spline-Interpolated Photolysis & Aqueous CLW Triggers
            // Solves Unified Jacobian (including Sectional Advection / Modal shifting)

            KokkosBatched::TeamLU\<MemberType, KokkosBatched::Algo::LU::Unblocked\>
                ::invoke(team\_member, J\_block);

            KokkosBatched::TeamTrsv\<MemberType, KokkosBatched::Uplo::Lower, KokkosBatched::Trans::NoTranspose, KokkosBatched::Diag::Unit, KokkosBatched::Algo::Trsv::Unblocked\>
                ::invoke(team\_member, 1.0, J\_block, RHS\_block);

            // 4\. Proportional Mass Reconciliation handled post-kernel via parallel\_reduce
        }
    };

} // namespace MKPP
} // namespace catchem
\#endif

### **3.4 AOT CLI Contract & Exit Codes**

The compiler is invoked as a standalone, machine-readable command-line tool:

```text
mkpp compile <mechanism.{yaml,yml,json}> --test-env <environment.{yaml,yml,json}> --out <output-dir> [--strict] [--emit-manifest]
```

**Required Inputs**

- `<mechanism.{yaml,yml,json}>`: representation-agnostic mechanism definition.
- `--test-env <environment.{yaml,yml,json}>`: standardized validation environment that accompanies the mechanism.
- `--out <output-dir>`: writable directory for generated headers and reports.

**Channel Rules**

- `stdout` is reserved for normal progress summaries and machine-readable success output.
- `stderr` is reserved for validation errors, unsupported schema features, and stiffness diagnostics.

**Exit Code Taxonomy**

- `0`: compilation, validation, and generation succeeded.
- `1`: validation failure, unsupported chemistry, or unresolvable stiffness detected by the fuzzer.
- `2`: usage error, missing file, unreadable path, or malformed CLI invocation.

**Determinism Rule**

- Identical inputs and compiler options MUST produce byte-identical generated headers and manifests.

### **3.5 Zero-Copy Fortran Interoperability Wrapper & Interface Schema**

To ensure MKPP can be called from legacy Fortran-based Earth System Models without cross-bus copies, the compiler emits an `extern "C"` interoperability wrapper around the generated solver headers.

**Interface Ownership and Lifetime**

- Host models own the raw concentration and meteorology buffers.
- The wrapper creates `Kokkos::MemoryUnmanaged` views only for the duration of the call.
- The wrapper must not allocate replacement buffers or copy host data into temporary scratch storage.

**Array Schema**

- Concentrations: rank-4 array with explicit species and grid dimensions.
- Meteorology: rank-4 array with explicit forcing dimensions.
- Cloud liquid water: rank-1 or rank-structured host field passed separately from concentrations.
- Units: the contract must state canonical units for every field that participates in the solver input.

**Validation Requirements**

- The wrapper validates rank, extent, and unit compatibility before any Kokkos dispatch occurs.
- A mismatch in shape, units, or ownership expectations fails fast and reports the issue on `stderr`.

### **3.6 Preflight Validation & Consumer Harness Contract**

The build system must validate host integration assumptions before a runtime integration test is considered successful.

**Preflight Checks**

- Confirm the host application exposes a C-compatible entrypoint for the generated wrapper.
- Confirm cloud liquid water, meteorology, and concentration arrays are present with the expected extents.
- Confirm the build can link against the generated headers without relying on compiler-specific pragmas or private runtime assumptions.

**Consumer Harness Responsibilities**

- The downstream application must provide the `main` entrypoint and the host-memory buffers required by the generated wrapper.
- The downstream application must link the generated headers and exercise the emitted solver path with a deterministic test environment.
- The downstream application must verify at least one forward solve and one adjoint/TLM check against a known perturbation case.

### **3.7 Artifact Provenance & Reproducibility**

The AOT compiler emits a manifest alongside generated headers that records:

- input file digests for the mechanism and test environment,
- compiler version and generation options,
- artifact names and relative output paths,
- schema validation status and any non-fatal warnings.

The manifest itself must remain deterministic for identical inputs and options. If the compiler needs to emit human-oriented timestamps, those must be confined to separate logs and not embedded in the generated headers or the machine-readable manifest.

## ---

**4\. 18-Month Implementation Roadmap & WBS**

| Phase | Timeline | Description   |
| :---- | :---- | :---- |
| **Phase 1** | Months 1-3 | **DSL Core, Aerosol Logic & Adjoint Generation:** Build SymPy engine to generate analytical Jacobians, Adjoints/TLMs, and representation-agnostic aerosol logic (Modal/Sectional derivatives). Implement algorithm to identify 16x16 dense micro-blocks for KokkosBatched. |
| **Phase 2** | Months 4-6 | **Exaero Architecture & Cloud Coupling:** Implement the bidirectional Exaero API for optical diagnostics and Cloud Liquid Water ingest. Enforce DefaultExecutionSpace::array\_layout across all CATChem allocations. Build explicit parallel\_for boundary kernels for Nucleation. |
| **Phase 3** | Months 7-12 | **Hierarchical Solvers, SZA Sorting & Hysteresis:** Implement SZA workload sorting in the host driver. Implement Kokkos::TeamPolicy dynamic sub-stepping for the slow solver. Formulate prognostic differential equations for aqueous fraction and spline-interpolated J-rates. |
| **Phase 4** | Months 13-15 | **Data Assimilation Validation & Mass Auditing:** Validate Auto-Adjoints within the JEDI framework. Implement proportional parallel\_reduce elemental mass reconciliation. Execute 3D host model regional runs (UFS/CMAQ) across terminators. |
| **Phase 5** | Months 16-18 | **Exascale Optimization, CI/CD & Release:** Profile GPU kernels via NVIDIA Nsight Compute to confirm register pressure is contained via KokkosBatched and memory throughput achieves ≥ 80% theoretical bandwidth via SoA layouts. |

## **5\. Verification & Acceptance Criteria Matrix**

| Validation Metric | Methodology | Target Acceptance Threshold   |
| :---- | :---- | :---- |
| **Adjoint/TLM Validity** | Perform Taylor series tests on the auto-generated tangent linear and adjoint models via JEDI. | Machine precision agreement against finite difference perturbations. |
| **0D Box Accuracy (Sunrise)** | Compare MKPP GPU output against SUNDIALS CPU across the dawn terminator using dynamic J-rates. | Max Relative Error \< 0.1%; Zero negative radical concentrations. |
| **Aerosol Growth Spectrum** | Track physical size distribution during heavy condensation events using the 1D advection scheme. | Mass successfully transitions across Sectional/Modal Exaero boundaries (No trapped mass). |
| **Register Pressure Limits** | Profile compiler assembly output (PTX/SASS) for the KokkosBatched solver. | Max 128 registers per thread (zero local memory spilling). |
| **Memory Bandwidth Efficiency** | Profile memory layout performance (SoA vs. AoS) using Nsight Compute. | \> 80% utilization of theoretical device memory bandwidth. |
| **Terminator Load Balance** | Measure wall-clock GPU block execution times comparing sorted vs. unsorted grid cells. | Nighttime idle starvation reduced by ≥ 90%. |

## **6\. DETAILS**

I have searched the web for some additional context on MICM, OpenAtmos, and ISORROPIA to ensure the new section is as rigorous as possible.

The unified expansion below completely defines all the integrated auxiliary engines you mentioned (Cloud-J, ISORROPIA-Lite, EXAERO, SOA). Here is the proposed draft, explicitly highlighting the exact connections you requested.

---

### **Draft Expansion: Section 2.6 – Integrated Auxiliary Engine Suite & Physics Coupling**

The Multiphase Kinetic PreProcessor (MKPP) utilizes an integrated suite of auxiliary, header-only C++ engines. By building these engines natively within the Kokkos environment and compiling them alongside the AOT chemical solver, MKPP ensures that complex multiphase processes—such as photolysis, inorganic thermodynamics, and secondary organic aerosol (SOA) partitioning—are evaluated locally within hardware registers. This eliminates the massive memory-bandwidth bottlenecks caused by legacy operator splitting.

**1. Inline Cloud-J C++ (Photolysis Forcing)**
Legacy models calculate photolysis rates (J-values) in an external module and pass them across the memory bus to the chemistry solver.

* **The MKPP Method:** MKPP incorporates a header-only C++ port of the **Cloud-J** multi-scattering photolysis calculator.
* **Execution:** J-values are computed directly in the GPU thread registers immediately before the ROS-3 integration step.
* **Coupling:** Cloud-J directly queries the EXAERO interface (see below) for aerosol optical properties (extinction, single-scattering albedo, asymmetry factor) and ingests grid-cell Cloud Liquid Water (CLW) to calculate dynamically attenuated J-values, ensuring photolytic fluxes are chemically consistent with the real-time aerosol state.

**2. ISORROPIA-Lite (Inorganic Thermodynamics & Acidity)**
Predicting aerosol liquid water content and pH is notoriously difficult due to extreme non-ideality at low relative humidity (RH). Legacy modules like ISORROPIA II rely on massive, highly branched `if/else` decision trees to determine the thermodynamic state of crustal species, sulfates, nitrates, and ammonia, leading to severe GPU thread warp divergence.

* **The MKPP Method:** MKPP utilizes **ISORROPIA-Lite**, a vectorized C++ refactor.
* **Execution:** To eliminate warp divergence, ISORROPIA-Lite replaces rigid conditional thresholds with continuous, C¹-differentiable sigmoid transition curves.
* **Coupling:** ISORROPIA-Lite ingests dry and wet mass densities from EXAERO. It rapidly calculates Aerosol Liquid Water Content (ALWC) and aerosol acidity (pH), which are subsequently fed into the SymPy-generated `HETCHEM` equations to dictate heterogeneous uptake rates.

**3. EXAERO (Physical Aerosol Abstraction)**
EXAERO acts as the central physical abstraction layer, translating raw chemical concentration arrays into physical particle diagnostics.

* **Microphysics Outputs:** EXAERO calculates physical state variables such as surface area density ($S_a$), wet particle radii ($r_{\text{wet}}$), and overall density. These outputs are fed directly into the HETCHEM engine for gas-to-particle kinetic flux calculations.
* **Optical Query Interface:** EXAERO exposes C++ querying methods, allowing the Cloud-J engine to instantly request aerosol optical properties (Extinction, SSA, Asymmetry factor $g$) for radiative transfer calculations.

**4. SOA Formation via C¹ Hermite Splines**
Legacy models handle Secondary Organic Aerosol (SOA) condensation using fixed Volatility Basis Set (VBS) lookup tables or sequential Raoult's Law equilibrium solvers. These approaches introduce non-differentiable step-functions that break continuous adjoints.

* **The MKPP Method:** MKPP models SOA partitioning directly within the ODE solver. The AOT compiler utilizes SymPy to construct continuous $C^1$ cubic Hermite polynomial splines $Y(NO_x, T, RH)$ to parameterize SOA yields.
* **Execution:** Because these splines are continuously differentiable over the entire domain, they are seamlessly evaluated within the Unified Jacobian. SymPy derives the continuous partial derivatives (e.g., $\frac{\partial Y}{\partial [NO_x]}$) to ensure that both the forward integration and transposed Adjoint ($\mathbf{J}^T$) never encounter numerical gradient cliffs.

This is exactly the right approach. To capture the true power of MKPP, we can't just list the reaction types—we need to rigorously define their mathematical formulations, detail where their dynamic physical parameters come from, and explicitly explain how the SymPy compiler fuses them into a single, seamless matrix (the Unified Jacobian) without operator splitting.

Here is the expanded draft for this section. Review this depth and structure, and let me know if it hits the mark before we integrate it into the master specification.

---

### **Draft Expansion: Section 2.2 – Native MICM Reaction Types & The Unified Jacobian**

MKPP maintains strict schema compatibility with OpenAtmos / MICM mechanism definitions. However, unlike legacy solvers that use dynamic `switch/case` statements at runtime to evaluate different reaction types—causing severe GPU thread warp divergence—MKPP’s AOT Python compiler uses SymPy to symbolically parse, differentiate, and unroll all five core MICM reaction types at compile time.

This enables the formulation of a **Unified Jacobian** where gas kinetics, photolysis, and aerosol phase-transfers are evaluated simultaneously in a single, branchless ODE micro-step.

#### **1. ARRHENIUS (Standard Gas-Phase Kinetics)**

* **Formulation:** The standard temperature-dependent bimolecular or termolecular rate constant.

$$k(T) = A \cdot \left(\frac{T}{300}\right)^B \cdot \exp\left(-\frac{C}{T}\right)$$


* **Physical Drivers:** Driven purely by ambient Temperature ($T$) provided by the `METEO_STRUCT` memory view.
* **SymPy Integration:** SymPy constructs the kinetic flux $R_r = k(T) \prod [C_{\text{reactants}}]$. Because this is a purely algebraic expression, SymPy derives exact analytical partial derivatives $\frac{\partial R_r}{\partial [C_j]}$ for the Jacobian, unrolling the products into flat C++ scalar assignments.

#### **2. TROE (Pressure-Dependent Falloff)**

* **Formulation:** Reactions that transition between low-pressure and high-pressure limits (e.g., $NO_2 + OH \rightarrow HNO_3$), requiring Lindemann-Hinshelwood/Troe broadening factors.

$$k(T, P) = \left( \frac{k_0 [M]}{1 + \frac{k_0 [M]}{k_\infty}} \right) F_c^{\left( 1 + \left[ \log_{10}\left( \frac{k_0 [M]}{k_\infty} \right) / N \right]^2 \right)^{-1}}$$


* **Physical Drivers:** Requires Temperature ($T$) and total air number density ($[M]$) from the host meteorology.
* **SymPy Integration:** The AOT compiler evaluates the falloff parameters ($k_0, k_\infty, F_c, N$) symbolically. Instead of computing these complex exponents dynamically in the GPU loop, SymPy pre-forms the pressure-dependent Jacobian terms, emitting them as highly optimized, vectorized C++ math functions (`std::pow`, `std::exp`).

#### **3. PHOTOLYSIS (Light-Driven Radical Production)**

* **Formulation:** First-order photolytic cleavage driven by solar radiation.

$$R_r = J_{\text{photo}}(z, \chi, \tau) \cdot [C_{\text{reactant}}]$$


* **Physical Drivers:** The photolysis rate constant ($J_{\text{photo}}$) is calculated dynamically in hardware registers by the **Inline Cloud-J Engine**, dependent on altitude ($z$), Solar Zenith Angle ($\chi$), and aerosol/cloud optical depth ($\tau$).
* **SymPy Integration:** SymPy treats $J_{\text{photo}}$ as an independent symbolic parameter. This yields trivial, perfectly linear Jacobian terms ($\frac{\partial R_r}{\partial [C_{\text{reactant}}]} = J_{\text{photo}}$) that integrate seamlessly into the implicit solver without requiring multi-module data copying.

#### **4. HETEROGENEOUS (Uptake & Gas-to-Particle Phase Transfer)**

* **Formulation:** Pseudo-first-order kinetic fluxes representing gases colliding with and reacting upon aerosol/droplet surfaces (e.g., $N_2O_5$ hydrolysis or $SO_2$ condensation).

$$k_{het} = \frac{1}{4} \cdot \bar{v}_{gas} \cdot S_a \cdot \gamma(T, RH, pH)$$


* **Physical Drivers:** Requires the mean molecular velocity ($\bar{v}_{gas}$), aerosol surface area density ($S_a$ provided by **EXAERO**), and the uptake coefficient ($\gamma$ provided by **HETCHEM / ISORROPIA-Lite**).
* **SymPy Integration (The Phase Bridge):** This is where MKPP eliminates operator splitting. SymPy treats $k_{het}$ as a continuous kinetic flux parameter connecting two different physical phases in the *same* state vector. A single heterogeneous reaction symbolically subtracts mass from $[C_{\text{gas}}]$ and adds it to $[C_{\text{aerosol}}]$, coupling them directly in the implicit ROS-3 matrix.

#### **5. TUNNELING & C1 HERMITE SPLINES (Custom & SOA Yields)**

* **Formulation:** Custom non-Arrhenius kinetics (like quantum tunneling) or continuous multi-dimensional yield parameterizations for Secondary Organic Aerosols (SOA).

$$R_r = k \cdot Y(NO_x, T, RH) \cdot [C_{\text{precursor}}] [C_{\text{oxidant}}]$$


* **Physical Drivers:** Spline functions ($Y$) depend on dynamically shifting environmental ratios (like $NO_x$ regimes) and relative humidity.
* **SymPy Integration:** Legacy solvers use fixed Volatility Basis Set (VBS) lookup bins, which create non-differentiable step-functions. MKPP replaces these with $C^1$ cubic Hermite polynomials. SymPy symbolically differentiates the spline ($\frac{\partial Y}{\partial [NO_x]}$), ensuring that the forward Jacobian and continuous transposed Adjoint ($\mathbf{J}^T$) never encounter gradient cliffs or `if/else` boundaries.

---

#### **The Blending: Constructing the Unified Jacobian**

Because all five reaction types are processed by the same SymPy AOT compilation step, they are mathematically fused into a single unified state vector ($\mathbf{C}$):

1. **State Vector Assembly:** Gases, primary aerosols, and secondary condensed phases are stacked into one contiguous array `C[1...N]`.
2. **Total Differential Formulation:** SymPy sums the fluxes from all reaction types to form the total derivative for each species: $\frac{d[C_i]}{dt} = \sum (\text{Arrhenius} + \text{Troe} + \text{Photolysis} + \text{Heterogeneous} + \text{Splines})$.
3. **Analytical Differentiation:** SymPy computes the exact partial derivatives across all phases simultaneously ($J_{ij} = \frac{\partial f_i}{\partial [C_j]}$).
4. **Unrolled Emission:** The resulting sparse matrix is reordered via Reverse Cuthill-McKee (RCM) and emitted as a flat sequence of C++ scalar equations, allowing the GPU to solve gas chemistry, cloud chemistry, and aerosol condensation in a single, perfectly synchronized warp execution.


Here is the updated and expanded text for those four critical upgrades. You can drop these directly into your master specification document to replace the outdated legacy concepts.

### **Replacement for Section 2.5: Separation of Concerns, Fuzzing & Algebraic Mass Conservation**



---

### **Replacement for Section 2.9: Solvers & Dual-Output AOT Reduction (DRGEP)**

We require the standard fixed-stage Rosenbrock solver capabilities (e.g., ROS-3, RODAS-3) formulated as unrolled, branchless micro-block solvers to run optimally on GPU hardware.

However, unlike legacy KPP which performs mechanism auto-reduction dynamically at runtime in Fortran (incurring massive computational overhead), **MKPP shifts auto-reduction entirely to the Ahead-Of-Time (AOT) Python compiler.**

When the `enable_drgep: true` flag is activated in the YAML configuration, the AOT compiler executes Direct Relation Graph with Error Propagation (DRGEP) and flux-weighted $RO_2$ radical lumping during the build phase. In a single pass, the compiler emits **two distinct, fully unrolled C++ headers**:

1. `MKPP_solver_full.hpp`: The 100% unreduced reference solver used for ground-truth scientific validation and benchmarking.
2. `MKPP_solver_reduced.hpp`: The highly pruned production solver (target $\le 55$ active tracers) containing only the tightly coupled pathways necessary for operational exascale runs.

Both headers retain full support for SymPy-generated analytical Adjoints ($\mathbf{J}^T$) and Tangent Linear Models (TLM) required by the JEDI 4D-Var Data Assimilation framework.

---

### **New Addition: Section 3.4 Zero-Copy Fortran Interoperability Wrapper**

To ensure MKPP can be called natively by legacy Fortran-based Earth System Models (like CMAQ, GEOS-Chem, or WRF-GC) without incurring data-transfer bottlenecks, the AOT compiler generates a standardized `extern "C"` wrapper using `ISO_C_BINDING`. Raw Fortran device pointers are wrapped directly into `Kokkos::MemoryUnmanaged` views using `Kokkos::LayoutLeft`, guaranteeing zero memory allocations or cross-bus copies during integration.

**`catchem_MKPP_wrapper.cpp`**

```cpp
#ifndef CATCHEM_MKPP_WRAPPER_HPP_
#define CATCHEM_MKPP_WRAPPER_HPP_

#include <Kokkos_Core.hpp>
#include "MKPP_solver_reduced.hpp"

extern "C" {

// C-compatible interface for Fortran ISO_C_BINDING
void run_MKPP_step_c(
    double* raw_conc_ptr,    // Device pointer to 4D Fortran concentration array
    double* raw_meteo_ptr,   // Device pointer to 4D Fortran meteorology array
    const double dt,         // Physics timestep
    const int n_lon,
    const int n_lat,
    const int n_alt,
    const int n_species)
{
    // Wrap Fortran VRAM pointers in unmanaged Kokkos Views
    // Enforce LayoutLeft (Structure of Arrays) to match Fortran and maximize GPU coalescing
    using View4D = Kokkos::View<double****, Kokkos::LayoutLeft, Kokkos::DefaultExecutionSpace::memory_space, Kokkos::MemoryUnmanaged>;

    View4D conc_view(raw_conc_ptr, n_species, n_lon, n_lat, n_alt);
    View4D meteo_view(raw_meteo_ptr, 10, n_lon, n_lat, n_alt); // T, P, RH, etc.

    // Calculate total grid cells for 1D parallel dispatch
    const int total_cells = n_lon * n_lat * n_alt;

    // Launch parallel dispatch using SZA sorted TeamPolicy (as defined in 2.4)
    Kokkos::parallel_for("MKPP_3D_Integration",
        Kokkos::TeamPolicy<Kokkos::DefaultExecutionSpace>(total_cells, Kokkos::AUTO),
        catchem::MKPP::MKPPTeamSolver<Kokkos::DefaultExecutionSpace>(conc_view, meteo_view, dt)
    );
}

} // extern "C"
#endif // CATCHEM_MKPP_WRAPPER_HPP_

```