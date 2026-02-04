from flask import Flask, render_template, request, url_for
import db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    return render_template('consulta.html')
@app.route('/consulta/veiculo', methods=['GET', 'POST'])
def consulta_veiculo():
    if request.method == 'POST':
        placa = request.form['placa']
        veiculo = db.consultar_veiculo(placa)
        if not veiculo:
                veiculo = "Veículo não encontrado."
        return render_template('registro.html', veiculo=veiculo)
    print(veiculo)
    return render_template('registro.html')

@app.route('/registro/troca', methods=['GET', 'POST'])    
def registro():
    if request.method == 'POST':
        placa = request.form['placa']
        data_troca = request.form['data_troca']
        km_troca = request.form['km_troca']
        km_proxima = request.form['km_proxima']
        data_proxima = request.form['data_proxima']
        oficina_responsavel = request.form['oficina']
        msg = db.registrar_troca(placa, data_troca, km_troca, km_proxima, data_proxima, oficina_responsavel)
        return render_template('registro.html', msg=msg)
    return render_template('registro.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        id = request.form['id']
        marca = request.form['marca']
        modelo = request.form['modelo']
        placa = request.form['placa']
        msg = db.cadastrar_veiculo(id, marca, modelo, placa)
        return render_template('cadastro.html', msg=msg)



app.run(debug=True)