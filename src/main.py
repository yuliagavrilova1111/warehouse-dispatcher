from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from . import config, feature_builder, dispatcher, database
import numpy as np
import joblib
import json
import pandas as pd
from contextlib import asynccontextmanager

lgb_model = joblib.load('models/lgb_model.pkl')
xgb_model = joblib.load('models/xgb_model.pkl')
cat_model = joblib.load('models/cat_model.pkl')
meta_model = joblib.load('models/meta_model.pkl')

with open('models/features.json', 'r') as f:
    features = json.load(f)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect_to_db()
    yield
    await database.close_db_connection()

app = FastAPI(title='Warehouse Transport Dispatcher', version='1.0', lifespan=lifespan)

class ForecastRequest(BaseModel):
    route_id: int
    forecast_timestamp: str

class ForecastResponse(BaseModel):
    route_id: int
    forecast_timestamp: str
    predicted_volume: float
    required_trucks: int
    order_id: Optional[int] = None

@app.post('/forecast', response_model=ForecastResponse)
async def forecast(request: ForecastRequest):
    history_list = await database.get_history(request.route_id, max_lag=config.MAX_LAG)
    if not history_list:
        raise HTTPException(status_code=404, detail=f'No history for route {request.route_id}')
    
    hist_df = pd.DataFrame(history_list)
    hist_df['timestamp'] = pd.to_datetime(hist_df['timestamp'])
    hist_df = hist_df.sort_values('timestamp').reset_index(drop=True)

    ts = datetime.fromisoformat(request.forecast_timestamp)
    X = feature_builder.build_features_from_history(hist_df, ts, features, max_lag=config.MAX_LAG)

    lgb_pred = lgb_model.predict(X)[0]
    xgb_pred = xgb_model.predict(X)[0]
    cat_pred = cat_model.predict(X)[0]

    X_meta = np.column_stack([lgb_pred, xgb_pred, cat_pred])
    meta_pred = meta_model.predict(X_meta)[0]

    trucks = dispatcher.calculate_trucks(meta_pred)

    order = dispatcher.create_order(request.route_id, ts, trucks)
    order_id = await database.save_order(order)

    new_row = {
        'timestamp': ts.isoformat(),
        'target_2h': meta_pred
    }

    last_row = hist_df.iloc[-1].to_dict()
    for i in range(1, 9):
        new_row[f'status_{i}'] = last_row.get(f'status_{i}', 0)
    
    await database.save_history(request.route_id, new_row)

    return ForecastResponse(
        route_id=request.route_id,
        forecast_timestamp=request.forecast_timestamp,
        predicted_volume=meta_pred,
        required_trucks=trucks,
        order_id=order_id
    )

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/orders')
async def list_orders():
    orders = await database.get_orders()
    return {'orders': orders}