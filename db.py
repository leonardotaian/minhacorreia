import sqlite3


def obter_id_veiculo(placa, marca, modelo):
    placa = placa.strip().upper()
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_obter_id = '''SELECT id FROM veiculo WHERE placa = ? AND marca = ? AND modelo = ?'''
        cursor.execute(sql_obter_id, (placa, marca, modelo))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            conn = sqlite3.connect('mc.db')
            cursor = conn.cursor() 
            sql_registrar_veiculo = '''INSERT INTO veiculo (marca, modelo, placa) VALUES (?, ?, ?)'''
            cursor.execute(sql_registrar_veiculo, (marca, modelo, placa))
            resultado = cursor.lastrowid()
            conn.commit()
            conn.close()
            return resultado
            
    except Exception as e:
        return f"Erro ao obter ID do veículo: {e}"

def cadastrar_veiculo(id, marca, modelo, placa):
    placa = placa.strip().upper()
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_cadastro_veiculo = f'INSERT INTO veiculo (id, marca, modelo, placa) VALUES ({id}, "{marca}", "{modelo}", "{placa}")'
        cursor.execute(sql_cadastro_veiculo)
        conn.commit()
        conn.close()
        msg = "Veículo cadastrado com sucesso!"
        return msg
    except Exception as e:
        return f"Erro ao cadastrar veículo: {e}"

def consultar_veiculo(placa):
    placa = placa.strip().upper()
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_veiculo = f'SELECT * FROM veiculo WHERE placa="{placa}"'
        cursor.execute(sql_consulta_veiculo)
        veiculo = cursor.fetchone()
        conn.close()
        return veiculo
    except Exception as e:
        return f"Erro ao consultar veículo: {e}"

def cadastrar_oficina(nome, email, senha):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_oficina = f'INSERT INTO oficina ( nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")'
        cursor.execute(sql_registro_oficina)
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
        sql_consulta_oficina = f'SELECT * FROM oficina WHERE email="{email}"'
        cursor.execute(sql_consulta_oficina)
        oficina = cursor.fetchone()
        conn.close()
        return oficina
    except Exception as e:
        return f"Erro ao consultar oficina: {e}"

def registrar_troca(id_veiculo, placa, marca, modelo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel):
    placa = placa.strip().upper()
    id_veiculo = obter_id_veiculo(placa, marca, modelo)
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_troca = '''INSERT INTO trocas (id, id_veiculo, placa, marca, modelo, data_troca, km_troca, km_proxima, data_proxima, oficina) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(sql_registro_troca, (id_veiculo, placa, marca, modelo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel))
        conn.commit()
        conn.close()
        msg = "Troca de correia registrada com sucesso!"
        return msg
    except Exception as e:
        return f"Erro ao registrar troca de correia: {e}"
    
def consultar_troca(placa):
    placa = placa.strip().upper()   
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_troca = f'SELECT * FROM trocas WHERE placa="{placa}"'
        cursor.execute(sql_consulta_troca)
        troca = cursor.fetchone()
        conn.close()
        return troca
    except Exception as e:
        return f"Erro ao consultar troca de correia: {e}"