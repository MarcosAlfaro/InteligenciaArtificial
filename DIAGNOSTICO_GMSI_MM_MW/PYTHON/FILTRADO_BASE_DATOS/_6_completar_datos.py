"""
EN ESTE PROGRAMA SE COMPLETAN LOS DATOS DE LAS PRUEBAS REALIZADAS MEDIANTE INTERPOLACIÓN Y EXTRAPOLACIÓN LINEAL:
-dimensión 1: índice de analítica
-dimensión 2: prueba
-dimensión 3: ID paciente

Además, se indican los pacientes que no son válidos

Tiempo ejecución: 0

Programa anterior a ejecutar: "_5_guardar_datos.py"
Programa siguiente a ejecutar: "_7_datos_clasificador_v2.py"
"""


import pandas as pd
import numpy as np
import os
import csv
import _1a_bis_pacientes_excluidos


def crear_fila_csv(id, prueba, datos):
    fila = [id, prueba]
    for num in range(numAnaliticas):
        fila.append(datos[num])
    # print(fila)
    writer.writerow(fila)
    return


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

datosPacientes = pd.read_excel(os.path.join(datosDir, 'DatosPacientes.xlsx'))
datosGraficas = pd.read_csv(os.path.join(datosDir, "DatosGraficas.csv"), encoding='latin1')
fechasGraficas = pd.read_csv(os.path.join(datosDir, "FechasGraficas.csv"), encoding='latin1')

PA_NumAnaliticas = datosPacientes['N. Analiticas']
numAnaliticas = max(PA_NumAnaliticas)

pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'LDH', 'Creatinina']

dimensiones = (numAnaliticas, len(pruebas), 575)
resultadosPruebas = np.zeros(dimensiones)
fechasPruebas = np.zeros(dimensiones)

for i in range(len(datosGraficas['IDPaciente'])):
    IDPaciente = int(datosGraficas['IDPaciente'][i])
    for j in range(numAnaliticas):
        resultadosPruebas[j][i % len(pruebas)][IDPaciente] = datosGraficas[str(j)][i]
        fechasPruebas[j][i % len(pruebas)][IDPaciente] = fechasGraficas[str(j)][i]

pruebasVacias = np.zeros(len(pruebas))
pacientesFaltaPruebas = []

for ID in range(1, 575):
    if ID not in _1a_bis_pacientes_excluidos.IDexcluidos:
        for sol in range(numAnaliticas):
            if not np.any(resultadosPruebas[sol, :, ID] != 0):
                break
        N = sol - 1

        # AÑADIR FECHA PRUEBAS A CADA ANALÍTICA
        for sol in range(N+1):
            for prueba in range(len(pruebas)):
                if fechasPruebas[sol][prueba][ID] != 0.0:
                    for p in range(len(pruebas)):
                        fechasPruebas[sol][p][ID] = fechasPruebas[sol][prueba][ID]
                    break

        for prueba in range(len(pruebas)):

            cont0 = np.count_nonzero(resultadosPruebas[:, prueba, ID])

            # si al paciente no se le ha realizado ninguna analítica con esta prueba, el paciente no es válido
            if cont0 == 0:
                print(f"ID{ID}, Prueba:{pruebas[prueba]}")
                if ID not in pacientesFaltaPruebas:
                    pacientesFaltaPruebas.append(ID)
                pruebasVacias[prueba] += 1

            # si al paciente solo se le ha realizado una analítica con esta prueba
            # se completa el vector de datos para dicha prueba con el único valor disponible
            elif cont0 == 1:
                idx = np.where(resultadosPruebas[:, prueba, ID] != 0)[0][0]
                for i in range(N+1):
                    resultadosPruebas[i][prueba][ID] = resultadosPruebas[idx][prueba][ID]

            # si al paciente se le han realizado varias analíticas con esta prueba
            # se completa el vector de datos para dicha prueba mediante interpolación lineal
            # con la restricción de que los valores no pueden ser negativos
            else:

                nonZeroValues = np.where(resultadosPruebas[:, prueba, ID] != 0)[0]
                for x in range(len(nonZeroValues)-1):
                    i = nonZeroValues[x]
                    j = nonZeroValues[x+1]

                    # interpolación
                    for k in range(i+1, j):
                        if resultadosPruebas[k][prueba][ID] == 0:
                            resultadosPruebas[k][prueba][ID] = \
                                resultadosPruebas[i][prueba][ID] + \
                                (fechasPruebas[k][prueba][ID] - fechasPruebas[i][prueba][ID]) * \
                                (resultadosPruebas[j][prueba][ID] - resultadosPruebas[i][prueba][ID]) / \
                                (fechasPruebas[j][prueba][ID] - fechasPruebas[i][prueba][ID] + 0.001)

                i = nonZeroValues[0]
                j = nonZeroValues[1]
                # extrapolación para valores previos al primer valor
                for k in reversed(range(i)):
                    resultadosPruebas[k][prueba][ID] = \
                        resultadosPruebas[i][prueba][ID] - \
                        (resultadosPruebas[j][prueba][ID] - resultadosPruebas[i][prueba][ID]) * \
                        (fechasPruebas[i][prueba][ID] - fechasPruebas[k][prueba][ID]) / \
                        (fechasPruebas[j][prueba][ID] - fechasPruebas[i][prueba][ID] + 0.001)

                    if resultadosPruebas[k][prueba][ID] < 0:
                        resultadosPruebas[k][prueba][ID] = resultadosPruebas[k+1][prueba][ID]

                i = nonZeroValues[-2]
                j = nonZeroValues[-1]
                # extrapolación para valores posteriores al último valor
                for k in (range(j+1, N+1)):
                    resultadosPruebas[k][prueba][ID] = \
                        resultadosPruebas[j][prueba][ID] + \
                        (resultadosPruebas[j][prueba][ID] - resultadosPruebas[i][prueba][ID]) * \
                        (fechasPruebas[k][prueba][ID] - fechasPruebas[i][prueba][ID]) / \
                        (fechasPruebas[j][prueba][ID] - fechasPruebas[i][prueba][ID] + 0.001)

                    if resultadosPruebas[k][prueba][ID] < 0:
                        resultadosPruebas[k][prueba][ID] = resultadosPruebas[k-1][prueba][ID]

print(f"Pacientes con falta de 1 o + pruebas: {pacientesFaltaPruebas}")
print(f"Num. pacientes: {len(pacientesFaltaPruebas)}")

for p in range(len(pruebas)):
    print(f"{pruebas[p]}: {pruebasVacias[p]}")


with open(os.path.join(datosDir, 'DatosGraficasCompleto.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IDPaciente", "Prueba"] + [str(i) for i in range(numAnaliticas)])

    for i in range(1, 575):
        if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
            for j in range(len(pruebas)):
                crear_fila_csv(i, pruebas[j], resultadosPruebas[:, j, i])


with open(os.path.join(datosDir, 'FechasGraficasCompleto.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IDPaciente", "Prueba"] + [str(i) for i in range(numAnaliticas)])

    for i in range(1, 575):
        if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
            for j in range(len(pruebas)):
                crear_fila_csv(i, pruebas[j], fechasPruebas[:, j, i])
