import pytest
import sys
import os
# Ensure src is in path if not installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from mofsynth_adv.workflow import run_synthesis

def test_workflow_exec(synthesis_env):
    """
    Test the 'exec' function of the synthesis workflow.
    This test runs the full pipeline on a sample CIF.
    """
    # Check for optional dependencies
    try:
        import tblite
    except ImportError:
        pytest.skip("tblite not installed, skipping integration test requiring xTB")

    directory = str(synthesis_env)
    function = 'exec'
    calc_choice = 'xtb'
    opt_choice = 'lbfgs'
    supercell_limit = 5
    
    # Run synthesis
    # Note: run_synthesis might call sys.exit() on error, so we might want to capture that
    try:
        run_synthesis(directory, function, calc_choice, opt_choice, supercell_limit)
    except SystemExit as e:
        pytest.fail(f"run_synthesis exited with {e}")
    except Exception as e:
        pytest.fail(f"run_synthesis raised exception: {e}")

    # Check if results were generated
    # The code expects to write to ../Synth_folder relative to directory
    # synthesis_env is tmp/cif_folder
    # so we look in tmp/Synth_folder
    
    root_path = synthesis_env.parent
    synth_folder = root_path / "Synth_folder"
    
    assert synth_folder.exists()
    assert (synth_folder / "sample").exists() # It creates a folder for the MOF (sanitized name 'sample')
