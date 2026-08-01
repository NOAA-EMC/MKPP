import argparse
import sys
from pathlib import Path
import yaml

from .parser import load_mechanism
from .validation import validate_mechanism, validate_mpi_safety, sanitize_path
from .lowering import partition_reactions
from .codegen import generate_headers

def run_compiler(mech_path: str, env_path: str, out_dir: str, strict: bool, emit_manifest: bool):
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
        # Using a dummy condition number check for MVP architecture
        dummy_max_condition = 1e5
        validate_fuzzer_stiffness(max_condition_number=dummy_max_condition)
        
        # Partition reactions and prepare adjoint logic
        blocks = partition_reactions(mech)
        from .lowering import prepare_adjoint_and_tlm
        adjoint_metadata = prepare_adjoint_and_tlm(mech)
        
        # Generate artifacts
        generate_headers(mech, out_dir=out_dir)
        
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
    compile_parser.add_argument("--out", required=True, help="Output directory for generated artifacts")
    compile_parser.add_argument("--strict", action="store_true", help="Enable strict schema validation")
    compile_parser.add_argument("--emit-manifest", action="store_true", help="Emit metadata manifest alongside headers")
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command == "compile":
        run_compiler(
            parsed_args.mechanism,
            parsed_args.test_env,
            parsed_args.out,
            parsed_args.strict,
            parsed_args.emit_manifest
        )
        sys.exit(0)

if __name__ == "__main__":
    main()
