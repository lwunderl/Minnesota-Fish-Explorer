#import dependencies
import psycopg2
from config import password

def main():
    connect()

def connect():
    print("Connecting to the PostgreSQL")
    conn = psycopg2.connect(host="localhost",
                            port=5432,
                            database="fish_finder_db",
                            user="postgres",
                            password=password)
    cur = conn.cursor()
    print("PostgreSQL database version:")

    cur.execute("SELECT version()")
    db_version = cur.fetchone()
    print(db_version)

    cur.execute("SELECT fish_description FROM fish_info WHERE fish_description LIKE '%Bass%'")
    response = cur.fetchall()
    fish_list = [x[0] for x in response]
    print(fish_list)

    cur.close()
    conn.close()
    print("PostgreSQL database is closed")

if __name__ == "__main__":
    main()