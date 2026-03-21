import sys
from ase.io import read, write

def get_calculator(name):
    # CUSTOM USERS: Add your preferred ASE calculator (e.g., UMA, eSEN) here.
    name = name.lower()
    if name == "xtb":
        try:
            from tblite.ase import TBLite
            return TBLite(method="GFN2-xTB")
        except ImportError:
            raise ImportError(
                "\n\n[TBLite NOT FOUND] Please ensure tblite is installed.\n"
                "You can install it via conda or pip if supported on your OS.\n")
    elif name == "mace_mp":
        try:
            from mace.calculators import mace_mp
            import torch
            device = "cpu"
            if torch.cuda.is_available():
                device = "cuda"
            return mace_mp(model="small", device=device)
        except ImportError:
            raise ImportError(
                "\n\n[MACE NOT FOUND] To use Machine Learning potentials, "
                "please install the optional dependencies:\n"
                "pip install mofsynth_adv[ml]\n")
    elif name == "mace_off":
        try:
            from mace.calculators import mace_off
            import torch
            device = "cpu"
            if torch.cuda.is_available():
                device = "cuda"
            return mace_off(model="small", device=device)
        except ImportError:
            raise ImportError(
                "\n\n[MACE NOT FOUND] To use Machine Learning potentials, "
                "please install the optional dependencies:\n"
                "pip install mofsynth_adv[ml]\n")
    else:
        print(f"Unknown calculator: {name}. Cannot proceed without a valid backend.")
        sys.exit(1)


def get_optimizer(name, atoms):
    name = name.lower()
    if name == "sella":
        from sella import Sella
        return Sella(atoms)
    elif name == "fire":
        from ase.optimize import FIRE
        return FIRE(atoms)
    elif name == "lbfgs":
        from ase.optimize import LBFGS
        return LBFGS(atoms)
    else:
        from ase.optimize import BFGS
        return BFGS(atoms)

def run_calculation(xyz_path, out_dir, calc_name, opt_name):
    atoms = read(xyz_path)
    atoms.calc = get_calculator(calc_name)

    try:
        # 1. Initial Energy
        initial_energy = atoms.get_potential_energy()
        
        # 2. Optimization
        dyn = get_optimizer(opt_name, atoms)
        # The convergence criterion is that the force on all individual atoms should be less than fmax
        dyn.run(fmax=0.05)
        
        # 3. Final Energy
        final_energy = atoms.get_potential_energy()
        
        # 4. Write Files
        write(f"{out_dir}/final.xyz", atoms)
        with open(f"{out_dir}/converged.out", "w") as f:
            f.write(f"Initial Energy: {initial_energy * 23.06:.6f} kcal/mol\n")
            f.write(f"Final Energy: {final_energy * 23.06:.6f} kcal/mol\n")
            f.write(f"Delta: {(final_energy - initial_energy) * 23.06:.6f} kcal/mol\n")
    except Exception as e:
            # initial_energy = final_energy = float('nan')
            log_file = f"{out_dir}" / 'not_converged.out'
            with open(log_file, "a") as f:
                f.write(f"Failed processing {xyz_path} | Error: {str(e)}")

if __name__ == "__main__":
    # Args: xyz_path, out_dir, calculator, opt_name
    run_calculation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])