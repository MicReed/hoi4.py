"""
extract info from parsed HOI4 json to csv
TODO: B
add requirements
"""

import json
import pandas as pd
import re
from typing import List, Optional


def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def extract_technology_info(data: pd.DataFrame, country_code: str) -> pd.DataFrame:
    """
    extract tech info
    """
    technologies = data['countries'][country_code]['technology']['technologies']
    tech_list = []
    for tech_name, tech_details in technologies.items():
        tech_details['technology'] = tech_name
        tech_details['country'] = country_code
        tech_list.append(tech_details)
    desired_order = ['country', 'technology', 'level', 'research_points', 'date']
    df = create_dataframe(tech_list, desired_order)
    return df


def rename_subdict():
    """
    Rename the sub_dict in the dictionary as a general approach.
    
    transforms the sub_dict's keys by prefixing the parent key (e.g., "id") to each of the sub_dict's keys.
    e.g. :
    
    Before renaming:
    {
        "id": {
            "id": "147",
            "type": "56"
        }
    }
    
    After renaming:
    {
        "id_id": "147",
        "id_type": "56"
    }
    TODO: C
    rename sub_dict
    """
    pass


# get the key names in the condition of multiple similar key names
def get_sim_key_names(data: dict, country_code: str, ger_pattern: re.Pattern) -> List[str]:
    """
    get the key names in the condition of multiple similar key names
    TODO: C
    add rename process
    """
    # rename_subdict()
    prod_keys = data['countries'][country_code]['production'].keys()
    key_names = []
    for key in prod_keys:
        if re.match(ger_pattern, key):
            key_names.append(key)
    return key_names


def extract_mil_lines(data: dict, country_code: str) -> pd.DataFrame:
    """
    extract mil lines information, return as pd
    TODO: C
    add equipment ID to match the equipment name and info
    """
    mil_pattern = re.compile('^military_lines.*')
    line_names = get_sim_key_names(data, country_code, mil_pattern)
    line_datas = []
    for line_name in line_names:
        line_data = data['countries'][country_code]['production'][line_name]
        line_data['line_name'] = line_name
        line_data['id_id'] = line_data['id']['id']
        line_data['id_type'] = line_data['id']['type']
        del line_data['id']
        line_datas.append(line_data)
    desired_order = ['id_type', 'id_id', 'line_name', 'active_factories', 'speed', 'factory_efficiencies', 'cost']
    df = create_dataframe(line_datas, desired_order)
    return df


def cal_stability(data: dict, country_code: str) -> float:
    """
    extract country stability, considering: party popularity
    TODO: C
    other stability mod
    """
    stability = data['countries'][country_code]['stability']
    ruling_party = data['countries'][country_code]['politics']['ruling_party']
    stability = float(stability)
    ruling_party_popularity = data['countries'][country_code]['politics']['parties'][ruling_party]['popularity']
    # cal others
    ruling_party_popularity = float(ruling_party_popularity) * 0.01 * 0.15
    stability = min(100.0, stability + ruling_party_popularity)
    return stability


def cal_export_bonus(data: dict, country_code: str) -> float:
    """
    calculate export bonus
    TODO: B
    move bonus data to game_settings
    """
    export_bonuses = {
        'free_trade': 0.15,
        'export_focus': 0.1,
        'limited_exports': 0.05,
    }
    ideas = data['countries'][country_code]['politics']['ideas']
    for export_type in export_bonuses.keys():
        if export_type in ideas:
            return export_bonuses[export_type]
    return 0


def reorder_pd_keys(df: pd.DataFrame, desired_order: Optional[List[str]] = None) -> pd.DataFrame:
    """
    reorder the keys of dataframe according to the desired order, put the not mentioned keys in the back
    """
    if desired_order:
        remaining_columns = [col for col in df.columns if col not in desired_order]
        if remaining_columns:
            df = df[desired_order + remaining_columns]
        else:
            df = df[desired_order]
    return df


def create_dataframe(tech_list: list, desired_order: Optional[List[str]] = None) -> pd.DataFrame:
    """
    create dataframe from list and reorder it
    """
    df = pd.DataFrame(tech_list)
    df = reorder_pd_keys(df, desired_order)
    return df


def add_basic_info_to_df(df: pd.DataFrame, country: str, stability: float, export_bonus: float, **kargs):
    """
    add basic information such as stability to df that ready to export as csv
    """
    df_len = len(df)
    df['country'] = [country] * df_len
    df['stability'] = [stability] * df_len
    df['export_bonus'] = [export_bonus] * df_len
    for key, val in kargs.items():
        df[key] = [val] * df_len
    desired_order = ['country', 'stability', 'export_bonus']
    df = reorder_pd_keys(df, desired_order)
    return df


def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")


if __name__ == "__main__":
    # print("Current working directory:", os.getcwd())

    # json_file_path = r'tests\GER_simple.json'
    # json_file_path = r'tests\ENG_36_02_01.json'
    # json_file_path = r'tests\GER_36_02_01.json'
    json_file_path = r'tests\GER_1936_02_01_0.json'

    # Load JSON data
    json_data = load_json(json_file_path)

    # base info
    game_difficulty = json_data['difficulty']
    country_stability = cal_stability(json_data, 'GER')
    country_export_bonus = cal_export_bonus(json_data, 'GER')

    # Extract technology information for Germany (GER)
    # ger_technologies = extract_technology_info(data, 'GER')
    # tech_df = extract_technology_info(data, 'GER')
    # tech_csv_path = r'tests\GER_technologies.csv'
    # save_to_csv(tech_df, tech_csv_path)

    mil_lines_df = extract_mil_lines(json_data, 'GER')
    mil_lines_df = add_basic_info_to_df(mil_lines_df, 'GER', country_stability, country_export_bonus, game_difficulty=game_difficulty)
    # mil_lines_df = extract_military_lines(json_data, 'ENG')
    mil_lines_csv_path = r'tests\GER_mil_lines.csv'
    # mil_lines_csv_path = r'tests\ENG_mil_lines.csv'
    save_to_csv(mil_lines_df, mil_lines_csv_path)
