from flask import Flask, render_template, request, url_for
import db, re
from datetime import date
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        msg = None
        placa = request.form['placa']
        veiculo = db.consultar_troca(placa)
        if not veiculo:
                msg = "Nenhuma troca registrada para este veículo."
        return render_template('consulta.html', msg=msg, veiculo=veiculo)
    return render_template('consulta.html')
@app.route('/consulta/veiculo', methods=['GET', 'POST'])
def consulta_veiculo():
    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        veiculo = db.obter_id_veiculo(placa, marca, modelo)
        if not veiculo:
                veiculo = "Veículo não encontrado."
        return render_template('consulta.html', veiculo=veiculo)
    print(veiculo)
    return render_template('registro.html')

@app.route('/registro/troca', methods=['GET', 'POST'])    
def registro():
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
        id_veiculo = db.obter_id_veiculo(request.form['placa'], request.form['marca'], request.form['modelo'])
        data_troca = request.form['data_troca']
        ano_atual = date.today().year
        ano = int(data_troca[:4])
        if ano != ano_atual:
            msg = "Ano da troca deve ser o ano atual."
            return render_template('registro.html', msg=msg)
        km_troca = int(request.form['km_troca'])
        km_proxima = int(request.form['km_proxima'])
        data_proxima = request.form['data_proxima']
        oficina_responsavel = request.form['oficina_responsavel']
        msg = db.registrar_troca(id_veiculo, placa, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel)
        return render_template('registro.html', msg=msg)
    return render_template('registro.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        placa = request.form['placa']
        id = db.obter_id_veiculo(placa, marca, modelo)
        msg = db.cadastrar_veiculo(id, marca, modelo, placa)
        return render_template('cadastro.html', msg=msg)



app.run(debug=True)