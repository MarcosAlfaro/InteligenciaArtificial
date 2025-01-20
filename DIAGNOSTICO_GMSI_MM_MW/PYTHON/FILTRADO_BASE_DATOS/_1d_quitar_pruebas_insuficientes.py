"""
EN ESTE PROGRAMA SE ELIMINAN DEL EXCEL "DatosPruebas1c.xlsx"
LOS DATOS DE LAS PRUEBAS QUE SOBRAN:
Por ejemplo: si se dispone de la prueba Calcio pero no de la prueba Albúmina, no se puede obtener
la característica Calcio ajustado por Albúmina

Tiempo ejecución: < 1 min.

Programa anterior a ejecutar: "_1c_quitar_pruebas_fuera_rango.py"
Programa siguiente a ejecutar: "_5_guardar_datos.py"
"""


import os
import pandas as pd

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

dataIN = pd.read_excel(os.path.join(datosDir, 'DatosPruebas1c.xlsx'))

dataOUT = {'IDPaciente': [], 'NumSolicitud': [], 'Prueba': [], 'FRealizacion': [], 'Resultado': [], 'Unidades': []}


pacienteID, numSolicitud, tipoPrueba, fechaPrueba, resPrueba, udsPrueba \
    = dataIN['IDPaciente'], dataIN['NumSolicitud'], dataIN['Prueba'], \
    dataIN['FRealizacion'], dataIN['Resultado'], dataIN['Unidades']

solAntigua = int(numSolicitud[0])
flag = 0

for i in range(1, len(pacienteID)):

    if solAntigua != int(numSolicitud[i]):
        j = i
        solAntigua = int(numSolicitud[i])
        flag = 0
        while solAntigua == int(numSolicitud[j]) and j < len(pacienteID)-1:
            if 'Calcio' in tipoPrueba[j]:
                flag += 1
                idx_borrar = j
            elif 'Albúmina' in tipoPrueba[j]:
                flag -= 1
            j += 1

    if not (flag == 1 and i == idx_borrar):
        dataOUT['IDPaciente'].append(pacienteID[i])
        dataOUT['NumSolicitud'].append(numSolicitud[i])
        dataOUT['Prueba'].append(tipoPrueba[i])
        dataOUT['FRealizacion'].append(fechaPrueba[i])
        dataOUT['Resultado'].append(resPrueba[i])
        dataOUT['Unidades'].append(udsPrueba[i])

nuevoExcel = os.path.join(datosDir, 'DatosPruebas1d.xlsx')
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True)
