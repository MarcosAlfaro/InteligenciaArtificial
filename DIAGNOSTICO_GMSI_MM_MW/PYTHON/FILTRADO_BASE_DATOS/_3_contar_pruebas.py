"""
EN ESTE PROGRAMA SE REALIZAN LAS SIGUIENTES TAREAS:
1. SE OBTIENEN LAS ANALÍTICAS DE CADA PACIENTE (TOTALES Y ANALÍTICAS CON PRUEBA DE COMPONENTE MONOCLONAL)
2. SE ORDENAN CRONOLÓGICAMENTE LAS ANALÍTICAS
3. SE ELIMINAN LAS PRUEBAS REALIZADAS FUERA DEL RANGO [1 mes antes DX1, DX2]
4. SE CREAN 2 CSV CON LOS NÚMEROS DE SOLICITUD DE LAS ANALÍTICAS REALIZADAS A CADA PACIENTE ORDENADAS (TOTALES Y CON CM)
5. SE CREA EL EXCEL "DatosPacientes.xlsx" QUE CONTIENE INFORMACIÓN GENERAL DE CADA PACIENTE

Tiempo ejecución: <1 min.

Programa anterior a ejecutar: "_2_ordenar_pruebas.py"
Programa siguiente a ejecutar: "_4_grupos_pacientes.py"
"""

import os
import pandas as pd
from datetime import timedelta
import csv
import _1a_bis_pacientes_excluidos


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

datosPruebas = pd.read_excel(os.path.join(datosDir, 'DatosPruebas2.xlsx'))
datosPA = pd.read_excel(os.path.join(datosDir, 'PacientesAnonimo.xlsx'))

DP_pacienteID, DP_numSolicitud, DP_tipoPrueba, DP_fechaPrueba \
    = datosPruebas['IDPaciente'], datosPruebas['NumSolicitud'], datosPruebas['Prueba'], datosPruebas['FRealizacion']

PA_DX1, PA_DX2, PA_pacienteID, PA_tipoDX2 \
    = datosPA['Fecha:DX1 (GAMMAPATIA)'], datosPA['FECHA_DX2 (Neoplasia)'],\
    datosPA['IDPaciente'], datosPA['DX2(MM=1;MW=2)']

factoresCM = ['Monoclonal', 'monoclonal', 'MONOCLONAL']


# función para ordenar cronológicamente las analíticas de cada paciente
def ordenar_analiticas(solicitudes, fechas):
    if len(solicitudes) == 0:
        return solicitudes, fechas
    listasOrdenadas = sorted(zip(fechas, solicitudes), key=lambda x: x[0])
    fechas, solicitudes = zip(*listasOrdenadas)
    solicitudes, fechas = list(solicitudes), list(fechas)
    return solicitudes, fechas


# función para eliminar las fechas fuera del rango DX1-DX2/Última prueba
def quitar_fechas(solicitudes, fechas):
    quitarSol, quitarFec = [], []
    for f in range(len(fechas)):
        if fechas[f] + timedelta(days=30) < fechasDX1[i][0] or (tipoDX2[i][0] == 1 and fechas[f] > fechasDX2[i][0]):
            quitarSol.append(solicitudes[f])
            quitarFec.append(fechas[f])
    for sol in quitarSol:
        solicitudes.remove(sol)
    for fec in quitarFec:
        fechas.remove(fec)
    return solicitudes, fechas


def incluir_prueba_csv(solicitudes, fechas, cont):
    fecCSV, solCSV = [], []
    for p in range(1, 575):
        if p not in _1a_bis_pacientes_excluidos.IDexcluidos:
            numAnaliticas = len(solicitudes[p])
            if cont < numAnaliticas:
                fecCSV.append(fechas[p][cont])
                solCSV.append(int(solicitudes[p][cont]))
            else:
                fecCSV.append('')
                solCSV.append('')
    return solCSV, fecCSV


# crear listas donde almacenar la info de cada paciente
analiticasPacientes, analiticasCMPacientes = [], []
fechasAnaliticas, fechasCMAnaliticas = [], []
fechasDX1, fechasDX2 = [], []
tipoDX2 = []
for i in range(575):
    analiticasPacientes.append([])
    analiticasCMPacientes.append([])
    fechasAnaliticas.append([])
    fechasCMAnaliticas.append([])
    fechasDX1.append([])
    fechasDX2.append([])
    tipoDX2.append([])


