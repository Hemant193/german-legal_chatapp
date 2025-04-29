from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
import psycopg2
import os

load_dotenv()

# Get the environment variables for .env file
connection = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)

# Establish the connection with the DB
curr = connection.cursor()
register_vector(connection)
curr.execute("SELECT 1")


print("DATABASE Connection successful:", curr.fetchone())

# Closing of connection to the DB after completion
curr.close()
connection.close()