import sqlite3


def obter_id_veiculo(placa):
    placa = placa.strip().upper()
    conn = sqlite3.connect('mc.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id FROM veiculo WHERE placa = ?',
        (placa,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def criar_veiculo(placa, marca, modelo):
    try:
        placa = placa.strip().upper()
        marca = marca.upper()
        modelo = modelo.upper()
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO veiculo (placa, marca, modelo) VALUES (?, ?, ?)',
            (placa, marca, modelo))
        id_veiculo = cursor.lastrowid
        conn.commit()
        conn.close()
        return id_veiculo
    except Exception:
        return None



def cadastrar_oficina(nome, email, senha_hash):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_oficina = '''INSERT INTO oficina (nome, email, pw) VALUES (?, ?, ?)'''
        cursor.execute(sql_registro_oficina, (nome, email, senha_hash))
        conn.commit()
        conn.close()
        msg = "Oficina registrada com sucesso!"
        return msg
    except Exception as e:
        return None

def consultar_oficina(email):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_oficina = '''SELECT * FROM oficina WHERE email=?'''
        cursor.execute(sql_consulta_oficina, (email,))
        oficina = cursor.fetchone()
        conn.close()
        return oficina
    except Exception:
        return None

def registrar_troca(id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel,):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_troca = '''INSERT INTO trocas (id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina) VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(sql_registro_troca, (id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel))
        conn.commit()
        conn.close()
        msg = "Troca de correia registrada com sucesso!"
        return msg
    except Exception as e:
        msg = f"Erro ao registrar troca de correia: {e}"
        return msg
    
def consultar_troca(id_veiculo):  
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_troca = '''SELECT * FROM trocas WHERE id_veiculo=?'''
        cursor.execute(sql_consulta_troca,(id_veiculo,))
        msg = cursor.fetchall()
        conn.close()
        return msg
    except Exception:
        return None
    
def consultar_duplicidade_email(email):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_email = '''SELECT email FROM oficina WHERE email=?'''
        cursor.execute(sql_consulta_email, (email,))
        resultado = cursor.fetchone()
        if resultado:
            email_existe = True
        else:
            email_existe = False
        conn.close()
        return email_existe
    except Exception as e:
        print(e)
        return None
    

    
def consultar_duplicidade_nome(nome):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_nome = '''SELECT nome FROM oficina WHERE nome=?'''
        cursor.execute(sql_consulta_nome, (nome,))
        resultado = cursor.fetchone()
        if resultado:
            nome_existe = True
        else:
            nome_existe = False
        conn.close()
        return nome_existe
    except Exception as e:
        print(e)
        return None
    