# añadir fechas DX1 y DX2 de cada paciente a listas
for i in range(len(PA_DX1)):

    fechasDX1[int(PA_pacienteID[i])].append(PA_DX1[i].to_pydatetime())

    if PA_tipoDX2[i] == 1 or PA_tipoDX2[i] == 2:
        fechasDX2[int(PA_pacienteID[i])].append(PA_DX2[i].to_pydatetime())
        tipoDX2[int(PA_pacienteID[i])].append(1)
    else:
        fechasDX2[int(PA_pacienteID[i])].append('')
        tipoDX2[int(PA_pacienteID[i])].append(0)


# añadir num solicitud y fechas de analíticas (totales y con prueba CM) a listas
for i in range(len(DP_pacienteID)):
    if not int(DP_pacienteID[i]) in _1a_bis_pacientes_excluidos.IDexcluidos:

        if not int(DP_numSolicitud[i]) in analiticasPacientes[int(DP_pacienteID[i])]:
            analiticasPacientes[int(DP_pacienteID[i])].append(int(DP_numSolicitud[i]))
            fechasAnaliticas[int(DP_pacienteID[i])].append(DP_fechaPrueba[i].to_pydatetime())

        if any(elemento in DP_tipoPrueba[i] for elemento in factoresCM):
            if not int(DP_numSolicitud[i]) in analiticasCMPacientes[int(DP_pacienteID[i])]:
                analiticasCMPacientes[int(DP_pacienteID[i])].append(int(DP_numSolicitud[i]))
                fechasCMAnaliticas[int(DP_pacienteID[i])].append(DP_fechaPrueba[i].to_pydatetime())


for i in range(1, 575):
    if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
        # ordenar analiticas cronológicamente
        analiticasPacientes[i], fechasAnaliticas[i] \
            = ordenar_analiticas(analiticasPacientes[i], fechasAnaliticas[i])
        analiticasCMPacientes[i], fechasCMAnaliticas[i] \
            = ordenar_analiticas(analiticasCMPacientes[i], fechasCMAnaliticas[i])

        # quitar pruebas fuera del rango DX1-DX2/Última prueba
        analiticasPacientes[i], fechasAnaliticas[i] = quitar_fechas(analiticasPacientes[i], fechasAnaliticas[i])
        analiticasCMPacientes[i], fechasCMAnaliticas[i] = quitar_fechas(analiticasCMPacientes[i], fechasCMAnaliticas[i])

        print(f"Nº analíticas Paciente {i}: {len(fechasAnaliticas[i])}")
        print(f"Nº analíticas Componente Monoclonal Paciente {i}: {len(fechasCMAnaliticas[i])}")

with open(os.path.join(datosDir, 'AnaliticasPacientes.csv'), 'w', newline='') as file1:
    with open(os.path.join(datosDir, 'AnaliticasCMPacientes.csv'), 'w', newline='') as file2:
        IDutilizados = []
        for ID in range(1, 575):
            if ID not in _1a_bis_pacientes_excluidos.IDexcluidos:
                IDutilizados.append(ID)
        writer1 = csv.writer(file1)
        writer1.writerow([str(ID) for ID in IDutilizados])
        writer2 = csv.writer(file2)
        writer2.writerow([str(ID) for ID in IDutilizados])

        numMax = max(len(a) for a in analiticasPacientes)
        numMaxCM = max(len(a) for a in analiticasCMPacientes)

        for a in range(numMax):
            solicitudesCSV, fechasCSV = incluir_prueba_csv(analiticasPacientes, fechasAnaliticas, a)
            writer1.writerow(solicitudesCSV)
            # writer1.writerow(fechasCSV)
        for a in range(numMaxCM):
            solicitudesCSV, fechasCSV = incluir_prueba_csv(analiticasCMPacientes, fechasCMAnaliticas, a)
            writer2.writerow(solicitudesCSV)
            # writer2.writerow(fechasCSV)

dataOUT = {'IDPaciente': [], 'Fecha DX1': [], 'Fecha DX2': [], 'N. Analiticas': [], 'N. Analiticas CM': [], 'DX2': []}

for i in range(1, 575):
    if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
        dataOUT['IDPaciente'].append(i)
        dataOUT['Fecha DX1'].append(fechasDX1[i][0])
        dataOUT['Fecha DX2'].append(fechasDX2[i][0])
        dataOUT['N. Analiticas'].append(len(fechasAnaliticas[i]))
        dataOUT['N. Analiticas CM'].append(len(fechasCMAnaliticas[i]))
        if tipoDX2[i][0] == 1 or tipoDX2[i][0] == 2:
            dataOUT['DX2'].append(1)
        else:
            dataOUT['DX2'].append(0)

nuevoExcel = os.path.join(datosDir, "DatosPacientes.xlsx")
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True)
