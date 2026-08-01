import pytest
from mkpp.cli import main

def test_cli_help(capsys):
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Compile a mechanism into Kokkos headers" in captured.out

def test_cli_compile_missing_args(capsys):
    with pytest.raises(SystemExit) as e:
        main(["compile"])
    assert e.value.code != 0
    captured = capsys.readouterr()
    assert "error: the following arguments are required: mechanism" in captured.err.lower()

def test_cli_compile_success(tmp_path, capsys, monkeypatch):
    mech_file = tmp_path / "mech.yaml"
    mech_file.write_text("""
    species: [{name: O3}]
    reactions: []
    """)
    test_env_file = tmp_path / "env.yaml"
    test_env_file.write_text("mpi: {gather_to_root: false}")
    out_dir = tmp_path / "build"

    # Simulate success
    monkeypatch.setattr("mkpp.cli.run_compiler", lambda *args, **kwargs: None)
    
    with pytest.raises(SystemExit) as e:
        main(["compile", str(mech_file), "--test-env", str(test_env_file), "--out", str(out_dir), "--emit-manifest"])
    assert e.value.code == 0

def test_cli_compile_fatal_error(capsys, monkeypatch, tmp_path):
    # Simulate a deep failure in the pipeline
    def mock_load_mechanism(*args, **kwargs):
        raise ValueError("Simulated pipeline crash")
        
    monkeypatch.setattr("mkpp.cli.load_mechanism", mock_load_mechanism)
    
    # Create an actual temp environment file so the open(env_path) check passes
    env_file = tmp_path / "env.yaml"
    env_file.write_text("mpi: {gather_to_root: false}")
    
    # We must patch os.getcwd to trick sanitize_path into allowing tmp_path absolute paths
    import os
    monkeypatch.setattr(os, "getcwd", lambda: "/")
    
    with pytest.raises(SystemExit) as e:
        main(["compile", "mech.yaml", "--test-env", str(env_file), "--out", "build"])
        
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "FATAL ERROR: Simulated pipeline crash" in captured.err
    assert captured.out == "" # Ensure stdout is clean on crash

def test_cli_compile_strict_flag(capsys, monkeypatch, tmp_path):
    # Verify that the --strict flag is successfully parsed and passed down to validation
    env_file = tmp_path / "env.yaml"
    env_file.write_text("mpi: {gather_to_root: false}")
    mech_file = tmp_path / "mech.yaml"
    # Create an empty mechanism which lacks a description, triggering strict mode failure
    mech_file.write_text("species: [{name: O3}]\nreactions: []")
    
    import os
    monkeypatch.setattr(os, "getcwd", lambda: "/")
    
    with pytest.raises(SystemExit) as e:
        main(["compile", str(mech_file), "--test-env", str(env_file), "--out", "build", "--strict"])
        
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Strict mode requires a mechanism description" in captured.err
