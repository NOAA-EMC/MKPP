# Quickstart & Validation Guide

## Overview
This guide validates that the MKPP AMORE Lumping Engine correctly parses lumping rules, merges explicit reactions into a surrogate reaction, ensures carbon conservation, and bypassed DRGEP.

## Prerequisites
- A functional Python 3.14+ environment with `mkpp` installed.
- A dummy explicit mechanism (e.g., `mechanisms/lumping_test.yaml`) and a lumping rule file (`mechanisms/lumping_rules.yaml`).

## Setup

1. **Create the lumping rule file (`mechanisms/lumping_rules.yaml`)**:
   ```yaml
   surrogates:
     ALK_SURR:
       explicit_species:
         - ETHANE
         - PROPANE
       weights:
         ETHANE: 0.6
         PROPANE: 0.4
   ```

## Test / Run Commands

1. **Compile with Lumping Engine Enabled**:
   ```bash
   mkpp compile mechanisms/lumping_test.yaml --lump mechanisms/lumping_rules.yaml
   ```

2. **Verify Output**:
   Check the generated `mkpp-generated/lumping_test_reduced.yaml` (or equivalent generated header).
   - Ensure `ETHANE` and `PROPANE` are not present.
   - Ensure `ALK_SURR` is present.
   - Look for the merged reaction and verify the product multipliers account for the carbon ratio.
   
3. **C++ End-to-End Test**:
   ```bash
   cd build
   cmake ..
   make
   ./tests/integration/test_e2e_mechanisms
   ```
   Ensure the solver compiles and runs without any missing variable/species errors.
