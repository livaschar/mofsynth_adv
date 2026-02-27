import shutil
import pickle
import os
import openpyxl

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

def write_xlsx_results(results_list, results_xlsx_path):
    
    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Write headers
    headers = ["NAME", "ENERGY_(OPT-SP)_[au]", "ENERGY_(OPT-SP)_[kcal/mol]", "RMSD_[A]", "LINKER_(CODE)", "LINKER_(SMILES)", "Linker_SinglePointEnergy_[au]", "Linker_OptEnergy_[au]", "Opt_status"]
    sheet.append(headers)

    # Write results
    for result_row in results_list:
        sheet.append(result_row)

    # Save the workbook to the specified Excel file
    workbook.save(results_xlsx_path)