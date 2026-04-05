import os

TRUCK_CAPACITY = 100.0      # единиц товара на одну машину
SAFETY_FACTOR = 1.2         # страховой запас (20%)
FORECAST_HORIZON_HOURS = 2  # прогноз на 2 часа
MAX_LAG = 48                # максимальное количество хранимых исторических записей (48 * 30 мин = 24 часа)

DB_CONFIG = {
    'user': os.getenv('POSTGRES_USER', 'yulia_gavrilova'),
    'password': os.getenv('POSTGRES_PASSWORD', 'wildhack4295_fROvc83'),
    'database': os.getenv('POSTGRES_DB', 'wildhack_db'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', 5432)
}