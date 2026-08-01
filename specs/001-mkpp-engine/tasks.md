# Tasks: MKPP Engine

**Input**: Design documents from `/specs/001-mkpp-engine/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included where needed for CLI behavior, schema validation, generated code, and runtime integration.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] [SUBAGENT] Create the `src/mkpp/` Python package skeleton and module files in `src/mkpp/__init__.py`, `src/mkpp/cli.py`, `src/mkpp/model.py`, `src/mkpp/parser.py`, `src/mkpp/validation.py`, `src/mkpp/lowering.py`, and `src/mkpp/codegen.py`
- [ ] T002 Update the repository packaging and CLI entrypoint configuration in `pyproject.toml` to expose `mkpp` as a console script and include the new package
- [ ] T003 [P] [SUBAGENT] Create the Python test layout in `tests/python/test_cli.py`, `tests/python/test_validation.py`, and `tests/python/test_codegen.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Define the shared compiler dataclasses and enum-like types in `src/mkpp/model.py` for mechanism definitions, test-environment definitions, species, phases, reactions, and generated artifacts
- [x] T005 [P] [SUBAGENT] Implement strict YAML/JSON loading and normalization helpers in `src/mkpp/parser.py` for mechanism and test-environment inputs
- [x] T006 [P] [SUBAGENT] Implement deterministic schema validation and path-sanitization rules in `src/mkpp/validation.py` for required fields, finite numeric values, and cross-reference checks
- [x] T007 Implement the compiler orchestration helpers in `src/mkpp/lowering.py` that partition reactions into deterministic solver blocks and prepare symbolic lowering inputs
- [x] T008 Implement the artifact manifest and header-emission helpers in `src/mkpp/codegen.py` so downstream user stories can write deterministic outputs with digests and metadata
- [x] T042 [REVIEW] Implement the Extreme Environment Fuzzer compile gate in `src/mkpp/validation.py` and `src/mkpp/cli.py` with deterministic stiffness classification and required non-zero exit behavior for unresolvable stiffness
- [x] T043 [REVIEW] Add explicit no-root-rank aggregation and MPI safety verification rules in `src/mkpp/validation.py` and `contracts/test-environment-schema.md` for distributed execution constraints

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ahead-of-Time Mechanism Compilation & Adjoint Generation (Priority: P1) 🎯 MVP

**Goal**: Parse representation-agnostic chemistry definitions and generate deterministic Kokkos-based solver headers plus adjoint/TLM artifacts from the AOT compiler CLI.

**Independent Test**: Running `python -m mkpp compile <mechanism> --test-env <environment> --out <dir>` on a valid fixture should emit deterministic headers, a manifest, and adjoint/TLM artifacts without requiring a standalone test harness.

### Tests for User Story 1 (MANDATORY - blocks implementation) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation. Required by Constitution.**

- [x] T009 [P] [TDD] [US1] Add CLI contract tests in `tests/python/test_cli.py` for `mkpp compile`, `--test-env`, `--out`, `--strict`, `--emit-manifest`, stdout/stderr separation, and exit codes
- [x] T010 [P] [TDD] [US1] Add parser and validation tests in `tests/python/test_validation.py` for malformed mechanism files, malformed test-environment files, and deterministic failure modes
- [x] T011 [P] [TDD] [US1] Add code-generation tests in `tests/python/test_codegen.py` for byte-stable manifest content, deterministic header emission, and presence of adjoint/TLM artifact records

### Implementation for User Story 1

