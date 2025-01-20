"""
EN ESTE PROGRAMA SE JUNTAN LOS DATOS DE TODAS LAS PRUEBAS REALIZADAS A TODOS LOS PACIENTES
EN UN ÚNICO EXCEL "DatosPruebas0.xlsx"

Tiempo ejecución: 5 min aprox.
Tamaño archivo creado: 40MB aprox. (974721 filas)

Programa anterior a ejecutar: Ninguno
Programa siguiente a ejecutar: '_1a_quitar_pacientes.py'
"""

import pandas as pd
import os

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

dataIN = [pd.read_excel(os.path.join(datosDir, 'Datos1-199.xlsx'), sheet_name='P_laboratorio_pac1-99'),
          pd.read_excel(os.path.join(datosDir, 'Datos1-199.xlsx'), sheet_name='P_laboratorio_pac100-199'),
          pd.read_excel(os.path.join(datosDir, 'Datos200-299.xlsx'), sheet_name='P laboratorio pac200-299'),
          pd.read_excel(os.path.join(datosDir, 'Datos300-399.xlsx'), sheet_name='P laboratorio pac300-399'),
          pd.read_excel(os.path.join(datosDir, 'Datos400-574.xlsx'), sheet_name='P laboratorio pac400-499'),
          pd.read_excel(os.path.join(datosDir, 'Datos400-574.xlsx'), sheet_name='P laboratorio pac500-574')
          ]

dataOUT = {'IDPaciente': [], 'NumSolicitud': [], 'Prueba': [], 'FRealizacion': [], 'Resultado': [], 'Unidades': []}

for num in range(6):
    pacienteID = dataIN[num]['IDPaciente']
    numSolicitud = dataIN[num]['NumSolicitud']
    tipoPrueba = dataIN[num]['Prueba']
    fechaPrueba = dataIN[num]['FRealizacion']
    resPrueba = dataIN[num]['Resultado']
    udsPrueba = dataIN[num]['Unidades']

    for i in range(len(pacienteID)):
        dataOUT['IDPaciente'].append(pacienteID[i])
        dataOUT['NumSolicitud'].append(numSolicitud[i])
        dataOUT['Prueba'].append(tipoPrueba[i])
        dataOUT['FRealizacion'].append(fechaPrueba[i])
        dataOUT['Resultado'].append(resPrueba[i])
        dataOUT['Unidades'].append(udsPrueba[i])

nuevoExcel = os.path.join(datosDir, 'DatosPruebas0.xlsx')
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True)
