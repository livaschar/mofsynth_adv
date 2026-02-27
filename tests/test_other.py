import pytest
import os
import pickle
import csv
from mofsynth_adv.modules.other import copy, load_objects, write_csv_results

def test_copy(tmp_path):
    # Create source and destination directories
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    
    # Create a dummy file
    test_file = src / "test.txt"
    test_file.write_text("hello world")
    
    # Test case 1: Copy with same name
    copy(str(src), str(dst), "test.txt")
    assert (dst / "test.txt").exists()
    
    # Test case 2: Copy with new name
    copy(str(src), str(dst), "test.txt", "new_name.txt")
    assert (dst / "new_name.txt").exists()
    assert (dst / "new_name.txt").read_text() == "hello world"

def test_load_objects(tmp_path):
    # 1. Setup mock pickle files
    cifs_data = {"mof1": "data"}
    linkers_data = ["linker1", "linker2"]
    
    with open(tmp_path / 'cifs.pkl', 'wb') as f:
        pickle.dump(cifs_data, f)
    with open(tmp_path / 'linkers.pkl', 'wb') as f:
        pickle.dump(linkers_data, f)
        
    # 2. Setup mock text dictionary (SMILES ID)
    # Expected format: SMILES ID (split index 0 and -1)
    with open(tmp_path / 'smiles_id_dictionary.txt', 'w') as f:
        f.write("C1=CC=CC=C1 BENZ01\n")
        f.write("CO C_METH02\n")

    # 3. Run the function
    cifs, linkers, id_smiles_dict = load_objects(tmp_path)
    
    # 4. Assertions
    assert cifs == cifs_data
    assert linkers == linkers_data
    assert id_smiles_dict["BENZ01"] == "C1=CC=CC=C1"
    assert id_smiles_dict["C_METH02"] == "CO"

def test_write_csv_results(tmp_path):
    file_path = tmp_path / "results.csv"
    dummy_results = [
        ["MOF_1", -100.1, -62810.0, 0.05, "L1", "C1...", -50.0, -50.1, "Success"],
        ["MOF_2", -200.2, -125620.0, 0.08, "L2", "C2...", -100.0, -100.2, "Failed"]
    ]
    
    # Run the writer
    write_csv_results(dummy_results, str(file_path))
    
    # Verify the file exists
    assert file_path.exists()
    
    # Load it back to check content
    with open(file_path, newline='') as f:
        reader = list(csv.reader(f))
        
        # Check headers
        assert reader[0][0] == "NAME"
        # Check first row of data
        assert reader[1][0] == "MOF_1"
        assert reader[1][8] == "Success"