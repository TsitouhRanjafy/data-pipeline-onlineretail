CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50),
    stock_code VARCHAR(50),
    description TEXT,
    quantity INTEGER,
    invoice_date TIMESTAMP,
    unit_price NUMERIC(10, 2),
    customer_id NUMERIC,
    country VARCHAR(100),
    total_amount NUMERIC(10, 2),
    uploaded_at TIMESTAMP,
    processed_at TIMESTAMP,
    change_type VARCHAR(20)
);