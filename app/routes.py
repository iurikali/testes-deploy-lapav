from app import app
from flask import render_template
from flask import request
from flask import Response
from flask import send_file
from your_code import *

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    e_1 = int(request.form.get('e_1'))
    e_2 = int(request.form.get('e_2'))
    e_3 = int(request.form.get('e_3'))
    h_1 = int(request.form.get('h_1'))
    h_2 = int(request.form.get('h_2'))
    nu_1 = float(request.form.get('nu_1'))
    nu_2 = float(request.form.get('nu_2'))
    nu_3 = float(request.form.get('nu_3'))
    l_1 = int(request.form.get('l_1'))
    l_2 = int(request.form.get('l_2'))
    lposx_1 = int(request.form.get('lposx_1'))
    lposy_1 = int(request.form.get('lposy_1'))
    lposx_2 = int(request.form.get('lposx_2'))
    lposy_2 = int(request.form.get('lposy_2'))
    a_1 = int(request.form.get('a_1'))
    x_1_1 = int(request.form.get('x_1_1'))
    x_2_1 = int(request.form.get('x_2_1'))
    x_3_1 = int(request.form.get('x_3_1'))
    y_1 = int(request.form.get('y_1'))
    z_1_1 = float(request.form.get('z_1_1'))
    x_1 = int(request.form.get('x_1'))
    x_2 = int(request.form.get('x_2'))
    x_3 = int(request.form.get('x_3'))
    z_1 = int(request.form.get('z_1'))
    z_2 = int(request.form.get('z_2'))
    z_3 = int(request.form.get('z_3'))
    xx = int(request.form.get('xx'))
    depth = int(request.form.get('depth'))
    h_3 = int(request.form.get('h_3'))
    h_4 = int(request.form.get('h_4'))
    output = calcula(e_1= e_1, e_2= e_2, e_3= e_3, h_1= h_1, h_2= h_2, nu_1= nu_1, nu_2= nu_2, nu_3= nu_3, l_1= l_1, l_2= l_2, lposx_1= lposx_1, lposy_1= lposy_1, lposx_2= lposx_2, lposy_2= lposy_2, a_1= a_1, x_1_1= x_1_1, x_2_1= x_2_1, x_3_1= x_3_1, y_1= y_1, z_1_1= z_1_1, x_1= x_1, x_2= x_2, x_3= x_3, z_1= z_1, z_2= z_2, z_3= z_3, xx= xx, depth= depth, h_3= h_3, h_4= h_4)

    return send_file(
        output[0],
        as_attachment=True,
        download_name=output[1]
    )
  return render_template('inputs.html')