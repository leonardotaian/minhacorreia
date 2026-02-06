import sqlite3


def obter_id_veiculo(placa, marca, modelo):
    placa = placa.strip().upper()
    marca = marca.upper()
    modelo = modelo.upper()
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_obter_id = '''SELECT id FROM veiculo WHERE placa = ?'''
        cursor.execute(sql_obter_id, (placa,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        else:
            conn = sqlite3.connect('mc.db')
            cursor = conn.cursor() 
            sql_registrar_veiculo = '''INSERT INTO veiculo (marca, modelo, placa) VALUES (?, ?, ?)'''
            cursor.execute(sql_registrar_veiculo, (marca, modelo, placa))
            resultado = cursor.lastrowid
            conn.commit()
            conn.close()
            return resultado
            
    except Exception as e:
        return f"Erro ao obter ID do veículo: {e}"


def consultar_veiculo(placa):
    placa = placa.strip().upper()
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_veiculo = '''SELECT * FROM veiculo WHERE placa=?'''
        cursor.execute(sql_consulta_veiculo,(placa,))
        veiculo = cursor.fetchone()
        conn.close()
        return veiculo
    except Exception as e:
        return f"Erro ao consultar veículo: {e}"

def cadastrar_oficina(nome, email, senha):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_oficina = '''INSERT INTO oficina ( nome, email, senha) VALUES (?, ?, ?)'''
        cursor.execute(sql_registro_oficina, (nome, email, senha))
        conn.commit()
        conn.close()
        msg = "Oficina registrada com sucesso!"
        return msg
    except Exception as e:
        return f"Erro ao registrar oficina: {e}"

def consultar_oficina(email):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_oficina = '''SELECT * FROM oficina WHERE email=?'''
        cursor.execute(sql_consulta_oficina, (email,))
        oficina = cursor.fetchone()
        conn.close()
        return oficina
    except Exception as e:
        return f"Erro ao consultar oficina: {e}"

def registrar_troca(id_veiculo, placa, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel,):
    placa = placa.strip().upper()
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_troca = '''INSERT INTO trocas (id_veiculo, placa, data_troca, km_troca, km_proxima, data_proxima, oficina) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(sql_registro_troca, (id_veiculo, placa, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel))
        conn.commit()
        conn.close()
        msg = "Troca de correia registrada com sucesso!"
        return msg
    except Exception as e:
        msg = f"Erro ao registrar troca de correia: {e}"
        return msg
    
def consultar_troca(placa):
    placa = placa.strip().upper()   
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_troca = '''SELECT * FROM trocas WHERE placa=?'''
        cursor.execute(sql_consulta_troca,(placa,))
        msg = cursor.fetchone()
        conn.close()
        return msg
    except Exception as e:
        return f"Erro ao consultar troca de correia: {e}"
    
    
