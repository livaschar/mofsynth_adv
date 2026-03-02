# MOFSynth-Advanced

<h1 align="center">
  <!-- <img alt="Logo" src="https://github.com/livaschar/mofsynth_adv/blob/main/docs/source/images/synth_logo_v3_black.png" style="width: 500px;"/> -->
  <!-- <img alt="Logo" src="https://github.com/livaschar/mofsynth_adv/blob/main/docs/source/images/synth_image_v3.png" style="width: 500px;"/> -->
</h1>

<h4 align="center">

[![Requires Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-g?logo=python&logoColor=blue&label=Python&labelColor=black)](https://www.python.org/downloads/)
[![Read the Docs](https://img.shields.io/badge/latest-b?logo=readthedocs&logoColor=blue&label=Read%20the%20Docs&labelColor=black)](https://mofsynth-adv.readthedocs.io)
[![PyPI](https://img.shields.io/badge/PyPI%20-%20v%202.0.0%20-b?style=flat&logo=pypi&logoColor=blue&logoSize=auto&label=PyPI&labelColor=black)](https://pypi.org/project/mofsynth_adv/)
[![Licensed under GPL-3.0-only](https://img.shields.io/badge/GPL--3.0--only-gold?label=License&labelColor=black)](https://spdx.org/licenses/GPL-3.0-only.html)  

[![Online App](https://img.shields.io/badge/🔥%20MOFSYNTH%20Online-Try%20Now!-red?style=for-the-badge&labelColor=black)](https://mofsynth.website)  

</h4>

## 🔔 Release Note

We are excited to announce the release of MOFSynth-ADV, a significant leap forward in our commitment to speed, accessibility, and scientific reproducibility.

This new version is fully powered by open-source software, eliminating dependencies on proprietary packages and streamlining deployment across systems.

- **Multiple Calculators**: Seamlessly switch between xTB and MACE Machine Learning Potentials (`mace_mp`, `mace_off`)for rapid energy calculations.

- **Choice of Optimizers**: Select from a range of leading geometry optimizers including LBFGS, FIRE, BFGS, and Sella.

- **Global Config**: Set up your SLURM templates once with our new `~/.mofsynth/slurm_template.sh` approach and run anywhere.

- **Open Science Ready**: All dependencies are now open source, making MOFSynth-ADV fully transparent and reproducible.

✅ Why Upgrade?
Whether you're screening thousands of MOFs or performing high-throughput synth-likelihood predictions, MOFSynth delivers the performance and flexibility modern computational chemists demand.

Open source, faster, and ready for your next breakthrough.

## What is MOFSynth?
MOFSynth is a Python package for **MOF synthesizability evaluation**, with
emphasis on reticular chemistry.

In materials science, especially in the synthesis of metal-organic frameworks (MOFs),
a significant portion of time and effort is spent on the experimental process of synthesizing
and evaluating the viability of MOFs.

MOFSynth aims to provide a simple and efficient interface for evaluating
the synthesizability of metal-organic frameworks (MOFs) in an experiment-ready format,
minimizing the time and labor traditionally required for these experimental preprocessing steps.
This allows researchers to focus more on innovative synthesis and experimental validation
rather than on preparatory tasks.

## ⚙️  Installation

Because MOFSynth-ADV relies on computational chemistry tools that require compiled Fortran and C libraries (like `tblite`), **it is strongly recommended to use Conda** to manage your environment. Using a standard Python `venv` with pure `pip` may result in missing Fortran runtime errors.

### Method 1: Using environment.yml (Recommended)

If you are installing from the source repository, we provide an environment file that perfectly configures all complex dependencies.

```sh
# Clone the repository
git clone https://github.com/livaschar/mofsynth_adv.git
cd mofsynth_adv

# Create the environment and install all dependencies
conda env create -f environment.yml

# Activate the environment
conda activate mofsynth_adv_env
```

### Method 2: Manual Installation via Conda + Pip

If you are installing directly from PyPI, please ensure you install tblite via conda-forge before running pip.

```sh
# 1. Create and activate a new conda environment
conda create -n mmofsynth_adv_env python=3.13
conda activate mofsynth_adv_env

# 2. Install tblite via conda-forge to ensure Fortran libraries are linked
conda install -c conda-forge tblite tblite-python

# 3. Install MOFSynth-ADV and the rest of the dependencies
pip install mofsynth_adv
```

### Requires

To run MOFSynth-ADV, the following modules and tools must be present in your system:

1. [**mofid**](https://github.com/snurr-group/mofid): A Python library for MOF identification and characterization.

## 💻 Browser-Based MOFSynth

Easy to use [Web version](https://mofsynth.website) of the tool.

## 📖 Usage example

Check the [tutorial](https://mofsynth-adv.readthedocs.io/en/latest/tutorial.html).

Also check the [examples](https://github.com/livaschar/mofsynth_adv/tree/main/examples) folder for ready to use python scripts.

## :warning: Problems?

You can start by [opening an issue](https://github.com/livaschar/mofsynth_adv/issues) or communicate via [email](mailto:chemp1167@edu.chemistry.uoc.gr).

## 📰 Citing MOFSynth

Please consider citing [this publication](https://pubs.acs.org/doi/full/10.1021/acs.jcim.4c01298) or use the following BibTex.

<details>
<summary>Show BibTex entry</summary>

```bibtex
@article{doi:10.1021/acs.jcim.4c01298,
  author = {Livas, Charalampos G. and Trikalitis, Pantelis N. and Froudakis, George E.},
  title = {MOFSynth: A Computational Tool toward Synthetic Likelihood Predictions of MOFs},
  journal = {Journal of Chemical Information and Modeling},
  volume = {64},
  number = {21},
  pages = {8193-8200},
  year = {2024},
  doi = {10.1021/acs.jcim.4c01298},
  note ={PMID: 39481084},
  URL = {https://doi.org/10.1021/acs.jcim.4c01298},
  eprint = {https://doi.org/10.1021/acs.jcim.4c01298}
  }
```

</details>

## 📑 License

MOFSynth-ADV is released under the [GNU General Public License v3.0 only](https://spdx.org/licenses/GPL-3.0-only.html).
















