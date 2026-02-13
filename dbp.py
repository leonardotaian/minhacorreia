import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="mc_db",
        user="mc_admin",
        password="7355608",
        port="5432")

def obter_id_veiculo(placa):
    placa = placa.strip().upper()
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_obter_id_veiculo = '''SELECT id FROM veiculo WHERE placa=%s'''
                cursor.execute(sql_obter_id_veiculo, (placa,))
                print(placa)
                resultado = cursor.fetchone()
                return resultado[0] if resultado else None                
    except Exception as e:
        print(e)
        return None


def criar_veiculo(placa, marca, modelo):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_criar_veiculo = '''INSERT INTO veiculo (placa, marca, modelo) VALUES (%s, %s, %s) RETURNING id'''
                cursor.execute(sql_criar_veiculo, (placa, marca, modelo))
                id_veiculo = cursor.fetchone()[0]
        return id_veiculo
    except Exception as e:
        print(e)
        return None
    
def obter_modelo_marca(id_veiculo):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_obter_modelo_marca = '''SELECT marca, modelo FROM veiculo WHERE id=%s'''
                cursor.execute(sql_obter_modelo_marca, (id_veiculo,))
                resultado = cursor.fetchone()
                return resultado if resultado else None                
    except Exception as e:
        print(e)
        return None

def cadastrar_oficina(nome, email, senha_hash):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_registro_oficina = '''INSERT INTO oficina (nome, email, pw) VALUES (%s, %s, %s)'''
                cursor.execute(sql_registro_oficina, (nome, email, senha_hash))
                msg = "Oficina registrada com sucesso!"
        return msg
    except Exception as e:
        print(e)
        return None

def consultar_oficina(email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_consulta_oficina = '''SELECT id, nome, email, pw FROM oficina WHERE email=%s'''
                cursor.execute(sql_consulta_oficina, (email,))
                oficina = cursor.fetchone()
        return oficina
    except Exception as e:
        print(e)
        return None
        
    
def registrar_troca(id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:   
                sql_registrar_troca = '''INSERT INTO troca (id_veiculo, data_troca, km_troca, km_proxima, data_proxima, id_oficina) VALUES (%s, %s, %s, %s, %s, %s)'''
                cursor.execute(sql_registrar_troca, (id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel))
                msg = "Troca registrada com sucesso!"
        return msg
    except Exception as e:
        print(e)
        return None
    
def consultar_troca(id_veiculo):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_consultar_troca = '''SELECT * FROM troca WHERE id_veiculo=%s ORDER BY data_troca DESC'''
                cursor.execute(sql_consultar_troca, (id_veiculo,))
                trocas = cursor.fetchall()
        return trocas
    except Exception as e:
        print(e)
        return None
    
def consultar_duplicidade_email(email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_consultar_email = '''SELECT email FROM oficina WHERE email=%s'''
                cursor.execute(sql_consultar_email, (email,))
                resultado = cursor.fetchone()
                print(resultado)
        return resultado[0] if resultado else None
    except Exception as e:
        print(e)
        return None
    
def consultar_duplicidade_nome(nome):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_consultar_nome = '''SELECT id FROM oficina WHERE nome=%s'''
                cursor.execute(sql_consultar_nome, (nome,))
                resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(e)
        return None
    
def nome_oficina(id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_nome_oficina = '''SELECT nome FROM oficina WHERE id=%s'''
                cursor.execute(sql_nome_oficina, (id,))
                resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(e)
        return None