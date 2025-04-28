# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:56:30 2025

@author: jeffe
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def calcula(comprimento, posicao, valor, dist):
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

    # Relatório
    print("=========== MEMORIAL DE CÁLCULO ===========")
    print(f"Viga {tipo_viga.capitalize()}")
    print(f"L = {L} m")
    print("Cargas Concentradas:")
    for pos, val in cargas_concentradas:
        print(f" - {val} kN em x = {pos} m")
    print("Cargas Distribuídas:")
    for a, b, q in cargas_distribuidas:
        print(f" - {q} kN/m de x = {a} até x = {b}")
    print(f"Reações: RA = {RA:.2f} kN, RB = {RB:.2f} kN")
    print(f"Q(x): min = {min(Q):.2f} kN, max = {max(Q):.2f} kN")
    print(f"M(x): min = {min(M):.2f} kN.m, max = {max(M):.2f} kN.m")

    return buf.getvalue()