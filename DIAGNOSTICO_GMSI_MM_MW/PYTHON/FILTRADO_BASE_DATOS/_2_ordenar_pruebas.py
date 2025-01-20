"""
EN ESTE PROGRAMA SE ORDENAN LAS PRUEBAS POR NÚMERO DE SOLICITUD DE MENOR A MAYOR:

Tiempo ejecución: <1 min.

Programa anterior a ejecutar: '_1b_quitar_pruebas_irrelevantes.py'
Programa siguiente a ejecutar: '_3_contar_pruebas.py'
"""

import pandas as pd
import os

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

datosPruebas = pd.read_excel(os.path.join(datosDir, 'DatosPruebas1b.xlsx'))


DP_pacienteID, DP_numSolicitud, DP_tipoPrueba, DP_fechaPrueba, DP_resPrueba, DP_udsPrueba \
    = datosPruebas['IDPaciente'], datosPruebas['NumSolicitud'], datosPruebas['Prueba'], \
    datosPruebas['FRealizacion'], datosPruebas['Resultado'], datosPruebas['Unidades']

pacienteID, numSolicitud, tipoPrueba, fechaPrueba, resPrueba = [], [], [], [], []
udsPrueba, comentarioPrueba1, textoPrueba, comentarioPrueba = [], [], [], []

for i in range(len(DP_pacienteID)):
    pacienteID.append(int(DP_pacienteID[i]))
    numSolicitud.append(int(DP_numSolicitud[i]))
    tipoPrueba.append(DP_tipoPrueba[i])
    fechaPrueba.append(DP_fechaPrueba[i])
    resPrueba.append(float(DP_resPrueba[i]))
    udsPrueba.append(DP_udsPrueba[i])


# Se ordenan las pruebas en función del número de solicitud
listasOrdenadas = sorted(zip(numSolicitud, pacienteID,
                             tipoPrueba, fechaPrueba, resPrueba, udsPrueba), key=lambda x: x[0])

# Descomprimir las listas ordenadas
numSolicitud, pacienteID, tipoPrueba, fechaPrueba, resPrueba, udsPrueba = zip(*listasOrdenadas)

# Convertir las tuplas de vuelta a listas, si es necesario
numSolicitud, pacienteID, tipoPrueba, fechaPrueba, resPrueba, udsPrueba \
    = list(numSolicitud), list(pacienteID), list(tipoPrueba), list(fechaPrueba), list(resPrueba), list(udsPrueba)


dataOUT = {'IDPaciente': [], 'NumSolicitud': [], 'Prueba': [], 'FRealizacion': [], 'Resultado': [], 'Unidades': []}

for i in range(len(pacienteID)):
    dataOUT['IDPaciente'].append(pacienteID[i])
    dataOUT['NumSolicitud'].append(numSolicitud[i])
    dataOUT['Prueba'].append(tipoPrueba[i])
    dataOUT['FRealizacion'].append(fechaPrueba[i])
    dataOUT['Resultado'].append(resPrueba[i])
    dataOUT['Unidades'].append(udsPrueba[i])

nuevoExcel = os.path.join(datosDir, 'DatosPruebas2.xlsx')
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True)
