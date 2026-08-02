# Tasks: MKPP AMORE Lumping Engine

**Input**: Design documents from `specs/010-mkpp-amore-lumping-engine/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `src/mkpp/amore.py` module skeleton

**Execution notes**: No special discipline required. Verify project builds before proceeding.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 [P] [TDD] Implement `LumpingRule` entity and YAML validation logic in `src/mkpp/amore.py`
- [x] T003 [P] [TDD] Implement `CollapsedReaction` data model in `src/mkpp/amore.py`

**Execution notes**: Tasks marked [TDD] — write tests first, verify they fail, then implement.

**Checkpoint**: Foundation ready. Get human approval before starting user stories.

---

## Phase 3: User Story 1 - Mechanism Surrogating & Reaction Merging (Priority: P1)

**Goal**: Automatically map explicit VOCs to surrogate classes and collapse redundant reactions.
**Independent Test**: Provide an explicit mechanism, apply lumping rules, and check if explicit species are collapsed and rates are concentration-weighted.

### Tests for User Story 1 (if TDD applies)

- [x] T004 [P] [TDD] [US1] Write unit tests for explicit species substitution in `tests/python/test_amore.py`
- [x] T005 [P] [TDD] [US1] Write unit tests for reaction merging and $A_{eff}$ calculation in `tests/python/test_amore.py`

### Implementation for User Story 1

- [x] T006 [US1] Implement AST explicit species substitution in `src/mkpp/amore.py`
- [x] T007 [US1] Implement reaction merging and effective rate expression ($A_{eff}$) calculation in `src/mkpp/amore.py`

**Execution notes**: T006 and T007 handle the core AST node collapsing.

**Checkpoint**: User Story 1 fully functional and testable. Get human approval.

---

## Phase 4: User Story 2 - Automated Carbon & Mass Conservation (Priority: P1)

**Goal**: Generate stoichiometric product multipliers to ensure carbon/mass conservation.
**Independent Test**: Verify product yields of collapsed reactions include correct carbon-scaling factors.

### Tests for User Story 2 (if TDD applies)

- [x] T008 [P] [TDD] [US2] Write unit tests for carbon scaling factors calculation in `tests/python/test_amore.py`

### Implementation for User Story 2

- [x] T009 [US2] Implement carbon atoms extraction from species definitions in `src/mkpp/amore.py`
- [x] T010 [US2] Implement carbon-scaling factor injection into surrogate product yields in `src/mkpp/amore.py`

**Checkpoint**: User Story 2 works independently and maintains mass conservation. Get human approval.

---

## Phase 5: User Story 3 - Replacement of Destructive DRGEP (Priority: P1)

**Goal**: CLI integration to trigger AMORE instead of DRGEP using the `--lump` flag.
**Independent Test**: Run `mkpp compile --lump rules.yaml` and verify AMORE is executed while DRGEP is bypassed.

### Tests for User Story 3 (if TDD applies)

- [x] T011 [P] [TDD] [US3] Write tests for `--lump` flag parsing and parser hooking in `tests/python/test_amore.py` (or test_cli.py)

### Implementation for User Story 3

- [x] T012 [P] [US3] Update `src/mkpp/cli.py` to accept `--lump <filepath>` argument
- [x] T013 [US3] Modify `src/mkpp/parser.py` to invoke AMORE engine before DRGEP bypass when `--lump` is provided

**Checkpoint**: User Story 3 works. CLI integration complete. Get human approval.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T014 [P] Validate E2E output against dummy mechanism using guide in `specs/010-mkpp-amore-lumping-engine/quickstart.md`
- [x] T015 [P] Run C++ end-to-end Kokkos solver tests (`tests/integration/test_e2e_mechanisms.cpp`) to verify block-sparse generated headers are valid
- [x] T016 Run full pytest suite — all tests must pass
- [x] T017 Code cleanup, refactoring, and documentation updates for `amore.py`

**Execution notes**: Final verification of block-sparse C++ compilation and numerical conservation.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3-5)**: Depend on Foundational completion. US1 should ideally precede US2, but US3 (CLI) can run in parallel.
- **Polish (Final Phase)**: Depends on all user stories being complete

### Parallel Opportunities

- T002 and T003 can run in parallel.
- Test implementations (T004, T005, T008, T011) can run in parallel before their respective implementation tasks.
- T012 (CLI update) can run independently of the core AST engine.
