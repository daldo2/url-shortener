import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="url_shortener_db",
        user="postgres",
        host="localhost",
        port="5432"
    )

def init_db():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                short_code VARCHAR(10) UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                click_count INT DEFAULT 0
            );
        """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()