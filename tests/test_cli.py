import pytest
import os
from mofsynth_adv.__cli__ import _return_cli_parser, _transaction_summary

def test_parser_defaults():
    """Test that the parser sets default values correctly."""
    parser = _return_cli_parser()
    # Simulate: mofsynth_adv exec ./my_cifs
    args = parser.parse_args(['exec', './my_cifs'])
    
    assert args.function == 'exec'
    assert args.directory == './my_cifs'
    assert args.calc_choice == 'xtb'  # Default value
    assert args.opt_choice == 'lbfgs' # Default value
    assert args.supercell_limit is None

def test_transaction_summary_output(tmp_path, capsys):
    """Test the visual summary with a mock directory and captured output."""
    # 1. Setup: Create a fake directory with 2 dummy .cif files
    d = tmp_path / "cif_folder"
    d.mkdir()
    (d / "mof1.cif").write_text("dummy content")
    (d / "mof2.cif").write_text("dummy content")
    (d / "notes.txt").write_text("not a cif") # Should be ignored

    # 2. Mock the args object
    class MockArgs:
        directory = str(d)
        function = 'verify'
        calc_choice = 'mace'
        opt_choice = 'fire'
        time_limit = 20
        supercell_limit = 10.0

    # 3. Run the function
    _transaction_summary(MockArgs())

    # 4. Capture and check the printed text
    captured = capsys.readouterr()
    
    assert "Transaction Summary" in captured.out
    assert "Calculate for:" in captured.out
    assert "2" in captured.out  # Should count exactly 2 .cif files
    assert "mace - fire" in captured.out
    assert "10.0" in captured.out