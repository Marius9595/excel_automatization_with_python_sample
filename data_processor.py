from typing import Tuple
import pandas as pd
from pandas import DataFrame


def get_data_of_player_by_position() -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Tuple(strikers, midfielders, defenders, goalkeapers)
    """
    data = _merge_data_for_players()
    return (_extract_strikers_from(data),
        _extract_midfielders_from(data),
        _extract_defenders_from(data),
        _extract_goalkeapers_from(data))

def _extract_strikers_from(data: pd.DataFrame) -> pd.DataFrame:
    return _eliminate_irrelevant_data_from(data[data['position'] == 'Forward'])

def _extract_midfielders_from(data: pd.DataFrame) -> pd.DataFrame:
    return _eliminate_irrelevant_data_from(data[data['position'] == 'Midfielder'])

def _extract_defenders_from(data: pd.DataFrame) -> pd.DataFrame:
    return _eliminate_irrelevant_data_from(data[data['position'] == 'Defender'])

def _extract_goalkeapers_from(data: pd.DataFrame) -> pd.DataFrame:
    return _eliminate_irrelevant_data_from(data[data['position'] == 'Goalkeeper'])

def _eliminate_irrelevant_data_from(players):
    for column in list(players.columns):
        is_irrelevant_column = players[column].isnull().values.all()
        if is_irrelevant_column:
            players.drop(column, inplace=True, axis=1)
    players = players.drop_duplicates(subset=['player_name'], keep='first').reset_index(drop=True)
    return players

def _merge_data_for_players()->pd.DataFrame:
    UEFA_CHAMPIOS_LEAGUE_DATASETS = [
        'attacking.csv', 'attempts.csv',
        'defending.csv', 'disciplinary.csv',
        'distributon.csv', 'goalkeeping.csv',
        'key_stats.csv'
    ]

    data_set_merged = pd.DataFrame({'player_name':[]})
    for data_csv in UEFA_CHAMPIOS_LEAGUE_DATASETS:
        data_set_merged = pd.merge(left=data_set_merged,
                 right=_extract_data_from(f'data/{data_csv}'),
                 left_on='player_name',
                 right_on='player_name',
                 how='outer',
                suffixes=('_delete', ''))

    data_set_merged.drop([column for column in data_set_merged.columns if 'delete' in column],
                         axis=1, inplace=True)
    return data_set_merged

def _extract_data_from(file:str)->pd.DataFrame:
    return pd.read_csv(file, index_col=0, decimal=",")

#prueba = get_data_of_player_by_position()