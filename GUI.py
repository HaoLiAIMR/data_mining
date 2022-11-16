import streamlit as st

import pandas as pd
import numpy as np
import re
import ast


def parameter(pH, v0, v1):
    v0_SHE = round(eval(v0) - pH * 0.059, 3)  # V = V0-pH*0.059  using the round to keep three numbers after the dot
    v1_SHE = round(eval(v1) - pH * 0.059, 3)

    V0 = -1.2  # Potential changes as the pH value changes,setting the origin potential for the begin potential
    V1 = 2.16  # Potential changes as the pH value changes,setting the origin potential for the end potential
    V_start = round(V0 - pH * 0.059, 3)  # V = V0-pH*0.059  using the round to keep three numbers after the dot
    V_end = round(V1 - pH * 0.059, 3)
    num = (V_end - V_start) / 0.01
    # pd.read_excel read the excel, the number indexes have many numbers after the dot, so replace the columns by the new numbers
    index_rename = []
    for intr in np.linspace(V_start, V_end, int(num + 1)):
        intr = round(intr, 3)
        index_rename.append(intr)
    # the number of potentials form V_start to V_end, the interbal is 0.01
    if v0_SHE in index_rename:
        v0_real = v0_SHE
    else:
        v0_real = np.array(index_rename)[np.array(index_rename) > v0_SHE][0]
    if v1_SHE in index_rename:
        v1_real = v1_SHE
    else:
        if v1 == v0:
            v1_real = v0_real
        else:
            v1_real = np.array(index_rename)[np.array(index_rename) < v1_SHE][-1]
    return v0_real, v1_real, index_rename


def read_database(path, index_rename):
    database = pd.read_excel(path, header=0, dtype=object)
    data_V = database.iloc[:, 3:]
    data_V.columns = index_rename
    return database, data_V


def Gpbx_entry_id_ion(i, v0_real, v1_real, database, data_V):
    materials = data_V.iloc[i]  # the ith materials
    material_id = database.iloc[i]['material_id']
    V_num_list = np.linspace(v0_real, v1_real, int(round((v1_real - v0_real) / 0.01, 3)) + 1)
    # according to the input v0 and v1, we can obtain the potentials in this range with the interval of 0.01V
    Gpbx_i = []
    entry_id_i = []
    species_i = []
    ion_num = []
    solid_num = []
    for j in range(0, len(V_num_list)):
        v = round(V_num_list[j], 3)
        str_all = materials[v]
        str_all_to_dict = ast.literal_eval(str_all)
        Gpbx = str_all_to_dict['Gpbx']
        entry_id = str_all_to_dict['entry_id']
        if 'ion' in str(entry_id):
            ion_num.append(1)
        else:
            solid_num.append(0)
        species = str_all_to_dict['species']
        Gpbx_i.append(Gpbx)
        entry_id_i.append(entry_id)
        species_i.append(species)
    Gpbx_i_max = max(Gpbx_i)
    return Gpbx_i_max, entry_id_i, species_i, ion_num, V_num_list, material_id


def stable_phase(V_num_list, species_i):
    rst = {}
    for jt in range(len(V_num_list)):
        key = species_i[jt]
        val = round(V_num_list[jt], 3)
        if key in rst.keys():
            rst[key].append(val)
        else:
            rst[key] = [val]

    rst_new = {}
    for key in rst.keys():
        rst_new[key] = str(rst[key][0]) + "-" + str(rst[key][-1]) + " V"
    phase = dict(stable_species_VS_SHE=str(rst_new))
    return phase

def main(folder_path, pH, v0, v1):

    v0_real, v1_real, index_rename = parameter(pH, v0, v1)
    path = folder_path + "pH="+str(pH)+".xlsx"
    #path = "D:/Work in Tohoku/筛选材料/rare_earthO/rare_earthO_ph="+str(ph)+".xlsx"

    database, data_V = read_database(path, index_rename)

    stable_materials = []
    for i in range(0, len(database)):  # len(database)
        # print(i)
        Gpbx_i_max, entry_id_i, species_i, ion_num, V_num_list, material_id = Gpbx_entry_id_ion(i, v0_real, v1_real, database, data_V)
        if Gpbx_i_max < 0.5:

            if material_id in str(entry_id_i):
                phase = stable_phase(V_num_list, species_i)
                stable_material = database.iloc[i][['material_id', 'icsd_ids', 'pretty_formula']]
                max_Gpbx_i_max = dict(max_Gpbx=Gpbx_i_max)
                stable = pd.concat([stable_material, pd.Series(max_Gpbx_i_max), pd.Series(phase)])
                stable_materials.append(stable)

            else:
                if 'ion' in str(entry_id_i):
                    if len(V_num_list) > 10:
                        if len(ion_num) <= 3:
                            phase = stable_phase(V_num_list, species_i)
                            stable_material = database.iloc[i][['material_id', 'icsd_ids', 'pretty_formula']]
                            max_Gpbx_i_max = dict(max_Gpbx=Gpbx_i_max)
                            stable = pd.concat([stable_material, pd.Series(max_Gpbx_i_max), pd.Series(phase)])
                            stable_materials.append(stable)

                    elif 1 < len(V_num_list) <= 10:
                        if len(ion_num) <= 1:
                            phase = stable_phase(V_num_list, species_i)
                            stable_material = database.iloc[i][['material_id', 'icsd_ids', 'pretty_formula']]
                            max_Gpbx_i_max = dict(max_Gpbx=Gpbx_i_max)
                            stable = pd.concat([stable_material, pd.Series(max_Gpbx_i_max), pd.Series(phase)])
                            stable_materials.append(stable)
                    else:
                        if len(ion_num) == 0:
                            phase = stable_phase(V_num_list, species_i)
                            stable_material = database.iloc[i][['material_id', 'icsd_ids', 'pretty_formula']]
                            max_Gpbx_i_max = dict(max_Gpbx=Gpbx_i_max)
                            stable = pd.concat([stable_material, pd.Series(max_Gpbx_i_max), pd.Series(phase)])
                            stable_materials.append(stable)
                else:
                    phase = stable_phase(V_num_list, species_i)
                    stable_material = database.iloc[i][['material_id', 'icsd_ids', 'pretty_formula']]
                    max_Gpbx_i_max = dict(max_Gpbx=Gpbx_i_max)
                    stable = pd.concat([stable_material, pd.Series(max_Gpbx_i_max), pd.Series(phase)])
                    stable_materials.append(stable)

        else:
            continue
    # print(pd.DataFrame(stable_materials))
    #pd.DataFrame(stable_materials).to_excel("rastable_materials.xlsx", index=None)

    return stable_materials

folder_path = './'

with st.sidebar:
    pH = st.text_input(
        "Please enter the pH value"
    )
    v0 = st.text_input(
        "Please enter the begin potential(the potential range (vs RHE) is -1.2 ~ 2.16)",
    )
    v1 = st.text_input(
        "Please enter the end potential(the potential range (vs RHE) is -1.2 ~ 2.16)",
    )
# pH = int(input("Please enter the pH value:  "))
# v0 = input("Please enter the begin potential(the potential range (vs RHE) is -1.2 ~ 2.16)  ")
# v1 = input("Please enter the end potential(the potential range (vs RHE) is -1.2 ~ 2.16)  ")

if (pH != '') & (v0 != '') & (v1 != ''):
    stable_materials = main(folder_path, int(pH), v0, v1)
    st.dataframe(stable_materials)