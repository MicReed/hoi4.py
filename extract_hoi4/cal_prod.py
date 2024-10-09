import math
from extract_hoi4.game_settings import GameSettings
from extract_hoi4.tools import read_pd_file, read_pd_data


def cal_fac_output_mod(stability: float, export_bonus: float) -> float:
    """
    calculate the factory output modifier given the country's stability and export bonus.
    TODO: B: add more factories
    e.g. tech
    """
    stability_bonus = (stability - 0.5) * 0.4
    fac_output_mod = stability_bonus + export_bonus
    return fac_output_mod


def cal_cost(base_cost: float, cost_bonus: float) -> float:
    """
    Calculate the cost of a product given its cost bonus and base cost.
    TODO: B: manufacture related bonus
    """
    cost = base_cost * (1 - cost_bonus)
    return cost


def cal_mil_line_speed(fac_eff: list, stability, export_bonus, base_prod=4.5, deci_trunc=100):
    """
    Calculate the production speed(total production/day) of a mil_line given its efficiency, corresponding factories
    TODO: A: update line speed over time, replace for loop with numpy calculation
    """
    fac_output_mod = cal_fac_output_mod(stability, export_bonus)
    fac_prod = [math.floor(i * (1 + fac_output_mod) * base_prod * deci_trunc) / deci_trunc for i in fac_eff]
    line_speed = sum(fac_prod)
    return round(line_speed, 2)


def cal_line_output_predict(line_speed, prod_cost: float, prod_cost_bonus: float = 0) -> float:
    """
    predict the output of a production line given its speed and the prod cost
    TODO: C
    add showing mechanism for day, week, month, year
    """
    if prod_cost_bonus:
        prod_cost = cal_cost(prod_cost, prod_cost_bonus)
    output_predict = line_speed / prod_cost
    # cal unit
    return output_predict


def cal_line_output(line_speed: float, prod_cost: float, prod_cost_bonus: float = 0, days=1):  # noqa
    """
    TODO: A
    del no qa
    """
    start_date = GameSettings.start_date # noqa

    return


if __name__ == "__main__":
    csv_path = r'tests\GER_mil_lines.csv'
    country_code = 'GER'
    tar_mil_line = 'military_lines__2'

    data_df = read_pd_file(csv_path)
    # read mil line data from df
    mil_line_data = read_pd_data(data_df, tar_mil_line)
    country_stability = mil_line_data['stability']
    country_export_bonus = mil_line_data['export_bonus']
    line_prod_cost = mil_line_data['prod_cost']
    line_fac_eff = mil_line_data['fac_eff']
    line_fac_num = mil_line_data['fac_num']

    mil_line_speed = cal_mil_line_speed(line_fac_eff, line_fac_num, country_stability, country_export_bonus)
    print(f'mil_line_speed of {tar_mil_line} is:', mil_line_speed)
    line_output = cal_line_output_predict(mil_line_speed, line_prod_cost)
