import math
from datetime import datetime
from typing import Dict, Any
from .config import TRUCK_CAPACITY, SAFETY_FACTOR

def calculate_trucks(predicted_volume: float) -> int:
    required = (predicted_volume * SAFETY_FACTOR) / TRUCK_CAPACITY
    return math.ceil(required)

def create_order(route_id: int, forecast_timestamp: datetime, trucks: int) -> Dict[str, Any]:
    """Формирует заявку на транспорт."""
    return {
        'route_id': route_id,
        'forecast_timestamp': forecast_timestamp.isoformat(),
        'trucks': trucks,
        'created_at': datetime.now().isoformat(),
        'status': 'pending'
    }