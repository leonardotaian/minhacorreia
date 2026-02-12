import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mc_db",
    user="mc_admin",
    password="7355608",
    port="5432")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS oficina (
               id SERIAL PRIMARY KEY,
               nome VARCHAR(255) NOT NULL UNIQUE,
               email VARCHAR(255) NOT NULL UNIQUE,
                pw VARCHAR(255) NOT NULL)''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS veiculo (
                id SERIAL PRIMARY KEY,
                placa VARCHAR(20) NOT NULL UNIQUE,
               marca VARCHAR(255) NOT NULL,
                modelo VARCHAR(255) NOT NULL)''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS troca (
               id SERIAL PRIMARY KEY,
                id_veiculo INTEGER NOT NULL,
               data_troca DATE NOT NULL,
                km_troca INTEGER NOT NULL,
               km_proxima INTEGER NOT NULL,
                data_proxima DATE NOT NULL,
                id_oficina INTEGER NOT NULL,
                FOREIGN KEY (id_veiculo) REFERENCES veiculo (id),
               FOREIGN KEY (id_oficina) REFERENCES oficina (id))''')
conn.commit()

conn.close()
