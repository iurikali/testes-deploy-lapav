from app import app
from flask import render_template
from flask import request
from flask import Response
from calc_viga import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculadora')
def calculadora():
    return render_template('calculadora.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    l = float(request.form.get('comprimento'))
    posicao = (float(request.form.get('posicao_x')), float(request.form.get('posicao_y')))
    valor = (float(request.form.get('valor_x')), float(request.form.get('valor_y')))
    dist = (float(request.form.get('inicio')), float(request.form.get('fim')), float(request.form.get('q')))
    buf = calcula(l, posicao, valor, dist)
    return Response(buf, mimetype='image/png')