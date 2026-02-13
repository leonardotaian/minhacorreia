from flask import Flask, session, render_template, request, url_for, flash, redirect
import dbp, re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'

def br_date_filter(date_obj):
    """Converte data para formato brasileiro DD/MM/YYYY"""
    if date_obj is None:
        return ''
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime('%d/%m/%Y')

app.jinja_env.filters['br_date'] = br_date_filter


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        msg = None
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        token = request.form['token']
        if token != "tokencadastrobeta":
            msg = "Token de cadastro inválido."
            return render_template('cadastro.html', msg=msg)
        dupli_email = dbp.consultar_duplicidade_email(email)
        if dupli_email:
            msg = "Email já cadastrado. Faça login ou use outro email."
            return render_template('cadastro.html', msg=msg)
        elif dupli_email is None:
            dupli_nome = dbp.consultar_duplicidade_nome(nome)
            if dupli_nome:
                msg = "Nome já cadastrado. Faça login ou use outro nome."
                return render_template('cadastro.html', msg=msg)
            elif dupli_nome is None:
                senha_hash = generate_password_hash(senha)
                msg = dbp.cadastrar_oficina(nome, email, senha_hash)
                flash(msg, "success")
                    
                oficina = dbp.consultar_oficina(email)
                session['usuario_id'] = oficina[0]
                session['usuario_nome'] = oficina[1]
                
                return redirect(url_for('index'))
        
        
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'usuario_id' in session:
            flash("Você já está logado.", "info")
            return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        oficina = dbp.consultar_oficina(email)
        if not oficina:
            msg = "Email ou senha incorretos."
            return render_template('login.html', msg=msg)
        senha_salva = oficina[3]
        senha_valida = check_password_hash(senha_salva, senha)
        if senha_valida is True:
            session['usuario_id'] = oficina[0]
            session['usuario_nome'] = oficina[1]
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for('registro'))
        else:
            msg = "Email ou senha incorretos."
            return render_template('login.html', msg=msg)
        
        
    return render_template('login.html')        

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    flash("Logout realizado com sucesso.")
    return redirect(url_for('index'))


@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        msg = None
        placa = request.form['placa']
        id_veiculo = dbp.obter_id_veiculo(placa)
        if id_veiculo is None:
            msg = "Veículo não cadastrado."
            return render_template('consulta.html', msg=msg)
        trocas = dbp.consultar_troca(id_veiculo)
        if not trocas:
            msg = "Nenhum registro de troca encontrado."
            return render_template('consulta.html', msg=msg)
        
        veiculo = trocas[0]
        data_troca = veiculo[2]
        km_troca = veiculo[3]
        km_proxima = veiculo[4]
        data_proxima = veiculo[5]
        oficina = dbp.nome_oficina(veiculo[6])
        mod_mar = dbp.obter_modelo_marca(id_veiculo)
        marca = mod_mar[0]
        modelo = mod_mar[1]
        
        
        return render_template('consulta.html', msg=msg, data_troca=data_troca, km_troca=km_troca, km_proxima=km_proxima, data_proxima=data_proxima, oficina=oficina, marca=marca, modelo=modelo)
    return render_template('consulta.html')

@app.route('/registro/troca', methods=['GET', 'POST'])    
def registro():
    if 'usuario_id' not in session:
        flash("Faça login para acessar o registro de troca.", "error")
        return redirect(url_for('login'))
    if request.method == 'POST':
        
        placa = request.form['placa']
        placa = placa.strip().upper()
        padrao_antigo = r'^[A-Z]{3}[0-9]{4}$'
        padrao_mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'
        if not (re.match(padrao_antigo, placa) or re.match(padrao_mercosul, placa)):
            msg = "Placa inválida. Use o formato ABC1234 (antigo) ou ABC1D23 (mercosul)."
            return render_template('registro.html', msg=msg)
        if len (placa) != 7:
            msg = "Placa deve conter exatamente 7 caracteres."
            return render_template('registro.html', msg=msg)
        
        id_veiculo = dbp.obter_id_veiculo(placa)
        
        if id_veiculo is None:
            marca = request.form['marca']
            modelo =  request.form['modelo']
            id_veiculo = dbp.criar_veiculo(placa, marca, modelo)

        if id_veiculo is None:
            msg = "Erro ao criar veículo"
            return render_template('registro.html', msg=msg)
        
        data_troca = request.form['data_troca']
        ano_atual = date.today().year
        try:
            data_obj = datetime.strptime(data_troca, '%Y-%m-%d')
        except ValueError:
            msg = "Data de troca inválida. Use o formato disponibilizado no calendário."
            return render_template('registro.html', msg=msg)
        if data_obj.year != ano_atual:
            msg = "Ano da troca deve ser o ano atual, o sistema não registra trocas antigas."
            return render_template('registro.html', msg=msg)
        
        try:
            km_troca = int(request.form['km_troca'])
        except ValueError:
            msg = "Quilometragem da troca inválida. Deve ser um número inteiro."
            return render_template('registro.html', msg=msg)
            
        if km_troca < 0:
            msg = "Quilometragem da troca deve ser maior que zero."
            return render_template('registro.html', msg=msg)
        
        if km_troca > 999999:
            msg = "Quilometragem não aceita: (maior que 999.999 km)."
            return render_template('registro.html', msg=msg)
        try:
            km_proxima = int(request.form['km_proxima'])
        except ValueError:
            msg = "Quilometragem da próxima troca inválida. Deve ser um número inteiro."
            return render_template('registro.html', msg=msg)
        if km_troca >= km_proxima:
            msg = "Quilometragem da próxima troca deve ser maior que a quilometragem da troca atual."
            return render_template('registro.html', msg=msg)
        
        data_proxima = request.form['data_proxima']
        oficina_responsavel = session['usuario_id']
        
        msg = dbp.registrar_troca(id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel)
        if msg is None:
            msg = "Erro ao registrar troca."
        msg_type = 'success' if msg and 'sucesso' in msg.lower() else 'error'
        
        return render_template('registro.html', msg=msg, msg_type=msg_type)
    return render_template('registro.html')


app.run(host='0.0.0.0', port=5000, debug=True)