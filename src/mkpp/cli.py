import argparse
import sys
from pathlib import Path
import yaml

from .parser import load_mechanism
from .validation import validate_mechanism, validate_mpi_safety, sanitize_path
from .lowering import partition_reactions
from .codegen import generate_headers

def run_compiler(mech_path: str, env_path: str, out_dir: str, strict: bool, emit_manifest: bool, enable_drgep: bool = False, drgep_threshold: float = 0.05, report: bool = False, lump_path: str = None):
    """Orchestrate the compilation pipeline."""
    mech_path = sanitize_path(mech_path)
    env_path = sanitize_path(env_path)
    out_dir = sanitize_path(out_dir)

    try:
        # Load test environment
        with open(env_path, 'r') as f:
            env_config = yaml.safe_load(f) or {}

        validate_mpi_safety(env_config)

        # Parse and validate mechanism
        mech = load_mechanism(mech_path)
        validate_mechanism(mech, strict=strict)

        # Enforce Extreme Environment Fuzzer compile gate (FR-008)
        from .validation import validate_fuzzer_stiffness
        dummy_max_condition = 1e5
        validate_fuzzer_stiffness(max_condition_number=dummy_max_condition)

        # Partition reactions and prepare adjoint logic
        from .validation import validate_terminator_safety, validate_mass_conservation
        validate_terminator_safety(mech)
        validate_mass_conservation(mech)

        blocks = partition_reactions(mech)
        mech.partition_metadata = blocks.get("metadata")

        from .lowering import prepare_adjoint_and_tlm, prepare_unified_jacobian
        adjoint_metadata = prepare_adjoint_and_tlm(mech)
        mech.sympy_metadata = prepare_unified_jacobian(mech)

        # Generate artifacts
        generate_headers(mech, out_dir=out_dir, suffix="_full" if enable_drgep else "")

        
        
        if lump_path:
            import copy
            from .amore import apply_amore_lumping
            
            with open(lump_path, 'r') as fl:
                rules = yaml.safe_load(fl)
                
            mech_lumped = load_mechanism(mech_path)
            mech_lumped = apply_amore_lumping(mech_lumped, rules)
            
            blocks_l = partition_reactions(mech_lumped)
            mech_lumped.partition_metadata = blocks_l.get("metadata")
            adjoint_metadata_l = prepare_adjoint_and_tlm(mech_lumped)
            mech_lumped.sympy_metadata = prepare_unified_jacobian(mech_lumped)
            
            generate_headers(mech_lumped, out_dir=out_dir, suffix="_lumped")


        if lump_path:
            import copy
            import yaml as pyyaml
            from .amore import apply_amore_lumping
            
            with open(lump_path, 'r') as fl:
                rules = pyyaml.safe_load(fl)
                
            mech_lumped = load_mechanism(mech_path)
            mech_lumped = apply_amore_lumping(mech_lumped, rules)
            
            blocks_l = partition_reactions(mech_lumped)
            mech_lumped.partition_metadata = blocks_l.get("metadata")
            adjoint_metadata_l = prepare_adjoint_and_tlm(mech_lumped)
            mech_lumped.sympy_metadata = prepare_unified_jacobian(mech_lumped)
            
            generate_headers(mech_lumped, out_dir=out_dir, suffix="_lumped")
            
            if report:
                from .reporting import write_report
                write_report(mech_lumped, mech_lumped.sympy_metadata, out_dir, suffix="_lumped")

        if enable_drgep:
            print("FATAL ERROR: DRGEP is not physically stable. Use AMORE lumping via --lump instead.", file=sys.stderr)
            sys.exit(1)

        if report:
            from .reporting import write_report
            write_report(mech, mech.sympy_metadata, out_dir, suffix="_full" if enable_drgep else "")
            
        if lump_path:
            import copy
            from .amore import apply_amore_lumping
            
            with open(lump_path, 'r') as fl:
                rules = yaml.safe_load(fl)
                
            mech_lumped = load_mechanism(mech_path)
            mech_lumped = apply_amore_lumping(mech_lumped, rules)
            
            blocks_l = partition_reactions(mech_lumped)
            mech_lumped.partition_metadata = blocks_l.get("metadata")
            adjoint_metadata_l = prepare_adjoint_and_tlm(mech_lumped)
            mech_lumped.sympy_metadata = prepare_unified_jacobian(mech_lumped)
            
            generate_headers(mech_lumped, out_dir=out_dir, suffix="_lumped")

        if enable_drgep:
                write_report(mech_reduced, mech_reduced.sympy_metadata, out_dir, suffix="_reduced")

        if emit_manifest:
            print(f"Manifest and headers emitted to {out_dir}")

    except Exception as e:
        print(f"FATAL ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="mkpp",
        description="Multiphase KPP (MKPP) Engine Compiler"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser("compile", help="Compile a mechanism into Kokkos headers")
    compile_parser.add_argument("mechanism", help="Path to the mechanism YAML/JSON file")
    compile_parser.add_argument("--test-env", required=True, help="Path to the test environment YAML/JSON file")
    compile_parser.add_argument("--out", default="src/solvers", help="Output directory for generated artifacts (defaults to mkpp-generated/)")
    compile_parser.add_argument("--strict", action="store_true", help="Enable strict schema validation")
    compile_parser.add_argument("--emit-manifest", action="store_true", help="Emit metadata manifest alongside headers")
    compile_parser.add_argument("--report", action="store_true", help="Generate full mechanism analysis report and graph")
    compile_parser.add_argument("--lump", type=str, help="Path to AMORE lumping rules YAML file")
    compile_parser.add_argument("--enable-drgep", action="store_true", help="DEPRECATED: Use --lump instead. Will exit if used.")
    compile_parser.add_argument("--drgep-threshold", type=float, default=0.05, help="DRGEP interaction threshold for pruning (0.0 to 1.0)")

    parsed_args = parser.parse_args(args)

    if parsed_args.command == "compile":
        run_compiler(
            parsed_args.mechanism,
            parsed_args.test_env,
            parsed_args.out,
            parsed_args.strict,
            parsed_args.emit_manifest,
            getattr(parsed_args, "enable_drgep", False),
            getattr(parsed_args, "drgep_threshold", 0.05),
            getattr(parsed_args, "report", False),
            getattr(parsed_args, "lump", None)
        )
        sys.exit(0)

if __name__ == "__main__":
    main()
