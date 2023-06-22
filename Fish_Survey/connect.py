#import dependencies
import psycopg2
from config import password, fish_db

def main():
    conn = connect_db(fish_db)
    cur = conn.cursor()
    search_criteria = input("What fish species are you looking for? ").title()
    cur.execute(f"SELECT fish_description FROM fish_info WHERE fish_description LIKE '%{search_criteria}%'")
    response = cur.fetchall()
    fish_list = [x[0] for x in response]
    print(fish_list)
    cur.close()
    close_db(conn)

def connect_db(database):
    print("Connecting to the PostgreSQL")
    conn = psycopg2.connect(host="localhost",
                            port=5432,
                            database=database,
                            user="postgres",
                            password=password)
    cur = conn.cursor()
    print("PostgreSQL database version:")
    cur.execute("SELECT version()")
    db_version = cur.fetchone()
    print(db_version)
    cur.close()
    return conn

def close_db(conn):
    conn.close()
    print("PostgreSQL database is closed")

if __name__ == "__main__":
    main()