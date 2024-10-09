from extract_hoi4.game_settings import GameSettings
from extract_hoi4.tools import read_pd_file, read_pd_data
import datetime


def prod_cap(difficulty: str) -> float:
    """
    calculate the production efficiency cap by difficulty, etc
    TODO: B: cap increase factor
    cap increased by industry technology, research, and national focuses.
    - add cap modifiers
    
    """
    prod_effi_cap = (GameSettings.prod_effi_cap[difficulty])
    print(prod_effi_cap)
    return prod_effi_cap


def prod_effi_grow(prod_effi_cap: float, prod_effi: float) -> float:
    """
    calculate production efficiency growth per day
    TODO: D
    the growth rate do not match the game data exactly, but close enough for now
    """
    growth = 0.001 * prod_effi_cap ** 2 / prod_effi
    return growth


def time_flow(prod_effi_cap: float, prod_effi: float, start_date='1936_02_01', days=1) -> float:
    """
    calculate the production efficiency over time
    print the target date
    TODO: C
    return target_date
    add unit test
    """
    c_day = datetime.datetime.strptime(start_date, '%Y_%m_%d')
    for i in range(days):
        growth = prod_effi_grow(prod_effi_cap, prod_effi)
        prod_effi = prod_effi + growth
        prod_effi = min(prod_effi, prod_effi_cap)

        c_day += datetime.timedelta(days=1)
        # print(f"Day {c_day.strftime('%Y_%m_%d')}")
        # print(f"prod_growth: {growth * 100:.5f}%")
        # print(f"Production Efficiency: {prod_effi * 100:.5f}%")
    # print(f"Day {c_day.strftime('%Y_%m_%d')}")
    # print(f"prod_growth: {growth * 100:.5f}%")
    # print(f"Production Efficiency: {prod_effi * 100:.5f}%")
    return prod_effi


if __name__ == '__main__':
    game_difficulty = 'very_hard'
    prod_cap(game_difficulty)
    csv_path = r'tests\GER_mil_lines.csv'
    country_code = 'GER'
    tar_mil_line = 'military_lines'
    data_df = read_pd_file(csv_path)
    mil_line_data = read_pd_data(data_df, tar_mil_line)
    fac_eff = mil_line_data['fac_eff']
    # print(fac_eff)
    game_start_date = '1936_02_01'

    effi_growth = time_flow(0.2, 0.1113699, start_date=game_start_date, days=60)
