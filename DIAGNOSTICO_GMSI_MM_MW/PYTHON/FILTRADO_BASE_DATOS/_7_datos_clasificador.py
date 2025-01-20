"""
EN ESTE PROGRAMA SE OBTIENEN LOS VECTORES DE CARACTERÍSTICAS DE LOS PACIENTES VÁLIDOS

Cada vector contiene las siguientes características:
-Para cada prueba, se obtiene el último valor y la tendencia en el último año
- Edad (años)
- Tipo IgG/no IgG (0: IgG, 1: no IgG)
- SALIDA: diagnóstico DX2 (0: negativo, 1: positivo)

Los pacientes válidos son aquellos que tengan al menos dos analíticas válidas realizadas

Tiempo ejecución: 0

Programa anterior a ejecutar: "_6_completar_datos.py"
Programa siguiente a ejecutar: "_8_data_augmentation.py"
"""


import pandas as pd
import numpy as np
import _1a_bis_pacientes_excluidos
import csv
import os


def crear_fila_csv(id, vector):
    fila = [id]
    for elemento in range(len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")


datosPacientes = pd.read_excel(os.path.join(datosDir, 'DatosPacientes.xlsx'))

PA_IDPaciente, PA_FechaDX1, PA_FechaNacimiento, PA_Grupo, PA_DX2, PA_numAnaliticas = \
    datosPacientes['IDPaciente'], datosPacientes['Fecha DX1'], datosPacientes['Fecha Nacimiento'], \
    datosPacientes['Grupo'], datosPacientes['DX2'], datosPacientes['N. Analiticas']


datosGraficas = pd.read_csv(os.path.join(datosDir, "DatosGraficasCompleto.csv"), encoding='latin1')
fechasGraficas = pd.read_csv(os.path.join(datosDir, "FechasGraficasCompleto.csv"), encoding='latin1')

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


numAnaliticas = max(PA_numAnaliticas)
dimensiones = (numAnaliticas, len(pruebas), 575)
resultadosPruebas = np.zeros(dimensiones)
fechasPruebas = np.zeros(dimensiones)
pacientesValidos = 0


for i in range(len(datosGraficas['IDPaciente'])):
    IDPaciente = int(datosGraficas['IDPaciente'][i])
    for j in range(numAnaliticas):
        resultadosPruebas[j][i % len(pruebas)][IDPaciente] = datosGraficas[str(j)][i]
        fechasPruebas[j][i % len(pruebas)][IDPaciente] = fechasGraficas[str(j)][i]

lenVector = 2 * len(pruebas) + 3

with open(os.path.join(datosDir, 'VectoresPacientes.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    lineaTituloColumnas = ["IDPaciente"]
    for prueba in range(len(pruebas)):
        lineaTituloColumnas.append(pruebas[prueba] + " Ultimo valor")
        lineaTituloColumnas.append(pruebas[prueba] + " Tendencia")
    lineaTituloColumnas.append("Edad")
    lineaTituloColumnas.append("IgG/No IgG")
    lineaTituloColumnas.append("DX2")

    writer.writerow(lineaTituloColumnas)
    vectoresPacientes = [np.zeros(lenVector)]

    for ID in range(1, 575):
        if ID in _1a_bis_pacientes_excluidos.IDexcluidos:
            vectoresPacientes.append(np.zeros(lenVector))
        else:

            # si el paciente no tiene ninguna analítica realizada se descarta
            if np.any(resultadosPruebas[0, :, ID] == 0):
                vectoresPacientes.append(np.zeros(lenVector))

            else:
                N = np.where(resultadosPruebas[:, prueba, ID] != 0)[0][-1]

                # si el paciente tiene solo una analítica realizada se descarta
                if N < 1:
                    vectoresPacientes.append(np.zeros(lenVector))
                    print(ID)

                # si el paciente tiene al menos dos analíticas realizadas
                # el paciente es válido y se obtiene su vector de características
                else:
                    idx = list(PA_IDPaciente).index(ID)
                    pacientesValidos += 1
                    vectorPaciente = np.zeros(lenVector)

                    for idxPrueba1year in reversed(range(N)):
                        if fechasPruebas[idxPrueba1year][0][ID] + 1 < fechasPruebas[N][0][ID]:
                            break

                    for prueba in range(len(pruebas)):
                        vectorPaciente[2 * prueba] = resultadosPruebas[N][prueba][ID]

                        fec1year = fechasPruebas[N][prueba][ID] - 1
                        if fec1year > 0:
                            res1year = \
                                resultadosPruebas[idxPrueba1year][prueba][ID] + \
                                (fec1year - fechasPruebas[idxPrueba1year][prueba][ID]) * \
                                (resultadosPruebas[idxPrueba1year + 1][prueba][ID] -
                                 resultadosPruebas[idxPrueba1year][prueba][ID]) / \
                                (fechasPruebas[idxPrueba1year + 1][prueba][ID] -
                                 fechasPruebas[idxPrueba1year][prueba][ID] + 0.001)

                            vectorPaciente[2 * prueba + 1] = \
                                resultadosPruebas[N][prueba][ID] - resultadosPruebas[idxPrueba1year][prueba][ID]
                        else:
                            vectorPaciente[2 * prueba + 1] = \
                                (resultadosPruebas[N][prueba][ID] - resultadosPruebas[0][prueba][ID]) / \
                                (fechasPruebas[N][prueba][ID] - fechasPruebas[0][prueba][ID])

                    if ID == 573:
                        vectorPaciente[-3] = 74.55
                    else:
                        vectorPaciente[-3] = (PA_FechaDX1[idx] - PA_FechaNacimiento[idx]).days/365.25 + \
                                         fechasPruebas[N][0][ID]

                    if 'IgG' in PA_Grupo[idx]:
                        vectorPaciente[-2] = 0
                    else:
                        vectorPaciente[-2] = 1

                    vectorPaciente[-1] = PA_DX2[idx]

                    vectoresPacientes.append(vectorPaciente)

                    crear_fila_csv(ID, vectorPaciente)

print(f"Pacientes válidos: {pacientesValidos}")
