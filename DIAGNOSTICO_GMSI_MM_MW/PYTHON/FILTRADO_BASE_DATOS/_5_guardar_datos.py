"""
EN ESTE PROGRAMA SE GUARDAN LOS DATOS DE LAS PRUEBAS REALIZADAS EN UN ARRAY 3D:
-dimensión 1: índice de analítica
-dimensión 2: prueba
-dimensión 3: ID paciente


Tiempo ejecución: 0

Programa anterior a ejecutar: "_1d_quitar_pruebas_irrelevantes.py"
Programa siguiente a ejecutar: "_6_completar_datos.py"
"""


import pandas as pd
import numpy as np
import _1a_bis_pacientes_excluidos
import csv
import os


def crear_fila_csv(ID, prueba, datosFila):
    fila = [ID, prueba]
    for num in range(maxNumAnaliticas):
        fila.append(datosFila[num])
    writer.writerow(fila)
    return


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")


pruebas = ['Componente monoclonal', 'Ratio K/L', 'IgA', 'IgG', 'IgM', 'Proteinas totales', 'Hemoglobina', 'VCM',
           'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos', 'Albumina', 'Calcio', 'LDH',
           'Creatinina']

nombresPruebas = [['Monoclonales (V. Absoluto)'], ['X'], ['IgA'], ['IgG'], ['IgM'], ['Proteínas totales'],
                  ['Hemoglobina'], ['Volumen corpuscular medio'], ['Leucocitos'], ['Plaquetas'],
                  ['Neutrofilos (V. Absoluto)'], ['Monocitos (V. Absoluto)'], ['Linfocitos (V. Absoluto)'],
                  ['Albúmina'], ['Calcio'], ['LDH'], ['Creatinina']]


datosPruebas = pd.read_excel(os.path.join(datosDir, 'DatosPruebas1d.xlsx'))
datosPacientes = pd.read_excel(os.path.join(datosDir, 'DatosPacientes.xlsx'))
datosAnaliticas = pd.read_csv(os.path.join(datosDir, 'AnaliticasPacientes.csv'))

PR_Prueba, PR_Resultado, PR_Fecha, PR_Solicitud, PR_IDPaciente = \
    datosPruebas['Prueba'], datosPruebas['Resultado'], datosPruebas['FRealizacion'], \
    datosPruebas['NumSolicitud'], datosPruebas['IDPaciente']

PA_IDPaciente, PA_NumAnaliticas, PA_DX2, PA_FechaDX1 \
    = datosPacientes['IDPaciente'], datosPacientes['N. Analiticas'], datosPacientes['DX2'], datosPacientes['Fecha DX1']

maxNumAnaliticas = max(PA_NumAnaliticas)

dimensiones = (maxNumAnaliticas, len(pruebas), 575)
resultadosPruebas = np.zeros(dimensiones)
fechasPruebas = np.zeros(dimensiones)

fechasDX1 = []
for i in range(575):
    fechasDX1.append([])
for i in range(len(PA_FechaDX1)):
    fechasDX1[int(PA_IDPaciente[i])].append(PA_FechaDX1[i])

datos = np.zeros(len(pruebas))
datoPorcentajeCM, datoKappa, datoLambda = 0, 0, 0
# datos[pruebas.index("Albumina")] = PR_Resultado[0]

solicitudAntigua, pacienteAntiguo = int(PR_Solicitud[0]), int(PR_IDPaciente[0])
fecha = (PR_Fecha[0] - fechasDX1[pacienteAntiguo][0]).days / 365.25

for i in range(len(PR_Solicitud)):
    paciente, solicitud = int(PR_IDPaciente[i]), int(PR_Solicitud[i])

    if solicitud != solicitudAntigua:

        analiticasPaciente = list(datosAnaliticas[str(pacienteAntiguo)])
        idx = analiticasPaciente.index(solicitudAntigua)


        # cálculo CM
        if datoPorcentajeCM != 0 and datos[pruebas.index("Proteinas totales")] != 0:
            datos[pruebas.index("Componente monoclonal")] \
                = datoPorcentajeCM * datos[pruebas.index("Proteinas totales")] / 100

        # ratio K/L
        if datoKappa != 0 and datoLambda != 0:
            datos[pruebas.index("Ratio K/L")] = datoKappa / datoLambda

        # calcio ajustado por albúmina
        if datos[pruebas.index("Albumina")] != 0 and datos[pruebas.index("Calcio")] != 0:
            datos[pruebas.index("Calcio")] += 0.8 * (4 - datos[pruebas.index("Albumina")])

        for p in range(len(pruebas)):
            if datos[p] != 0:
                resultadosPruebas[idx][p][pacienteAntiguo] = datos[p]
            fechasPruebas[idx][p][pacienteAntiguo] = fecha

        fecha = (PR_Fecha[i] - fechasDX1[paciente][0]).days / 365.25

        datos = np.zeros(len(pruebas))
        datoPorcentajeCM, datoKappa, datoLambda = 0, 0, 0

    solicitudAntigua = solicitud
    pacienteAntiguo = paciente

    flag = False
    for p in range(len(nombresPruebas)):
        for nombre in nombresPruebas[p]:
            if nombre in PR_Prueba[i]:
                datos[p] = PR_Resultado[i]
                flag = True
                break
        if flag:
            break
    if "Monoclonales" in PR_Prueba[i]:
        datoPorcentajeCM = PR_Resultado[i]
    if 'CADENAS KAPPA LIBRE EN SUERO' in PR_Prueba[i] or 'CADENA KAPPA LIBRE EN SUERO' in PR_Prueba[i] \
            or 'Cadenas ligeras Kappa' in PR_Prueba[i]:
        datoKappa = PR_Resultado[i]
    if 'CADENAS LAMBDA LIBRE EN SUERO' in PR_Prueba[i] or 'CADENA LAMBDA LIBRE EN SUERO' in PR_Prueba[i] \
            or 'Cadenas ligeras Lambda' in PR_Prueba[i]:
        datoLambda = PR_Resultado[i]
    # fecha = (PR_Fecha[i] - fechasDX1[paciente][0]).days / 365.25


with open(os.path.join(datosDir, 'DatosGraficas.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IDPaciente", "Prueba"]+[str(i) for i in range(maxNumAnaliticas)])

    for i in range(1, 575):
        if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
            for p in range(len(pruebas)):
                crear_fila_csv(i, pruebas[p], resultadosPruebas[:, p, i])

with open(os.path.join(datosDir, 'FechasGraficas.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IDPaciente", "Prueba"]+[str(i) for i in range(maxNumAnaliticas)])

    for i in range(1, 575):
        if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
            for p in range(len(pruebas)):
                crear_fila_csv(i, pruebas[p], fechasPruebas[:, p, i])
