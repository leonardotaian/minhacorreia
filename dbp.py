import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mc_db",
    user="mc_admin",
    password="7355608",
    port="5432")

