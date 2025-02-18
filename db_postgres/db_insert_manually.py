import psycopg2
from psycopg2 import sql
import random
from datetime import datetime

# Database connection details
DB_CONFIG = {
    "dbname": "test_database",
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
    CREATE TABLE IF NOT EXISTS chat_messages (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    print("Table 'chat_messages' created successfully.")

# Generate fake messages
def generate_messages(n=5):
    sample_messages = [
        "Hello, how can I help you?",
        "I am a chatbot, ask me anything!",
        "What’s your favorite programming language?",
        "Do you need help with FastAPI or Docker?",
        "PostgreSQL is a great choice for databases!"
    ]
    messages = [
        (random.randint(1, 10), random.choice(sample_messages), datetime.now())
        for _ in range(n)
    ]
    return messages

# Insert data into table
def insert_messages(messages):
    query = """
    INSERT INTO chat_messages (user_id, message, created_at)
    VALUES (%s, %s, %s);
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, messages)
            conn.commit()
    print(f"{len(messages)} messages inserted successfully.")

if __name__ == "__main__":
    create_table()
    messages = generate_messages()
    insert_messages(messages)