import os
import psycopg2

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', 5432)
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')


db = None
try:
    db = psycopg2.connect(f"dbname='{DB_NAME}' sslmode='disable' "
                          f"host={DB_HOST} port='{DB_PORT}' "
                          f"user='{DB_USER}' password='{DB_PASSWORD}'")
    print("Connection established.")
except Exception as e:
    print(f"I am unable to connect to the database: {e}")


def main():
    if db:
        cur = db.cursor()
        cur.execute("""SELECT datname from pg_database""")
        return [row[0] for row in cur.fetchall()]
    else:
        raise Exception("Database is unavailable")


if __name__ == '__main__':
    print(main())
