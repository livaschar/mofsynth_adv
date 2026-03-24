import re
import os
import sys
import pickle
import time
from pathlib import Path
from datetime import datetime

from mofsynth_adv.core import MOF, Linkers
from mofsynth_adv.modules.other import (copy, load_objects, write_csv_results)


class SynthesizabilityWorkflow:
    r"""
    A High-Throughput Engine that orchestrates the synthesis evaluation of 
    multiple CIF files contained within a directory.
    """
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.synth_folder_path = self.root_path / "Synth_folder"
        self.linkers_path = self.synth_folder_path / "_Linkers_"
        self.results_csv_path = self.root_path / "synth_results.csv"

    def _log_time(self, start_time, end_time, function):
        """Writes start and end times into runtime.log."""
        filepath = self.root_path / "runtime.log"
        with open(filepath, "a") as f:
            f.write("--------------------------------------------------\n")
            f.write(f"Function: {function}\n")
            f.write(f"Start time: {start_time}\n")
            f.write(f"End time:   {end_time}\n")

    def run(self, directory: str, function: str, calc_choice: str, opt_choice: str, 
            time_limit: int, supercell_limit: int):
        
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_dir = Path(directory).resolve()

        if function == 'exec':
            self.execute(user_dir, calc_choice, opt_choice, time_limit, supercell_limit)
        elif function == 'verify':
            self.verify()
        elif function == 'report':
            self.report()
        else:
            print('Wrong function. Aborting...')
            sys.exit()
            
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log_time(start_time, end_time, function)

    def execute(self, user_dir: Path, calc_choice: str, opt_choice: str, time_limit: int, supercell_limit: int):
        print(f'  \033[1;32m\nSTART OF SYNTHESIZABILITY EVALUATION\033[m')
        
        self.synth_folder_path.mkdir(parents=True, exist_ok=True)
        self.linkers_path.mkdir(parents=True, exist_ok=True)

        cifs = []
        for cif in (item for item in user_dir.iterdir() if item.suffix == ".cif"):
            sanitized_name = re.sub(r'[^a-zA-Z0-9-_]', '_', cif.stem)
            cif.rename(user_dir / f"{sanitized_name}.cif")
            cifs.append(user_dir / f"{sanitized_name}.cif")
            
        if not cifs:
            print(f"\n\033[1;31m\n WARNING: No cif was found in: {user_dir}. Aborting session... \033[m")
            return False

        mof_instances = []
        linker_instances = []
        fault_parsing = []
        fault_fragment = []
        smiles_id_dict = {}
        unique_id = 0

        # Process each CIF
        for cif_path in cifs:
            print(f'\n - \033[1;34mMOF under study: {cif_path.stem}\033[m -')
            
            # New API
            try:
                mof = MOF.from_cif(str(cif_path))
            except ValueError:
                fault_parsing.append(cif_path.stem)
                continue
                
            try:
                smiles, xyz = mof.extract_linkers(time_limit=time_limit, supercell_limit=supercell_limit)
            except Exception:
                smiles, xyz = None, None
            
            if not smiles or not xyz:
                fault_fragment.append(mof.name)
                continue
                
            if smiles not in smiles_id_dict:
                unique_id += 1
                smiles_id_dict[smiles] = str(unique_id)
                
            mof.linker_smiles = smiles_id_dict[smiles]
            mof_instances.append(mof)
            
            # linker tracking
            opt_path = self.linkers_path / mof.linker_smiles / mof.name
            linker = Linkers(smiles_code=mof.linker_smiles, mof_name=mof.name, opt_path=opt_path)
            if xyz:
                linker.opt_path.mkdir(parents=True, exist_ok=True)
                with open(linker.opt_path / "linker.xyz", "w") as f:
                    f.write(xyz)
                    
            linker_instances.append(linker)

        # Opt
        for linker in linker_instances:
            print(f'\n - \033[1;34mLinker under optimization study: {linker.smiles_code}, of {linker.mof_name}\033[m -')
            linker.optimize(calc_choice=calc_choice, opt_choice=opt_choice, rerun=False)

        # Checkpoint
        with open(self.root_path / 'cifs.pkl', 'wb') as file:
            pickle.dump(mof_instances, file)
        with open(self.root_path / 'linkers.pkl', 'wb') as file:
            pickle.dump(linker_instances, file)

        if fault_fragment:
            with open(self.root_path / 'fault_fragmentation.txt', 'w') as f:
                for name in fault_fragment: f.write(f'{name}\n')
                
        if fault_parsing:
            with open(self.root_path / 'fault_parsing.txt', 'w') as f:
                for name in fault_parsing: f.write(f'{name}\n')
                
        with open(self.root_path / 'smiles_id_dictionary.txt', 'w') as f:
            for k, v in smiles_id_dict.items(): f.write(f'{k} : {v}\n')

        return mof_instances, linker_instances

    def verify(self):
        cifs, linkers, _ = load_objects(self.root_path)
        converged = []
        not_converged = []
        running = []
        
        for linker in linkers:
            status = linker.check_optimization_status()
            if status == 'converged':
                converged.append(linker)
            elif status == 'not_converged':
                not_converged.append(linker)
            else:
                running.append(linker)    
        with open(self.root_path / 'converged.txt', 'w') as f:
            for l in converged: f.write(f"{l.smiles_code} {l.mof_name}\n")
        with open(self.root_path / 'not_converged.txt', 'w') as f:
            for l in not_converged: f.write(f"{l.smiles_code} {l.mof_name}\n")
        with open(self.root_path / 'running.txt', 'w') as f:
            for l in running: f.write(f"{l.smiles_code} {l.mof_name}\n")
            
        return converged, not_converged, running

    def report(self):
        cifs, _, id_smiles_dict = load_objects(self.root_path)
        converged, _, _ = self.verify()
        
        # Determine best energies
        best_opt = {}
        for l in converged:
            if l.smiles_code not in best_opt or l.opt_energy < best_opt[l.smiles_code][0]:
                best_opt[l.smiles_code] = [l.opt_energy, l.opt_path]

        results = []
        for mof in cifs:
            linker = next((L for L in converged if L.smiles_code == mof.linker_smiles and L.mof_name == mof.name), None)
            if not linker:
                mof.opt_status = 'not_converged'
                mof.de = 0
                mof.rmsd = 0
            else:
                mof.opt_status = 'converged'
                best_energy = best_opt[mof.linker_smiles][0]
                best_path = best_opt[mof.linker_smiles][1]
                
                mof.de = float(best_energy) - float(linker.sp_energy)
                
                sp_file = linker.opt_path / "linker.xyz" 
                opt_file = best_path / "final.xyz" 
                
                if sp_file.exists() and opt_file.exists():
                    mof.rmsd = MOF.calculate_rmsd(opt_file, sp_file)
                else:
                    mof.rmsd = 10000.0

            row = [mof.name, mof.de/0.0016, mof.de, mof.rmsd, 
                   int(mof.linker_smiles) if str(mof.linker_smiles).isdigit() else mof.linker_smiles, 
                   id_smiles_dict.get(mof.linker_smiles, ''), 
                   linker.sp_energy if linker else 0, 
                   linker.opt_energy if linker else 0, 
                   mof.opt_status]
            results.append(row)

        write_csv_results(results, self.results_csv_path)
        return self.results_csv_path

def run_synthesis(directory, function, calc_choice, opt_choice, time_limit, supercell_limit):
    engine = SynthesizabilityWorkflow(root_path=Path(directory).parent)
    engine.run(directory, function, calc_choice, opt_choice, time_limit, supercell_limit)