- [x] T012 [US1] [REVIEW] Implement the top-level CLI entrypoint and argument handling in `src/mkpp/cli.py` using the contract defined in `contracts/cli.md`
- [x] T013 [US1] Wire parser, validation, lowering, and code generation together in `src/mkpp/cli.py` so valid inputs reach artifact emission and invalid inputs fail on stderr with the correct exit code
- [x] T014 [US1] Implement mechanism parsing and canonicalization in `src/mkpp/parser.py` for species, phases, reactions, and units from YAML/JSON inputs
- [x] T015 [US1] Implement symbolic lowering hooks in `src/mkpp/lowering.py` for analytical Jacobian, adjoint, and tangent-linear preparation
- [x] T016 [US1] [REVIEW] Implement deterministic header and manifest emission in `src/mkpp/codegen.py` for generated solver artifacts and provenance metadata
- [x] T017 [US1] Add the minimal generated-artifact validation fixture and documentation updates in `specs/001-mkpp-engine/quickstart.md` so the CLI contract can be exercised consistently
- [x] T044 [US1] [REVIEW] Add native runtime integration checks in `src/exaero/tests/CMakeLists.txt` and `specs/001-mkpp-engine/quickstart.md` to validate generated artifacts through the ctest path

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Bidirectional Host Interface & Cloud Coupling (Priority: P1)

**Goal**: Define the bidirectional zero-copy host interface for cloud liquid water ingest and optical diagnostics so the generated solver can interoperate with host-model memory without copies.

**Independent Test**: A consumer application can validate the interface schema against the generated headers, map host buffers without copying, and query a deterministic optical diagnostic value from the wrapped views.

### Tests for User Story 2 (MANDATORY - blocks implementation) ⚠️

- [ ] T018 [P] [TDD] [US2] Add interface schema tests in `tests/python/test_validation.py` for rank, extent, unit, and ownership validation of host-facing arrays
- [ ] T019 [P] [TDD] [US2] Add zero-copy contract tests in `tests/python/test_codegen.py` for generated manifest metadata describing unmanaged layout and host-buffer lifetimes

### Implementation for User Story 2

- [ ] T020 [US2] [SUBAGENT] Extend `src/mkpp/model.py` with explicit host-interface metadata for concentration arrays, meteorology arrays, cloud liquid water, and optical diagnostics
- [ ] T021 [US2] [REVIEW] Implement zero-copy interface generation in `src/mkpp/codegen.py` so emitted headers document unmanaged views, LayoutLeft expectations, and lifetime rules
- [ ] T022 [US2] [REVIEW] Add preflight host-compatibility checks in `src/mkpp/validation.py` for C-compatible entrypoints, shape compatibility, and canonical units before code generation
- [ ] T023 [US2] Update `contracts/test-environment-schema.md` and `docs/Project Plan_ Next-Gen Multiphase Atmospheric Chemistry Solver (Futuristic KPP) V8.md` to document the interface schema and host preflight contract

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Hierarchical Multi-Rate Solver & Workload Sorting (Priority: P2)

**Goal**: Partition solver work into fast and slow paths, preserve deterministic workload ordering, and support workload sorting for dawn terminator balance.

**Independent Test**: The lowering and code-generation layers can produce sorted solver metadata for a representative mechanism, and the generated artifacts record the solver partitioning deterministically.

### Tests for User Story 3 (MANDATORY - blocks implementation) ⚠️

- [ ] T024 [P] [TDD] [US3] Add workload-partitioning tests in `tests/python/test_validation.py` for solver-block classification and deterministic ordering
- [ ] T025 [P] [TDD] [US3] Add sorted-artifact tests in `tests/python/test_codegen.py` for stable solver metadata when reaction ordering changes

### Implementation for User Story 3

- [ ] T026 [US3] [SUBAGENT] Implement deterministic solver partition metadata in `src/mkpp/lowering.py` for fast/slow species, SZA sorting, and micro-block grouping
- [ ] T027 [US3] [REVIEW] Emit solver-partition annotations in `src/mkpp/codegen.py` so generated headers preserve workload-sorting metadata for downstream consumers
- [ ] T028 [US3] Add sunrise/terminator validation cases in `tests/python/test_validation.py` to assert that abrupt photolysis changes do not invalidate the partitioning contract

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should work independently

---

