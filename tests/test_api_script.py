import sys
from pathlib import Path
from mofsynth_adv.core import MOF

def test_api():
    try:
        # Assuming there is a test.cif or similar in the test folder
        test_cif = Path("c:/Users/livas/Desktop/mofsynth_adv/tests/test_cifs/HKUST-1.cif")
        
        if not test_cif.exists():
            print(f"Test CIF not found at {test_cif}")
            return
            
        print(f"Testing MOF instantiation from {test_cif.name}...")
        mof = MOF.from_cif(str(test_cif))
        print(f"Success! MOF Name: {mof.name}")
        print(f"Supercell dimension check: {mof.create_supercell()}")
        
    except Exception as e:
        print(f"API Test Failed with Error: {e}")

if __name__ == "__main__":
    test_api()
