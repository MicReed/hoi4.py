import pandas as pd
import ast


def read_pd_file(file_path):
    df = pd.read_csv(file_path)
    return df


def read_pd_data(df: pd.DataFrame, tar_mil_line: str) -> dict:
    """
    read mil line info according to tar_mil_line name,
    get relevant info such as fac_eff, stability and exported as a dictionary
    """
    line_df = df.loc[df['line_name'] == tar_mil_line]
    if line_df.empty:
        print(f'No such line {tar_mil_line} in the data, program will exit.')
        exit()
    line_df_index = df.index[df['line_name'] == tar_mil_line].to_list()[0]

    stability = line_df['stability'].values[0]
    export_bonus = line_df['export_bonus'].values[0]
    prod_cost = line_df['cost'].values[0]
    eff_list = line_df['factory_efficiencies']
    eff_list = eff_list.apply(ast.literal_eval)[line_df_index]
    fac_num = line_df['active_factories'].values[0]
    fac_eff = eff_list[:fac_num]
    fac_eff = [float(i) * 0.01 for i in fac_eff]

    pd_dict = {
        'stability': stability,
        'export_bonus': export_bonus,
        'prod_cost': prod_cost,
        'fac_eff': fac_eff,
        'fac_num': fac_num}

    return pd_dict
