from pathlib import Path
from mofsynth_adv import SynthesizabilityWorkflow

def run_high_throughput_batch(cif_directory: str):
    input_dir = Path(cif_directory).resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Please provide a valid directory containing CIF files. {input_dir} is invalid.")
        return

    # Initialize the Workflow engine
    # create an output folder named 'Synth_folder' at the current working directory
    root_workspace = Path.cwd()
    workflow = SynthesizabilityWorkflow(root_path=root_workspace)
    
    print(f"--- Starting High-Throughput Job on: {input_dir} ---")
    
    # Execute Fragmentation & Quantum Optimizations 
    # This automatically processes all .cif files inside `cif_directory`
    # It identifies unique linkers and avoids computing duplicate fragments across different MOFs
    workflow.execute(
        user_dir=input_dir, 
        calc_choice="xtb",   # Try 'mace' if you have Machine Learning Potentials installed
        opt_choice="lbfgs", 
        time_limit=30,      
        supercell_limit=None # Optional spatial limit for supercell size bounds
    )
    
    # Verify statuses (Wait for asynchronous optimizations to finish)
    import time
    print("\n--- Waiting for Optimizations to Complete ---")
    print("This may take a while depending on the calculator and cluster availability.")
    
    while True:
        converged, not_converged, running = workflow.verify()
        
        if not running:
            # All jobs have either converged or permanently failed
            break
            
        print(f"Status update: {len(running)} jobs still running. {len(converged)} converged, {len(not_converged)} failed. Waiting 10 seconds...")
        time.sleep(10)
        
    print(f"\nFinal Result:")
    print(f"Successfully Converged Linkers: {len(converged)}")
    print(f"Failed to Converge: {len(not_converged)}")
    
    # Generate final report (synth_results.csv)
    print("\n--- Generating Report ---")
    results_path = workflow.report()
    print(f"Job Complete! Final summary written to: {results_path}")

if __name__ == "__main__":
    # Provide the path to a folder containing multiple .cif files
    sample_dir = "path/to/your/cif_folder"
    
    if Path(sample_dir).exists():
        run_high_throughput_batch(sample_dir)
    else:
        print(f"Please create a folder named '{sample_dir}' and populate it with .cif files.")
