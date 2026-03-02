from dataclasses import dataclass
import subprocess
from pathlib import Path
from pymatgen.io.cif import CifWriter
from pymatgen.core.structure import IStructure
import signal
try:
    from mofid.run_mofid import cif2mofid
except ImportError:
    raise ModuleNotFoundError(
        "Please install the mofid module manually. "
        "See https://mofsynth-adv.readthedocs.io/en/latest/mofid_help.html for help"
    )

import tempfile
import shutil

class MOF:
    r"""
    Class representing a Metal-Organic Framework (MOF) molecule in memory.
    """
    
    def __init__(self, name: str, structure: IStructure):
        r"""
        Initialize a new MOF instance.
        
        Parameters
        ----------
        name : str
            The name of the MOF instance.
        structure : pymatgen.core.structure.IStructure
            The internal pymatgen representation of the MOF structure.
        """
        self.name = name
        self.structure = structure
        self.linker_smiles = ''
        self.de = 0
        self.rmsd = 0

    @classmethod
    def from_cif(cls, cif_path: str):
        r"""
        Load a MOF from a CIF file.
        
        Parameters
        ----------
        cif_path : str
            Path to the .cif file.
            
        Returns
        -------
        MOF
            A new MOF instance holding the generated pymatgen structure.
        """
        path = Path(cif_path)
        if not path.exists():
            raise FileNotFoundError(f"CIF file not found: {cif_path}")
            
        name = path.stem
        try:
            structure = IStructure.from_file(path)
            return cls(name, structure)
        except Exception as e:
            raise ValueError(f"'{name}' could not be parsed by Pymatgen. Error: {e}")

    def create_supercell(self, limit=None):
        r"""
        Create a supercell for the MOF instance safely in memory.

        Parameters
        ----------
        limit : int, optional
            The dimensional limit to enforce supercell creation.
            
        Returns
        -------
        IStructure
            Returns a internal `pymatgen` structure object representing the Supercell
        """
        if limit is not None and str(limit) != 'None' and all(cell_length > int(limit) for cell_length in self.structure.lattice.abc):
            return self.structure
        else:
            return self.structure * 2

    def extract_linkers(self, time_limit: int = 20, supercell_limit=None):
        r"""
        Extract the linkers from the MOF structure using the mofid library.
        Because mofid fundamentally requires file I/O, this function wraps the required
        steps in a temporary directory automatically.
        
        Returns
        -------
        tuple
            A tuple containing (smiles_code, xyz_content_string), or (None, None) if it failed.
        """
        class TimeoutException(Exception): pass
        def handler(signum, frame): raise TimeoutException()
        
        smiles_result = None
        xyz_result = None
        
        # We need a temp directory because `cif2mofid` strictly reads/writes paths
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            temp_cif = temp_path / f"{self.name}.cif"
            out_folder = temp_path / "Output"
            
            w = CifWriter(self.create_supercell(limit=supercell_limit))
            w.write_file(temp_cif)
            
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(int(time_limit))
            except AttributeError:
                pass # Windows fallback: no hard timeout applied via signal
            
            try:
                cif2mofid(temp_cif, output_path=out_folder)
                
                linker_cif = out_folder / "MetalOxo" / "linkers.cif"
                if linker_cif.exists() and linker_cif.stat().st_size >= 550:
                    
                    # Convert CIF to XYZ and SMILES using Obabel locally
                    linker_xyz = temp_path / "linker.xyz"
                    linker_smi = temp_path / "linker.smi"
                    
                    subprocess.run(["obabel", "-icif", linker_cif, "-oxyz", "-O", linker_xyz, "-r"], 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                   
                    subprocess.run(["obabel", linker_xyz, "-xc", "-O", linker_smi], 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                   
                    if linker_smi.exists() and linker_smi.stat().st_size > 9:
                        with open(linker_smi) as f:
                            lines = f.readlines()
                        smiles_result = str(lines[0].split()[0])
                    
                    if linker_xyz.exists():
                        with open(linker_xyz) as f:
                            xyz_result = f.read()
            except TimeoutException:
                pass
            except Exception:
                pass
            finally:
                try:
                    signal.alarm(0)
                except AttributeError:
                    pass
                
        return smiles_result, xyz_result

    @staticmethod
    def calculate_rmsd(opt_file, sp_file, reorder=False):
        r"""
        Calculate the RMSD between the optimized structure and the original single point.
        """
        import tempfile
        import shutil
        import subprocess

        rmsd_vals = []
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            sp_copy = temp_path / "sp.xyz"
            opt_copy = temp_path / "opt.xyz"
            sp_mod = temp_path / "sp_mod.xyz"
            sp_mod_txt = temp_path / "sp_mod.txt"
            
            shutil.copy(sp_file, sp_copy)
            shutil.copy(opt_file, opt_copy)

            # Dictionary mapping atomic numbers
            atomic_symbols = {
                0: 'X', 1: 'H', 2: 'He', 3: 'Li', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 
                15: 'P', 16: 'S', 17: 'Cl', 35: 'Br', 53: 'I'
            }
            
            try:
                if not reorder:
                    cmd = ["calculate_rmsd", "-p", str(opt_copy), str(sp_copy)]
                    with open(sp_mod_txt, "w") as out:
                        subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT)
                else:
                    cmd = ["calculate_rmsd", "-p", "--reorder", str(opt_copy), str(sp_copy)]
                    with open(sp_mod_txt, "w") as out:
                        subprocess.run(cmd, stdout=out, stderr=subprocess.DEVNULL)
                        
                data = []
                if sp_mod_txt.exists():
                    with open(sp_mod_txt, 'r') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if i < 2 or not line.split(): continue
                            parts = line.split()
                            try:
                                symbol = atomic_symbols.get(int(parts[0]), 'X')
                                coords = [float(c) for c in parts[1:4]]
                                data.append((symbol, coords))
                            except ValueError:
                                if not reorder:
                                    return MOF.calculate_rmsd(opt_file, sp_file, reorder=True)
                                return 10000.0

                    with open(sp_mod, 'w') as f:
                        f.write(f"{len(data)}\n\n")
                        for sym, coords in data:
                            f.write(f"{sym} {coords[0]:.6f} {coords[1]:.6f} {coords[2]:.6f}\n")
                            
                for run_file in [sp_copy, sp_mod]:
                    if run_file.exists():
                        cmd1 = f"calculate_rmsd -e {opt_copy} {run_file}"
                        cmd2 = f"calculate_rmsd -e --reorder-method hungarian {opt_copy} {run_file}"
                        cmd3 = f"calculate_rmsd -e --reorder-method distance {opt_copy} {run_file}"
                        
                        r1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
                        r2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
                        r3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True)
                        
                        for r in [r1, r2, r3]:
                            try:
                                rmsd_vals.append(float(r.stdout.strip()))
                            except ValueError:
                                pass
            except Exception:
                return 10000.0
                
        return min(rmsd_vals) if rmsd_vals else 10000.0

    def evaluate_synthesizability(self, calc_choice='xtb', opt_choice='lbfgs', time_limit: int = 30, supercell_limit=None):
        r"""
        A high-level wrapper to fully evaluate the synthesizability of this MOF instance.
        Extracts linkers, submits optimization jobs, waits for convergence, 
        and calculates the final energy difference (DE) and structural deviation (RMSD).
        
        Parameters
        ----------
        calc_choice : str
            Calculator to use (e.g., 'xtb', 'mace_mp')
        opt_choice : str
            Optimizer to use (e.g., 'lbfgs', 'fire')
        time_limit : int
            Time limit for linker extraction via mofid.
        supercell_limit : float or None
            Size limit to consider for supercell expansion during fragmentation.
            
        Returns
        -------
        bool
            True if evaluation succeeded and converged, False otherwise.
        """
        import time
        from mofsynth_adv.modules.linkers import Linkers
        
        print(f"--- Evaluating {self.name} ---")
        smiles, xyz = self.extract_linkers(time_limit=time_limit, supercell_limit=supercell_limit)
        
        if not smiles or not xyz:
            print(f"Failed to extract linker for {self.name}.")
            self.opt_status = 'not_converged'
            return False
            
        self.linker_smiles = smiles
        
        # Determine paths
        opt_path = Path("Synth_evaluations") / "single" / self.linker_smiles / self.name
        opt_path.mkdir(parents=True, exist_ok=True)
        
        # Write geometry
        with open(opt_path / "linker.xyz", "w") as f:
            f.write(xyz)
            
        linker = Linkers(smiles_code=smiles, mof_name=self.name, opt_path=opt_path)
        
        success, message = linker.optimize(calc_choice=calc_choice, opt_choice=opt_choice)
        if not success:
            print(f"Optimization submission failed: {message}")
            self.opt_status = 'not_converged'
            return False
            
        print("Waiting for optimization to complete...")
        while True:
            status = linker.check_optimization_status()
            if status != "no_output_file":
                break
            time.sleep(5)
            
        if status == "converged":
            self.opt_status = "converged"
            self.de = linker.opt_energy - linker.sp_energy
            
            # RMSD evaluation
            sp_file = linker.opt_path / "linker.xyz" 
            opt_file = linker.opt_path / "final.xyz" 
            if sp_file.exists() and opt_file.exists():
                self.rmsd = MOF.calculate_rmsd(opt_file, sp_file)
            else:
                self.rmsd = 10000.0
            return True
        else:
            self.opt_status = status
            self.de = 0.0
            self.rmsd = 10000.0
            return False

