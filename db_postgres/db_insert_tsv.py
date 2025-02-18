import psycopg2
from psycopg2 import sql
import random
from datetime import datetime
import csv

# Database connection details
DB_CONFIG = {
    "dbname": "imdb",
    "user": "yaxiong",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(**DB_CONFIG)


# Create table if not exists
def create_table():
    query = """
    CREATE TABLE name_basics (
    id SERIAL PRIMARY KEY,
    nconst TEXT UNIQUE,
    primaryName TEXT,
    birthYear INTEGER,
    deathYear INTEGER,
    primaryProfession TEXT,
    knownForTitles TEXT
    );
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    print("Table 'name_basics' created successfully.")


# Open tsv file and insert data
def insert_data():
    with connect_db() as conn:
        with conn.cursor() as cur:

            # Open the TSV file
            with open("data/name.basics.tsv", "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter="\t")  # TSV uses '\t' as delimiter
                next(reader)  # Skip the header row
                
                line_id = 0
                for row in reader:
                    if line_id == 10000: # save first 10000 data
                        break
                    # Replace '\N' with None (NULL in PostgreSQL)
                    row = [None if val == "\\N" else val for val in row]

                    # Insert into PostgreSQL
                    cur.execute("""
                        INSERT INTO name_basics (nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, row)

                    line_id += 1

        # Commit and close
        conn.commit()
        cur.close()


if __name__ == "__main__":
    create_table()
    insert_data()