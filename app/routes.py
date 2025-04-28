from app import app
from flask import render_template
from flask import request

@app.route('/')
def index():
    nome = "Kali"
    array = ["5", "2", "3"]
    return render_template('index.html', nome=nome, array= array)

@app.route('/calculadora')
def calculadora():
    return render_template('calculadora.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    valor_1 = int(request.form.get('int1'))
    valor_2 = int(request.form.get('int2'))

    resultado = str(valor_1 + valor_2)

    return render_template('calcular.html', resultado= resultado)