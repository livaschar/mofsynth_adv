from dataclasses import dataclass
from pathlib import Path

@dataclass
class Linkers:
    r"""
    Class representing a single linker molecule extracted from a MOF.
    """
    
    def __init__(self, smiles_code: str, mof_name: str, opt_path=None):
        r"""
        Initialize a Linkers instance.
        
        Parameters
        ----------
        smiles_code : str
            The SMILES representation of the linker.
        mof_name : str
            The name of the MOF this linker was extracted from.
        opt_path : str or Path, optional
            Working directory for this linker. If provided, it will be created.
        """
        self.smiles_code = smiles_code
        self.mof_name = mof_name
        
        self.opt_path = Path(opt_path) if opt_path is not None else None
        if self.opt_path is not None:
            self.opt_path.mkdir(parents=True, exist_ok=True)
            
        self.opt_energy = 0
        self.sp_energy = 0
        self.opt_status = 'NA'

    def optimize(self, calc_choice='xtb', opt_choice='lbfgs', rerun=False, opt_path=None):
        r"""
        Submits the linker optimization to the Slurm queue.
        
        Parameters
        ----------
        calc_choice : str
            Calculator to use (e.g., 'xtb', 'mace_mp')
        opt_choice : str
            Optimizer to use (e.g., 'lbfgs', 'fire')
        rerun : bool
            Whether to rerun the optimization if it already exists.
        opt_path : str or Path, optional
            Override the optimization path for this specific run.
        """
        import sys
        import subprocess
        from pathlib import Path
        import mofsynth_adv

        working_dir = Path(opt_path) if opt_path else self.opt_path
        if not working_dir:
            raise ValueError("opt_path must be provided either during initialization or when calling optimize().")
        working_dir.mkdir(parents=True, exist_ok=True)

        xyz_path = working_dir / "linker.xyz"
        job_sh = working_dir / "submit_opt.sh"

        # 2. Find the worker script
        worker_path = Path(mofsynth_adv.__file__).parent / "modules" / "ase_worker.py"
        # 3. Find the Python interpreter
        python_exe = sys.executable

        # 1. Create or read the Slurm Script Template from the user's home directory
        mofsynth_dir = Path.home() / ".mofsynth"
        mofsynth_dir.mkdir(parents=True, exist_ok=True)
        template_path = mofsynth_dir / "slurm_template.sh"
        
        if not template_path.exists():
            default_template = (
                "#!/bin/bash\n"
                "#SBATCH --job-name={job_name}\n"
                "#SBATCH --output={out_dir}/slurm.log\n"
                "#SBATCH --error={out_dir}/slurm.err\n"
                "#SBATCH --ntasks=1\n"
                "#SBATCH --cpus-per-task=4\n"
                "#SBATCH --time=01:00:00\n"
                "\n"
                "# Run using the venv's python and the dynamically located worker\n"
                "{python_exe} {worker_path} {xyz_path} {out_dir} {calc_choice} {opt_choice}\n"
            )
            with open(template_path, "w") as f:
                f.write(default_template)
        
        with open(template_path, "r") as f:
            template_content = f.read()

        slurm_content = template_content.format(
            job_name=f"MOF_opt_{working_dir.name}",
            out_dir=working_dir,
            python_exe=python_exe,
            worker_path=worker_path,
            xyz_path=xyz_path,
            calc_choice=calc_choice,
            opt_choice=opt_choice
        )
    
        with open(job_sh, "w") as f:
            f.write(slurm_content)
        command = f"sbatch {job_sh}"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Job submitted for {working_dir.name}")
                return True, "Submitted"
            else:
                return False, f"Slurm Error: {result.stderr}"
        except Exception as e:
            return False, str(e)

    def check_optimization_status(self, opt_path=None):
        r"""
        Check the optimization status of this linker.
        
        Parameters
        ----------
        opt_path : str or Path, optional
            Override the directory to check for convergence.
            
        Returns
        -------
        str
            The status: 'converged', 'not_converged', or 'no_output_file'
        """
        working_dir = Path(opt_path) if opt_path else self.opt_path
        if not working_dir:
            return 'no_output_file'
            
        converged_out = working_dir / "converged.out"
        not_converged_out = working_dir / "not_converged.out"
        
        if converged_out.exists():
            self.opt_status = 'converged'
            with open(converged_out, 'r') as f:
                content = f.read()    
            for line in content.split('\n'):
                if "Final Energy" in line:
                    self.opt_energy = float(line.split()[2])
                elif "Initial Energy" in line:
                    self.sp_energy = float(line.split()[2])
        elif not_converged_out.exists():
            self.opt_status = 'not_converged'
        else:
            self.opt_status = 'no_output_file'
            
        return self.opt_status
