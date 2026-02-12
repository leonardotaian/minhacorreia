import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mc_db",
    user="mc_admin",
    password="7355608",
    port="5432")

def obter_id_veiculo(placa):
    try:
        cursor = conn.cursor()
        sql_obter_id_veiculo = '''SELECT id FROM veiculo WHERE placa=%s'''
        cursor.execute(sql_obter_id_veiculo, (placa,))
        resultado = cursor.fetchone()
        if resultado:
            id_veiculo = resultado[0]
        else:
            id_veiculo = None
        return id_veiculo
    except Exception as e:
        print(e)
        return None

def criar_veiculo(placa, marca, modelo):
    try:
        cursor = conn.cursor()
        sql_criar_veiculo = '''INSERT INTO veiculo (placa, marca, modelo) VALUES (%s, %s, %s) RETURNING id'''
        cursor.execute(sql_criar_veiculo, (placa, marca, modelo))
        id_veiculo = cursor.fetchone()[0]
        conn.commit()
        return id_veiculo
    except Exception as e:
        print(e)
        return None

def cadastrar_oficina(nome, email, senha_hash):
    try:
        cursor = conn.cursor()
        sql_registro_oficina = '''INSERT INTO oficina (nome, email, pw) VALUES (%s, %s, %s)'''
        cursor.execute(sql_registro_oficina, (nome, email, senha_hash))
        conn.commit()
        msg = "Oficina registrada com sucesso!"
        return msg
    except Exception as e:
        print(e)
        return None

def consultar_oficina(email):
    try:
        cursor = conn.cursor()
        sql_consulta_oficina = '''SELECT * FROM oficina WHERE email=%s'''
        cursor.execute(sql_consulta_oficina, (email,))
        oficina = cursor.fetchone()
        return oficina
    except Exception as e:
        print(e)
        return None
    
def registrar_troca(id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel):
    try:
        cursor = conn.cursor()
        sql_registrar_troca = '''INSERT INTO troca (id_veiculo, data_troca, km_troca, km_proxima, data_proxima, id_oficina) VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql_registrar_troca, (id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel))
        conn.commit()
        msg = "Troca registrada com sucesso!"
        return msg
    except Exception as e:
        print(e)
        return None
    
def consultar_troca(id_veiculo):
    try:
        cursor = conn.cursor()
        sql_consultar_troca = '''SELECT data_troca, km_troca, km_proxima, data_proxima, id_oficina FROM troca WHERE id_veiculo=%s ORDER BY data_troca DESC'''
        cursor.execute(sql_consultar_troca, (id_veiculo,))
        trocas = cursor.fetchall()
        return trocas
    except Exception as e:
        print(e)
        return None
    
def consultar_duplicidade_email(email):
    try:
        cursor = conn.cursor()
        sql_consultar_email = '''SELECT id FROM oficina WHERE email=%s'''
        cursor.execute(sql_consultar_email, (email,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(e)
        return None
    
def consultar_duplicidade_nome(nome):
    try:
        cursor = conn.cursor()
        sql_consultar_nome = '''SELECT id FROM oficina WHERE nome=%s'''
        cursor.execute(sql_consultar_nome, (nome,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(e)
        return None
    