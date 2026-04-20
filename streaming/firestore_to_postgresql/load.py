from psycopg2 import pool


DB_CONFIG = {
    "dbname": "streaming_pipeline",
    "user": "pipeline_user",
    "password": "Chang3me!",
    "host": "192.168.1.100",
    "port": 5432,
}

open_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def load(record: dict) -> None:
    conn = open_pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (
                invoice_no, stock_code, description, quantity,
                invoice_date, unit_price, customer_id, country,
                total_amount, uploaded_at, processed_at, change_type
            ) VALUES (
                %(invoice_no)s, %(stock_code)s, %(description)s, %(quantity)s,
                %(invoice_date)s, %(unit_price)s, %(customer_id)s, %(country)s,
                %(total_amount)s, %(uploaded_at)s, %(processed_at)s, %(change_type)s
            )
        """, record)
        conn.commit()
        print(f" [{record['processed_at']}] {record['change_type']} → {record['invoice_no']}")
        cur.close()
    except Exception as e:
        conn.rollback()         
        print(f" Erreur load: {e}")
    finally:
        open_pool.putconn(conn)