"""
basic settings params for the game
"""

import datetime


class GameSettings:
    """
    basic settings params for the game
    """
    # pe_cap_difficulty : production efficiency cap by difficulty
    prod_effi_cap = {
        "very_easy": 0.3,  # Civilian
        "easy": 0.2,  # Recruit
        "normal": 0.1,  # Regular
        "hard": -0.2,  # Veteran
        "very_hard": -0.3,  # Elite
    }
    start_date = '1936_02_01'
    start_date = datetime.datetime.strptime(start_date, '%Y_%m_%d')

# print(GameSettings.pe_cap_difficulty["Civilian"])
