import io
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

'''
def calcula(valor_1, valor_2):    
    resultado = valor_1 + valor_2
    resultado_string = "O RESULTADO DA SOMA EH: " + str(resultado)

    buffer = io.BytesIO()
    buffer.write(resultado_string.encode('utf-8'))
    buffer.seek(0)

    nome = "soma.txt"

    lista_retorno = [buffer, nome]

    return lista_retorno
'''


def calcula(comprimento, posicao_x, posicao_y, valor_x, valor_y, inicio, fim, carga):

    posicao = (posicao_x, posicao_y)
    valor = (valor_x, valor_y)
    dist = (inicio, fim, carga)

    # Dados de entrada (exemplo)
    tipo_viga = "apoiada-apoiada"  # ou "engastada-livre"
    L = comprimento  # comprimento da viga em metros
    NP = 1000  # pontos de discretização
    cargas_concentradas = [posicao, valor]  # (posição, valor)
    cargas_distribuidas = [dist]  # (início, fim, q em kN/m)

    # Discretização
    x = np.linspace(0, L, NP)
    Q = np.zeros_like(x)
    M = np.zeros_like(x)

    # Cálculo das reações - Exemplo para viga apoiada-apoiada
    RA = sum([P * (L - a) / L for (a, P) in cargas_concentradas])
    RB = sum([P * a / L for (a, P) in cargas_concentradas])
    RA += sum([q * (b - a) * (L - (a + (b - a)/2)) / L for (a, b, q) in cargas_distribuidas])
    RB += sum([q * (b - a) * ((a + (b - a)/2)) / L for (a, b, q) in cargas_distribuidas])

    # Cálculo de Q(x) e M(x)
    for i, xi in enumerate(x):
        Q[i] += RA
        M[i] += RA * xi
        for (a, P) in cargas_concentradas:
            if xi >= a:
                Q[i] -= P
                M[i] -= P * (xi - a)
        for (a, b, q) in cargas_distribuidas:
            if xi >= a and xi <= b:
                Q[i] -= q * (xi - a)
                M[i] -= q * (xi - a)**2 / 2
            elif xi > b:
                Q[i] -= q * (b - a)
                M[i] -= q * (b - a) * (xi - (a + b)/2)

    # Gráficos
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, Q)
    plt.title("Esforço Cortante Q(x)")
    plt.xlabel("x [m]")
    plt.ylabel("Q(x) [kN]")

    plt.subplot(1, 2, 2)
    plt.plot(x, M)
    plt.title("Momento Fletor M(x)")
    plt.xlabel("x [m]")
    plt.ylabel("M(x) [kN.m]")
    plt.tight_layout()
    #plt.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)



    output = [buf, "grafico.png"]

    return output