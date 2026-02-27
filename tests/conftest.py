import pytest
from pathlib import Path
import os
import shutil
import sys
from unittest.mock import MagicMock

# Mock out external non-pip dependencies that fail during test collection
sys.modules['mofid'] = MagicMock()
sys.modules['mofid.run_mofid'] = MagicMock()

@pytest.fixture
def test_data_dir():
    """Returns the path to the test data directory."""
    return Path(__file__).parent / "data"

@pytest.fixture
def sample_cif(test_data_dir):
    """Returns the path to the sample CIF file."""
    cif_path = test_data_dir / "sample.cif"
    if not cif_path.exists():
        pytest.fail(f"Sample CIF not found at {cif_path}")
    return cif_path

@pytest.fixture
def temp_work_dir(tmp_path):
    """Creates a temporary working directory with a copy of the sample CIF."""
    # We want a directory structure that mimics what the code expects if needed
    # But for unit tests, usually just a clean dir is enough
    return tmp_path

@pytest.fixture
def synthesis_env(temp_work_dir, sample_cif):
    """Sets up a synthesis environment with the sample CIF file."""
    # Create the folder structure expected by run_synthesis if necessary
    # The code expects a directory with CIF files.
    cif_folder = temp_work_dir / "cif_folder"
    cif_folder.mkdir()
    shutil.copy(sample_cif, cif_folder / "sample.cif")
    return cif_folder
