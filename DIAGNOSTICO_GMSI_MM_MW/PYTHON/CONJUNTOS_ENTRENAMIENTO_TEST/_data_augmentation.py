"""
EN ESTE PROGRAMA SE REALIZAN LAS SIGUIENTES TAREAS:

1. DATA AUGMENTATION DE PACIENTES POSITIVOS (N=200)
- Los pacientes se generan introduciendo un ruido gaussiano de sigma = 3%
  sobre los vectores de características de los pacientes positivos

2. NORMALIZACIÓN DE LOS DATOS
- Los vectores de características de todos los pacientes (originales y aumentados) se normalizan entre -1 y +1

Tiempo ejecución: 0

Programa anterior a ejecutar: "_7_datos_clasificador_v2.py"
"""


import pandas as pd
import numpy as np
import csv
import os


def crear_fila_csv(vector):
    fila = []
    for elemento in range(1, len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")


numPacientesGenerados = 280

datosVectores = pd.read_csv(os.path.join(datosDir, "VectoresPacientes.csv"))
# datosVectores = pd.read_csv("VectoresPacientesDA.csv")
"""
pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Ratio Neutrofilos/Linfocitos', 'Ratio Plaquetas/Linfocitos', 'Ratio Monocitos/Linfocitos',
           'Albumina', 'Calcio', 'Proteina C reactiva', 'VSG', 'LDH',
           'Creatinina', 'Ratio Creatinina/Hemoglobina', 'Beta-2 microglobulina']

"""
pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'LDH', 'Creatinina']

pruebasOUT = ['ComponenteMonoclonal', 'RatioKappaLambda', 'IgA', 'IgG', 'IgM', 'ProteinasTotales',
              'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
              'Albumina', 'Calcio', 'LDH', 'Creatinina']


vectoresPacientes = []
vectoresPositivos = []
for i in range(len(datosVectores['IDPaciente'])):
    vectorPaciente = [datosVectores["IDPaciente"][i]]
    for j in range(len(pruebas)):
        vectorPaciente.append(datosVectores[pruebas[j] + " Ultimo valor"][i])
        vectorPaciente.append(datosVectores[pruebas[j] + " Tendencia"][i])
    vectorPaciente.append(datosVectores["Edad"][i])
    vectorPaciente.append(datosVectores["IgG/No IgG"][i])
    vectorPaciente.append(datosVectores["DX2"][i])
    vectoresPacientes.append(vectorPaciente)
    if datosVectores["DX2"][i] == 1:
        vectoresPositivos.append(vectorPaciente)


numPositivos = len(vectoresPositivos)
pacientesGenerados = []
for i in range(numPacientesGenerados):
    idxVector = np.random.choice(np.arange(numPositivos), 1,
                                 p=1 / numPositivos * np.ones(numPositivos))[0]
    vectorOriginal = vectoresPositivos[idxVector][:]
    vectorGenerado = vectorOriginal[:]
    vectorGenerado[0] = str(i+1) + "bis"
    for j in range(1, len(vectorOriginal)-2):
        noise = np.random.normal(loc=0.0, scale=0.05) * vectorOriginal[j]
        vectorGenerado[j] = vectorOriginal[j] + noise
    pacientesGenerados.append(vectorGenerado)


pacientesTotales = vectoresPacientes + pacientesGenerados

for c in range(1, len(pacientesTotales[0])-2):
    max, min = -100000, 100000

    for i in range(len(pacientesTotales)):
        if pacientesTotales[i][c] > max:
            max = pacientesTotales[i][c]
        if pacientesTotales[i][c] < min:
            min = pacientesTotales[i][c]

    for i in range(len(pacientesTotales)):
        pacientesTotales[i][c] = -1 + 2*(pacientesTotales[i][c]-min)/(max-min)


with open(os.path.join(datosDir, 'VectoresPacientesDA.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    # lineaTituloColumnas = ["IDPaciente"]
    lineaTituloColumnas = []
    for prueba in range(len(pruebasOUT)):
        lineaTituloColumnas.append(pruebasOUT[prueba] + "UltimoValor")
        lineaTituloColumnas.append(pruebasOUT[prueba] + "Tendencia")
    lineaTituloColumnas.append("Edad")
    lineaTituloColumnas.append("IgGNoIgG")
    lineaTituloColumnas.append("DX2")

    writer.writerow(lineaTituloColumnas)

    for i in range(len(vectoresPacientes)):
        crear_fila_csv(vectoresPacientes[i])
    for i in range(len(pacientesGenerados)):
        crear_fila_csv(pacientesGenerados[i])
