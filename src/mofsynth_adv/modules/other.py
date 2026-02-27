import shutil
import pickle
import os
import csv

def copy(path1, path2, file_1, file_2 = None):
    if file_2 is None:
        file_2 = file_1
    shutil.copy(os.path.join(path1, file_1), os.path.join(path2, file_2))
    return

def load_objects(root_path):
    id_smiles_dict = {}
    with open(root_path / 'cifs.pkl', 'rb') as file:
        cifs = pickle.load(file)
    with open(root_path / 'linkers.pkl', 'rb') as file:
        linkers = pickle.load(file)
    
    with open(root_path / 'smiles_id_dictionary.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            id_smiles_dict[line.split()[-1]] = line.split()[0]
    
    return cifs, linkers, id_smiles_dict

def write_csv_results(results_list, results_csv_path):
    headers = ["NAME", "ENERGY_(OPT-SP)_[au]", "ENERGY_(OPT-SP)_[kcal/mol]", "RMSD_[A]", "LINKER_(CODE)", "LINKER_(SMILES)", "Linker_SinglePointEnergy_[au]", "Linker_OptEnergy_[au]", "Opt_status"]
    
    with open(results_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for result_row in results_list:
            writer.writerow(result_row)