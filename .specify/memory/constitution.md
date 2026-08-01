<!-- 
Sync Impact Report:
- Version change: initial -> 1.0.0
- Principles added: I. Clarity Over Cleverness, II. Defensive Programming, III. Fail Fast, Fail Loudly, IV. High-Performance Computing & Message Passing (MPI), V. GPU Acceleration & Kokkos, VI. Zero-Copy Data Interoperability, VII. Scientific Hygiene & Determinism
- Sections added: Security & Federal Compliance, EE2 Compliance & CI/CD Workflow
- Removed sections: None
- Templates requiring updates: 
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
-->

# FKPP Constitution

## Core Principles

### I. Clarity Over Cleverness
Code inside this repository is co-authored and maintained by professional software engineers and domain atmospheric scientists. Avoid obscure syntax tricks, heavily obfuscated macro loops, or deeply nested pointer structures. Write self-documenting code with explicit variable and function naming conventions. Zero dead code allowed.

### II. Defensive Programming
Assume inputs (such as file reads, sensor inputs, or grid metrics) can be corrupted, malformed, or missing. Validate bounds, verify shapes, and test file descriptors explicitly before allowing execution to proceed into tight compute loops.

### III. Fail Fast, Fail Loudly
If a script or compiled unit detects a structural environmental failure (e.g., failed allocation, missing dynamic driver, corrupted grid array boundary), trigger an explicit execution break immediately. Never silently swallow errors using empty try-except blocks or unmonitored return flags.

### IV. High-Performance Computing & Message Passing (MPI)
Assume code executes within a distributed MPI framework. Always design operations with proper communicator awareness (`MPI_COMM_WORLD` or custom sub-communicators). Ensure matching non-blocking pairs to prevent deadlocks. Never gather multidimensional grid data or massive model states onto a single root rank for processing or serial disk output to prevent OOM failures.

### V. GPU Acceleration & Kokkos
Use `Kokkos::TeamPolicy` and `Kokkos::TeamThreadRange` to manage dynamic sub-stepping and ensure perfectly balanced GPU workloads. Never use `switch/case` or heavy `if/else` logic for evaluating thermodynamic phase branches inside Kokkos kernels to prevent warp divergence. Use `KokkosBatched` for localized, dense micro-matrix calculations to respect GPU register limits.

### VI. Zero-Copy Data Interoperability
Always track backend orientation during cross-language array sharing (C/C++ row-major vs. Fortran column-major). For modern C++ and Fortran handshakes, enforce zero-copy array views using C++23's `std::mdspan` with `std::layout_left` (or `Kokkos::LayoutLeft` with `Kokkos::MemoryUnmanaged`) to natively align data layouts to Fortran spatial arrays.

### VII. Scientific Hygiene & Determinism
Scientific results MUST be completely reproducible (no non-deterministic algorithms, race conditions, or unseeded random state initialization). No operator splitting: evaluate gas kinetics, photolysis, and phase-transfers simultaneously using a Unified Jacobian. Replace rigid conditional thresholds with continuous, analytically differentiable curves. Enforce bounds checking and boundary conditions for model grid physical walls.

## Security & Federal Compliance

As a federal information system, security is paramount.
- **No Hardcoded Secrets**: NEVER hardcode API keys, passwords, AWS credentials, or tokens. Inject via secure environment variables or vault integrations.
- **Path Sanitization**: Prevent directory traversal attacks by rigorously sanitizing path inputs before file I/O operations.
- **Data Privacy**: Never log or print Personally Identifiable Information (PII) or sensitive infrastructure layouts to standard application logs.

## EE2 Compliance & CI/CD Workflow

For any generated workflow (CI/CD or operational job chain), enforce the following gate order:
1. **Environment Validation**: Verify required modules, variables, and paths before compute steps.
2. **Static Quality Gates**: Run formatting/linting checks and fail immediately on violations.
3. **Test Gates**: Run unit/integration tests before any packaging, artifact publication, or deployment step.
4. **EE2 Policy Gates**: Validate output destinations and execution model rules (no background processing, approved paths, restart behavior).
5. **Build/Package/Deploy**: Execute only if all prior gates pass.

Any failing gate MUST stop the workflow and emit a clear `FATAL ERROR:`-prefixed message in logs.

## Governance

- The Constitution supersedes all other practices and acts as the supreme standard for MKPP/FKPP.
- All pull requests, reviews, and implementations MUST verify compliance with these rules, as specified in `.github/copilot-instructions.md`.
- Amendments require documentation, approval, and a semantic version bump.

**Version**: 1.0.0 | **Ratified**: 2026-07-31 | **Last Amended**: 2026-07-31
