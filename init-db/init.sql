CREATE TABLE IF NOT EXISTS route_history (
    id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    target_2h FLOAT,
    status_1 INTEGER,
    status_2 INTEGER,
    status_3 INTEGER,
    status_4 INTEGER,
    status_5 INTEGER,
    status_6 INTEGER,
    status_7 INTEGER,
    status_8 INTEGER
);

CREATE TABLE IF NOT EXISTS transport_orders (
    id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL,
    forecast_timestamp TIMESTAMP NOT NULL,
    required_trucks INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS idx_route_history_route_timestamp ON route_history(route_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_transport_orders_route_id ON transport_orders(route_id);