## Phase 6: User Story 4 - Aerosol Math & Algebraic Mass Conservation (Priority: P2)

**Goal**: Enforce proportional elemental mass conservation and continuous thermodynamics behavior across aerosol representations without rigid branching.

**Independent Test**: The compiler can lower aerosol-related reactions into deterministic artifact metadata that preserves conservation and continuous transition annotations for downstream validation.

### Tests for User Story 4 (MANDATORY - blocks implementation) ⚠️

- [ ] T029 [P] [TDD] [US4] Add mass-conservation tests in `tests/python/test_validation.py` for elemental balance and conservation metadata
- [ ] T030 [P] [TDD] [US4] Add continuous-transition tests in `tests/python/test_codegen.py` for hysteresis and smooth transition annotations in generated artifacts

### Implementation for User Story 4

- [ ] T031 [US4] [SUBAGENT] Extend `src/mkpp/model.py` with aerosol-representation metadata for bulk, modal, and sectional handling plus continuous-transition flags
- [ ] T032 [US4] [REVIEW] Implement algebraic mass-reconciliation metadata in `src/mkpp/lowering.py` so generated solver blocks carry elemental conservation requirements
- [ ] T033 [US4] [REVIEW] Emit continuous-thermodynamics annotations in `src/mkpp/codegen.py` for hysteresis, spline transitions, and smooth phase-change handling
- [ ] T034 [US4] Add aerosol-math validation cases in `tests/python/test_validation.py` for species balances, phase-transition metadata, and unsupported reaction combinations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish, Compliance & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 [P] [SUBAGENT] Update `specs/001-mkpp-engine/quickstart.md` and `docs/Project Plan_ Next-Gen Multiphase Atmospheric Chemistry Solver (Futuristic KPP) V8.md` with the final CLI invocation, expected outputs, and validation flow
- [ ] T036 Verify EE2 CI/CD gates in `.github/workflows/ci.yml` and any touched build scripts so linting, testing, and environment validation remain ahead of packaging
- [ ] T037 [REVIEW] Verify zero-copy interoperability and layout expectations in `src/mkpp/codegen.py` and `contracts/test-environment-schema.md` after all user stories are combined
- [ ] T038 [REVIEW] Verify deterministic artifact provenance and manifest contents in `src/mkpp/codegen.py` and `tests/python/test_codegen.py`
- [ ] T039 [P] [SUBAGENT] Add any missing unit or integration coverage in `tests/python/` for edge cases discovered during implementation
- [ ] T040 Perform security hardening checks for path sanitization and hardcoded-secret avoidance in `src/mkpp/validation.py` and `src/mkpp/cli.py`
- [ ] T041 Run the documented quickstart validation flow from `specs/001-mkpp-engine/quickstart.md` and confirm the emitted artifacts match the contract
- [ ] T045 [REVIEW] Add register-pressure profiling verification in `specs/001-mkpp-engine/quickstart.md` and `tests/python/test_codegen.py` using Nsight Compute to assert <= 64 registers per thread, aligned to SC-004
- [ ] T046 [REVIEW] Add memory-bandwidth profiling verification in `specs/001-mkpp-engine/quickstart.md` and `tests/python/test_codegen.py` with a pass/fail threshold aligned to SC-005
- [x] T047 [REVIEW] Add a deterministic regex-based negative assertion in `tests/python/test_codegen.py` to reject any generated C++ headers containing raw `#pragma omp` or `#pragma acc` directives, enforcing FR-002

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Add CLI contract tests in tests/python/test_cli.py for mkpp compile, --test-env, --out, --strict, --emit-manifest, stdout/stderr separation, and exit codes"
Task: "Add parser and validation tests in tests/python/test_validation.py for malformed mechanism files, malformed test-environment files, and deterministic failure modes"
Task: "Add code-generation tests in tests/python/test_codegen.py for byte-stable manifest content, deterministic header emission, and presence of adjoint/TLM artifact records"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence