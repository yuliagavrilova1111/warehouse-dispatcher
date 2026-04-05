from collections import defaultdict
import pandas as pd
from typing import Dict, List, Any

history_store: Dict[int, List[dict]] = defaultdict(list)
orders_store: List[dict] = []

MAX_LAG = 48

async def connect_to_db():
    print("Using in-memory storage")
    if not history_store:
        print("Loading initial history from train_team_track.parquet")
        try:
            await load_initial_history_from_parquet()
        except Exception as e:
            print(f"Error loading history: {e}")
    else:
        print("History store already contains data.")

async def close_db_connection():
    print('In-memory storage closed')

async def load_initial_history_from_parquet():
    try:
        file_path = 'data/train_team_track.parquet'
        print(f"Looking for file: {file_path}")
        import os
        if not os.path.exists(file_path):
            print(f"File not found: {os.path.abspath(file_path)}")
            return
        train_df = pd.read_parquet(file_path)
        print(f"Loaded {len(train_df)} rows from parquet")
        train_df['timestamp'] = pd.to_datetime(train_df['timestamp'])
        train_df = train_df.sort_values(['route_id', 'timestamp'])
        for route_id, group in train_df.groupby('route_id'):
            last_records = group.tail(MAX_LAG)
            for _, row in last_records.iterrows():
                history_store[route_id].append(row.to_dict())
        print(f"Loaded history for {len(history_store)} routes")
    except Exception as e:
        print(f"Exception in load_initial_history: {e}")
        raise

async def save_history(route_id: int, row: dict, max_lag: int = MAX_LAG):
    history_store[route_id].append(row)
    if len(history_store[route_id]) > max_lag:
        history_store[route_id] = history_store[route_id][-max_lag:]

async def get_history(route_id: int, max_lag: int = MAX_LAG) -> List[Dict[str, Any]]:
    if route_id not in history_store or not history_store[route_id]:
        return []
    df = pd.DataFrame(history_store[route_id])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df.tail(max_lag).to_dict(orient='records')

async def save_order(order: Dict[str, Any]) -> int:
    order_id = len(orders_store) + 1
    order_copy = order.copy()
    order_copy['id'] = order_id
    orders_store.append(order_copy)
    return order_id

async def get_orders() -> List[Dict[str, Any]]:
    return orders_store