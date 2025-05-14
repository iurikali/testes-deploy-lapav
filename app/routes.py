from app import app
from flask import render_template
from flask import request
from flask import Response
from flask import send_file
from your_code import *

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    comprimento = float(request.form.get('comprimento'))
    posicao_x = float(request.form.get('posicao_x'))
    posicao_y = float(request.form.get('posicao_y'))
    valor_x = float(request.form.get('valor_x'))
    valor_y = float(request.form.get('valor_y'))
    inicio = float(request.form.get('inicio'))
    fim = float(request.form.get('fim'))
    carga = float(request.form.get('carga'))
    output = calcula(comprimento= comprimento, posicao_x= posicao_x, posicao_y= posicao_y, valor_x= valor_x, valor_y= valor_y, inicio= inicio, fim= fim, carga= carga)

    return send_file(
        output[0],
        as_attachment=True,
        download_name=output[1]
    )
  return render_template('inputs.html')