from mofsynth_adv import MOF

# 1. Load the MOF directly from the CIF file
cif_path = "tests/data/sample.cif" 

try:
    print(f"Loading {cif_path}...")
    mof = MOF.from_cif(cif_path)
    
    # 2. Evaluate synthesizability in a single command!
    # This automatically extracts linkers, builds the SLURM paths, 
    # runs the optimization calculator, and calculates DE and RMSD.
    success = mof.evaluate_synthesizability(calc_choice="xtb", opt_choice="lbfgs")
    
    # 3. View the results
    print("\n--- Final Results ---")
    if success:
        print(f"Convergence Status: {mof.opt_status}")
        print(f"Linker SMILES:      {mof.linker_smiles}")
        print(f"Delta E (DE):       {mof.de:.4f} eV")
        print(f"RMSD:               {mof.rmsd:.4f} Å")
    else:
        print(f"Evaluation failed. Status: {mof.opt_status}")

except Exception as e:
    print(f"An error occurred: {e}")
