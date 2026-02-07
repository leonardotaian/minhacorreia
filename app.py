from flask import Flask, session, render_template, request, url_for, flash, redirect
import db, re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'

@app.template_filter('br_date')
def br_date(date_str):
    """Converte data de YYYY-MM-DD para DD-MM-YYYY"""
    if not date_str:
        return ''
    parts = str(date_str).split('-')
    if len(parts) == 3:
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    return date_str


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
        dupli_email = db.consultar_duplicidade_email(email)
        if dupli_email is True:
            msg = "Email já cadastrado. Faça login ou use outro email."
            return render_template('cadastro.html', msg=msg)
        elif dupli_email is None:
            msg = "Erro interno. Tente novamente."
            return render_template('cadastro.html', msg=msg)
        dupli_nome = db.consultar_duplicidade_nome(nome)
        if dupli_nome is True:
            msg = "Nome já cadastrado. Faça login ou use outro nome."
            return render_template('cadastro.html', msg=msg)
        elif dupli_nome is None:
            msg = "Erro interno. Tente novamente."
            return render_template('cadastro.html', msg=msg)
        
        senha_hash = generate_password_hash(senha)
        msg = db.cadastrar_oficina(nome, email, senha_hash)
        flash(msg, "success")
            
        oficina = db.consultar_oficina(email)
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
        oficina = db.consultar_oficina(email)
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
        id_veiculo = db.obter_id_veiculo(placa)
        if id_veiculo is None:
            msg = "Veículo não cadastrado."
            return render_template('consulta.html', msg=msg)
        veiculo = db.consultar_troca(id_veiculo)
        
        return render_template('consulta.html', msg=msg, veiculo=veiculo)
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
            msg = "Placa inválida. Use o formato ABC1234 ou ABC1D34 (mercosul)."
            return render_template('registro.html', msg=msg)
        if len (placa) != 7:
            msg = "Placa deve conter exatamente 7 caracteres."
            return render_template('registro.html', msg=msg)
        id_veiculo = db.obter_id_veiculo(placa)
        if id_veiculo is None:
            marca = request.form['marca']
            modelo =  request.form['modelo']
            id_veiculo = db.criar_veiculo(placa, marca, modelo)
        data_troca = request.form['data_troca']
        ano_atual = date.today().year
        ano = int(data_troca[:4])
        if ano != ano_atual:
            msg = "Ano da troca deve ser o ano atual."
            return render_template('registro.html', msg=msg)
        km_troca = int(request.form['km_troca'])
        if km_troca < 0:
            msg = "Quilometragem da troca deve ser maior que zero."
            return render_template('registro.html', msg=msg)
        if km_troca > 999999:
            msg = "Quilometragem não aceita (maior que 999.999 km)."
            return render_template('registro.html', msg=msg)
        km_proxima = int(request.form['km_proxima'])
        data_proxima = request.form['data_proxima']
        oficina_responsavel = session['usuario_nome']
        msg = db.registrar_troca(id_veiculo, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel)
        msg_type = 'success' if 'sucesso' in msg.lower() else 'error'
        return render_template('registro.html', msg=msg, msg_type=msg_type)
    return render_template('registro.html')




app.run(debug=True)