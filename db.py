import sqlite3

def cadastrar_veiculo(id, marca, modelo, placa):
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

def cadastrar_oficina(id, nome, email, senha):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_oficina = f'INSERT INTO oficina (id, nome, email, senha) VALUES ({id}, "{nome}", "{email}", "{senha}")'
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

def registrar_troca(id, id_veiculo, placa, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_registro_troca = f'INSERT INTO troca_correia (id, id_veiculo, placa, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel) VALUES ({id}, {id_veiculo}, "{placa}", "{data_troca}", {km_troca}, {km_proxima}, "{data_proxima}", "{oficina_responsavel}")'
        cursor.execute(sql_registro_troca)
        conn.commit()
        conn.close()
        msg = "Troca de correia registrada com sucesso!"
        return msg
    except Exception as e:
        return f"Erro ao registrar troca de correia: {e}"
    
def consultar_troca(placa):
    try:
        conn = sqlite3.connect('mc.db')
        cursor = conn.cursor()
        sql_consulta_troca = f'SELECT * FROM troca_correia WHERE placa="{placa}"'
        cursor.execute(sql_consulta_troca)
        troca = cursor.fetchone()
        conn.close()
        return troca
    except Exception as e:
        return f"Erro ao consultar troca de correia: {e}"