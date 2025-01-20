import pandas as pd
import numpy as np
import csv
import os


def crear_fila_csv(vector, writer):
    fila = []
    for elemento in range(len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


datosDir = "DATOS"


numPacientesGenerados = 40

datosVectores = pd.read_csv(os.path.join(datosDir, "VectoresPacientes.csv"))

pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'LDH', 'Creatinina']

pruebasOUT = ['ComponenteMonoclonal', 'RatioKappaLambda', 'IgA', 'IgG', 'IgM', 'ProteinasTotales',
              'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
              'Albumina', 'Calcio', 'LDH', 'Creatinina']


# ESCRIBIR LOS VECTORES DE LOS PACIENTES
vectoresPacientes = []
vectoresPositivos = []
IDPositivos = []
for i in range(len(datosVectores['IDPaciente'])):
    vectorPaciente = [str(datosVectores["IDPaciente"][i])]
    for j in range(len(pruebas)):
        vectorPaciente.append(datosVectores[pruebas[j] + " Ultimo valor"][i])
        vectorPaciente.append(datosVectores[pruebas[j] + " Tendencia"][i])
    vectorPaciente.append(datosVectores["Edad"][i])
    vectorPaciente.append(datosVectores["IgG/No IgG"][i])
    vectorPaciente.append(int(datosVectores["DX2"][i]))
    vectoresPacientes.append(vectorPaciente)
    if datosVectores["DX2"][i] == 1:
        vectoresPositivos.append(vectorPaciente)
        IDPositivos.append(str(datosVectores["IDPaciente"][i]))


desviaciones = [0]
for c in range(1, len(vectoresPacientes[0])-2):
    valores = []
    for i in range(len(vectoresPacientes)):
        valores.append(vectoresPacientes[i][c])

    avg = np.average(valores)
    desv = np.std(valores)
    desviaciones.append(desv)

# DATA AUGMENTATION
numPositivos = len(vectoresPositivos)
pacientesGenerados = []
for ID in IDPositivos:
    for i in range(numPacientesGenerados):
        idxVector = IDPositivos.index(ID)
        vectorOriginal = vectoresPositivos[idxVector][:]
        vectorGenerado = vectorOriginal[:]
        vectorGenerado[0] = str(ID) + "bis" + str(i+1)
        for j in range(1, len(vectorOriginal)-2):
            noise = np.random.normal(loc=0.0, scale=0.10) * desviaciones[j]
            vectorGenerado[j] = vectorOriginal[j] + noise
        pacientesGenerados.append(vectorGenerado)

pacientesTotales = vectoresPacientes + pacientesGenerados

# NORMALIZACIÓN
for c in range(1, len(pacientesTotales[0])-2):
    max, min = -100000, 100000
    valores = []
    for i in range(len(pacientesTotales)):
        valores.append(pacientesTotales[i][c])
        if pacientesTotales[i][c] > max:
            max = pacientesTotales[i][c]
        if pacientesTotales[i][c] < min:
            min = pacientesTotales[i][c]

    avg = np.average(valores)
    desv = np.std(valores)
    for i in range(len(pacientesTotales)):
        pacientesTotales[i][c] = -1 + 2*(pacientesTotales[i][c]-min)/(max - min)
        # pacientesTotales[i][c] = (pacientesTotales[i][c] - avg) / desv


numPacientesNegativos = len(pacientesTotales) - len(IDPositivos)
conjuntos = []
for _ in range(len(IDPositivos)):
    conjuntos.append([])
cont = 0
for i in range(len(pacientesTotales)):
    if pacientesTotales[i][-1] == 0:
        conjuntos[i % 7].append(pacientesTotales[i])
    else:
        if "bis" in pacientesTotales[i][0]:
            ID, _ = pacientesTotales[i][0].split("bis")
        else:
            ID = pacientesTotales[i][0]
        idxPos = IDPositivos.index(ID)
        conjuntos[idxPos].append(pacientesTotales[i])


for i in range(len(IDPositivos)):
    with open(os.path.join(datosDir, 'GrupoID' + IDPositivos[i] + '.csv'), 'w', newline='') as file:
        writer = csv.writer(file)

        lineaTituloColumnas = ["IDPaciente"]
        for prueba in range(len(pruebas)):
            lineaTituloColumnas.append(pruebasOUT[prueba] + "UltimoValor")
            lineaTituloColumnas.append(pruebasOUT[prueba] + "Tendencia")
        lineaTituloColumnas.append("Edad")
        lineaTituloColumnas.append("IgGNoIgG")
        lineaTituloColumnas.append("DX2")
        writer.writerow(lineaTituloColumnas)

        for paciente in conjuntos[i]:
            crear_fila_csv(paciente, writer)

