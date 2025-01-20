"""
EN ESTE PROGRAMA SE ELIMINAN DEL EXCEL "DatosPruebas2.xlsx"
LOS DATOS DE LAS PRUEBAS QUE SE ENCUENTRAN FUERA DEL RANGO [1 mes antes DX1, DX2]:

Tiempo ejecución: < 1 min.

Programa anterior a ejecutar: "_4_grupos_pacientes.py"
Programa siguiente a ejecutar: "_1d_quitar_pruebas_insuficientes.py"
"""


import os
import pandas as pd
import _1a_bis_pacientes_excluidos
import math

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

datosPruebas = pd.read_excel(os.path.join(datosDir, 'DatosPruebas2.xlsx'))
datosAnaliticas = pd.read_csv(os.path.join(datosDir, 'AnaliticasPacientes.csv'))

dataOUT = {'IDPaciente': [], 'NumSolicitud': [], 'Prueba': [], 'FRealizacion': [], 'Resultado': [], 'Unidades': []}


solicitudes = []
for i in range(1, 575):
    if i not in _1a_bis_pacientes_excluidos.IDexcluidos:
        solicitudesPaciente = datosAnaliticas[str(i)]
        for sol in solicitudesPaciente:
            if isinstance(sol, (int, float)) and not math.isnan(sol):
                solicitudes.append(int(sol))
            else:
                break


pacienteID, numSolicitud, tipoPrueba, fechaPrueba, resPrueba, udsPrueba \
    = datosPruebas['IDPaciente'], datosPruebas['NumSolicitud'], datosPruebas['Prueba'], \
    datosPruebas['FRealizacion'], datosPruebas['Resultado'], datosPruebas['Unidades']


for i in range(len(pacienteID)):

    if int(numSolicitud[i]) in solicitudes:
        dataOUT['IDPaciente'].append(pacienteID[i])
        dataOUT['NumSolicitud'].append(numSolicitud[i])
        dataOUT['Prueba'].append(tipoPrueba[i])
        dataOUT['FRealizacion'].append(fechaPrueba[i])
        dataOUT['Resultado'].append(resPrueba[i])
        dataOUT['Unidades'].append(udsPrueba[i])

nuevoExcel = os.path.join(datosDir, 'DatosPruebas1c.xlsx')
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True)







