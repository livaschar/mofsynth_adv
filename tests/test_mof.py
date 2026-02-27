import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from mofsynth_adv.core import MOF
from pymatgen.core import IStructure

def test_mof_initialization():
    """Tests if __init__ sets up attributes correctly."""
    mock_struct = MagicMock(spec=IStructure)
    mof = MOF("TestMOF", mock_struct)
    
    assert mof.name == "TestMOF"
    assert mof.structure == mock_struct
    assert mof.linker_smiles == ""
    assert mof.de == 0.0
    assert mof.rmsd == 0.0

@patch('mofsynth_adv.modules.mof.IStructure')
def test_from_cif(mock_istructure, tmp_path):
    """Tests creating a MOF from a CIF file."""
    cif_file = tmp_path / "test.cif"
    cif_file.write_text("data_test")
    
    mock_struct = MagicMock(spec=IStructure)
    mock_istructure.from_file.return_value = mock_struct
    
    mof = MOF.from_cif(str(cif_file))
    
    assert mof.name == "test"
    assert mof.structure == mock_struct
    from unittest.mock import ANY
    mock_istructure.from_file.assert_called_once_with(ANY)

def test_create_supercell():
    """Tests supercell creation by mocking Pymatgen calls."""
    mock_struct = MagicMock(spec=IStructure)
    mock_struct.lattice.abc = [10, 10, 10]
    
    # Mocking the multiplication (structure * 2)
    super_struct = MagicMock(spec=IStructure)
    mock_struct.__mul__.return_value = super_struct 
    
    mof = MOF("SuperMOF", mock_struct)
    new_struct = mof.create_supercell(limit=15)
    
    # 10 is < 15, so scaling factor is math.ceil(15/10) = 2
    mock_struct.__mul__.assert_called_once_with(2)
    assert new_struct == super_struct

@patch('mofsynth_adv.modules.mof.CifWriter')
@patch('mofsynth_adv.modules.mof.subprocess.run')
@patch('mofsynth_adv.modules.mof.cif2mofid')
def test_extract_linkers(mock_cif2mofid, mock_subprocess, mock_cifwriter):
    """Tests linker extraction and parsing SMILES."""
    mock_struct = MagicMock(spec=IStructure)
    mof = MOF("ExtractMOF", mock_struct)
    
    # Mock cif2mofid to succeed
    def mock_cif2mofid_call(*args, **kwargs):
        return True, "Success"
    mock_cif2mofid.side_effect = mock_cif2mofid_call
    
    # Mock subprocess (obabel) to succeed
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_subprocess.return_value = mock_result
    
    # Mock file creation expected by extract_linkers
    with patch('builtins.open') as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = "C1=CC=CC=C1\tlinker\n"
        mock_file.readlines.return_value = ["C1=CC=CC=C1\tlinker\n"]
        mock_open.return_value.__enter__.return_value = mock_file
        
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat_res = MagicMock()
            mock_stat_res.st_size = 1000
            mock_stat.return_value = mock_stat_res
            with patch('pathlib.Path.exists') as mock_exists:
                mock_exists.return_value = True
                
                smiles, xyz = mof.extract_linkers()
                assert smiles == "C1=CC=CC=C1"
                assert xyz == "C1=CC=CC=C1\tlinker\n"
    
def test_calculate_rmsd(tmp_path):
    """Tests the RMSD calculation wrapper."""
    file1 = tmp_path / "1.xyz"
    file2 = tmp_path / "2.xyz"
    file1.write_text("dummy")
    file2.write_text("dummy")
    
    with patch('mofsynth_adv.modules.mof.subprocess.run') as mock_subproc:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "1.234"
        mock_subproc.return_value = mock_result
        
        rmsd = MOF.calculate_rmsd(file1, file2)
        assert rmsd == 1.234