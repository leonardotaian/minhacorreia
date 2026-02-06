from flask import Flask, render_template, request, url_for
import db

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
        id_veiculo = db.obter_id_veiculo(request.form['placa'], request.form['marca'], request.form['modelo'])
        placa = request.form['placa']
        data_troca = request.form['data_troca']
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