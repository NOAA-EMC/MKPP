# Governed Python contract tests are deliberately small and non-publishable. Controlled-hardware
# campaigns remain opt-in and are never CTest assertions.
find_package(
  Python3
  COMPONENTS Interpreter
  REQUIRED)

set(_solver_benchmark_tests
    ${CMAKE_SOURCE_DIR}/tests/python/benchmark/test_runner_result_schema.py
    ${CMAKE_SOURCE_DIR}/tests/python/benchmark/test_orchestrator.py
    ${CMAKE_SOURCE_DIR}/tests/python/benchmark/test_admission.py
    ${CMAKE_SOURCE_DIR}/tests/python/benchmark/test_cli.py)

# -o addopts= clears the project-wide pytest addopts (which include "-n auto" from pytest-xdist).
# This CTest invokes a small explicit file list serially and must not depend on xdist being
# importable by the configure-time Python3 interpreter, which can differ from the interpreter pip
# installs into in CI.
add_test(NAME solver_benchmark_contract_admission_smoke
         COMMAND ${Python3_EXECUTABLE} -m pytest -q -o addopts= ${_solver_benchmark_tests})
set_tests_properties(
  solver_benchmark_contract_admission_smoke
  PROPERTIES LABELS "solver-benchmark;non-publishable;contract;admission" WORKING_DIRECTORY
             ${CMAKE_SOURCE_DIR} ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}/src")
