import pandas as pd
import numpy as np
from typing import List

def build_features_from_history(
        hist_df: pd.DataFrame,
        target_timestamp: pd.Timestamp,
        features_list: List[str],
        max_lag: int=48
) -> pd.DataFrame:
    """
    Строит признаки для одного момента времени на основе истории.
    Возвращает DataFrame с одной строкой и колонками в порядке features_list.
    """
    features = hist_df.iloc[-1].to_dict()
    features.pop('timestamp', None)
    features.pop('target_2h', None)

    features['hour'] = target_timestamp.hour
    features['weekday'] = target_timestamp.weekday()
    features['month'] = target_timestamp.month

    for col in features_list:
        if col.startswith('status_') and '_lag' in col:
            status, str_lag = col.split('_lag')
            lag = int(str_lag)

            if lag <= len(hist_df):
                features[col] = hist_df.iloc[-lag][status]
            else:
                features[col] = hist_df.iloc[0][status]
        
    for col in features_list:
        if 'target_lag' in col:
            targ_lag = int(col.split('target_lag')[-1])
                
            if targ_lag <= len(hist_df):
                features[col] = hist_df.iloc[-targ_lag]['target_2h']
            else:
                features[col] = hist_df.iloc[0]['target_2h']

    X = pd.DataFrame([features])[features_list]
    return X