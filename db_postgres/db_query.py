import psycopg2
import csv

# Database connection settings
DB_NAME = "imdb"
DB_USER = "yaxiong"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Query the database (example: get all tables in 'public' schema)
cur.execute("SELECT * FROM name_basics WHERE primaryName LIKE '%a';")
rows = cur.fetchall()  # Fetch all results

# Output the results to a TSV file
with open("data/output_data.tsv", mode="w", newline="") as file:
    writer = csv.writer(file, delimiter="\t")  # Using tab as delimiter
    writer.writerow([desc[0] for desc in cur.description])  # Write column names
    writer.writerows(rows)  # Write data rows

print("Query results have been written to 'output_data.tsv'.")

# Close connection
cur.close()
conn.close()