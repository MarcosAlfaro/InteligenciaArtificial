import pandas as pd
import numpy as np
import random
import csv
import os


def crear_fila_csv(vector, writer):
    fila = []
    for elemento in range(1, len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


datosDir = "DATOS"


numPacientesGenerados = 280

datosVectores = pd.read_csv(os.path.join(datosDir, "VectoresPacientes.csv"))
# datosVectores = pd.read_csv("VectoresPacientesDA.csv")

pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'LDH', 'Creatinina']

pruebasOUT = ['ComponenteMonoclonal', 'RatioKappaLambda', 'IgA', 'IgG', 'IgM', 'ProteinasTotales',
              'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
              'Albumina', 'Calcio', 'LDH', 'Creatinina']

"""
pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'Proteina C reactiva', 'VSG', 'LDH', 'Creatinina', 'Beta-2 microglobulina']
"""

vectoresPacientes = []
vectoresPositivos = []
IDPositivos = []

indicesPruebasCorreladas = [0, 1, 2, 4, 8, 9]

for i in range(len(datosVectores['IDPaciente'])):
    vectorPaciente = [datosVectores["IDPaciente"][i]]
    # vectorPaciente = []
    cont = 0
    for j in range(len(pruebas)):
        if cont in indicesPruebasCorreladas:
            vectorPaciente.append(datosVectores[pruebas[j] + " Ultimo valor"][i])
        cont += 1
        if cont in indicesPruebasCorreladas:
            vectorPaciente.append(datosVectores[pruebas[j] + " Tendencia"][i])
        cont += 1
    # vectorPaciente.append(datosVectores["Edad"][i])
    # vectorPaciente.append(datosVectores["IgG/No IgG"][i])
    vectorPaciente.append(int(datosVectores["DX2"][i]))
    vectoresPacientes.append(vectorPaciente)
    if datosVectores["DX2"][i] == 1:
        vectoresPositivos.append(vectorPaciente)
        IDPositivos.append(datosVectores["IDPaciente"][i])

numPositivos = len(vectoresPositivos)
pacientesGenerados, IDPacienteOriginal = [], []
for i in range(numPacientesGenerados):
    idxVector = np.random.choice(np.arange(numPositivos), 1,
                                 p=1 / numPositivos * np.ones(numPositivos))[0]
    vectorOriginal = vectoresPositivos[idxVector][:]
    vectorGenerado = vectorOriginal[:]
    vectorGenerado[0] = str(i+1) + "bis"
    for j in range(1, len(vectorOriginal)-1):
        noise = np.random.normal(loc=0.0, scale=0.05) * vectorOriginal[j]
        vectorGenerado[j] = vectorOriginal[j] + noise
    pacientesGenerados.append(vectorGenerado)
    IDPacienteOriginal.append(vectorOriginal[0])


pacientesTotales = vectoresPacientes + pacientesGenerados

for c in range(1, len(pacientesTotales[0])-1):
    max, min = -100000, 100000

    for i in range(len(pacientesTotales)):
        if pacientesTotales[i][c] > max:
            max = pacientesTotales[i][c]
        if pacientesTotales[i][c] < min:
            min = pacientesTotales[i][c]
    """
    max = np.max(pacientesTotales[:, c])
    min = np.min(pacientesTotales[:, c])
    """
    for i in range(len(pacientesTotales)):
        pacientesTotales[i][c] = -1 + 2*(pacientesTotales[i][c]-min)/(max - min)


with open(os.path.join(datosDir, 'VectoresPacientesTodos.csv'), 'w', newline='') as file1:
    writer1 = csv.writer(file1)
    # lineaTituloColumnas = ["IDPaciente"]
    lineaTituloColumnas = []
    cont = 0
    for prueba in range(len(pruebas)):
        if cont in indicesPruebasCorreladas:
            lineaTituloColumnas.append(pruebasOUT[prueba] + "UltimoValor")
        cont += 1
        if cont in indicesPruebasCorreladas:
            lineaTituloColumnas.append(pruebasOUT[prueba] + "Tendencia")
        cont += 1
    # lineaTituloColumnas.append("Edad")
    # lineaTituloColumnas.append("IgGNoIgG")
    lineaTituloColumnas.append("DX2")

    writer1.writerow(lineaTituloColumnas)

    for i in range(len(vectoresPacientes)):
        crear_fila_csv(vectoresPacientes[i], writer1)

    for i in range(len(pacientesGenerados)):
        crear_fila_csv(pacientesGenerados[i], writer1)
