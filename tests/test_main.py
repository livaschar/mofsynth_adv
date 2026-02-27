import pytest
import sys
from mofsynth_adv.__main__ import main

def test_main_execution_flow(monkeypatch, tmp_path, capsys):
    """Test the full flow: CLI -> Summary -> User Input 'Y' -> Run."""
    
    # 1. Setup a dummy directory so _transaction_summary doesn't crash
    d = tmp_path / "dummy_cifs"
    d.mkdir()
    
    # 2. Mock CLI arguments: [program_name, function, directory]
    monkeypatch.setattr(sys, "argv", ["mofsynth_adv", "exec", str(d)])
    
    # 3. Mock the 'input' prompt to automatically return 'Y'
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    
    # 4. Mock 'run_synthesis' so we don't actually start a heavy simulation
    # We just want to see if it was CALLED correctly
    import mofsynth_adv.__main__
    mock_run_called = []
    def mock_run(*args, **kwargs):
        mock_run_called.append(True)
    
    monkeypatch.setattr("mofsynth_adv.__main__.run_synthesis", mock_run)

    # 5. Run it!
    main()

    # 6. Assertions
    captured = capsys.readouterr()
    assert "Transaction Summary" in captured.out
    assert mock_run_called  # This proves the 'if inp.upper() == "Y"' logic worked