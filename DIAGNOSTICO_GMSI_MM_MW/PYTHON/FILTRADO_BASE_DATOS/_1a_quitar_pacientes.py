"""
EN ESTE PROGRAMA SE ELIMINAN DEL EXCEL "DatosPruebas0.xlsx" LOS DATOS DE LAS PRUEBAS
CORRESPONDIENTES A PACIENTES QUE:
- no son de interés (IDexcluidos1)
- pertenecen a un grupo incorrecto (IDexcluidos2 e IDexcluidos3)

Tiempo ejecución: 4 min aprox.

Programa anterior a ejecutar: '_0_juntar_datos.py'
Programa siguiente a ejecutar: '_1b_quitar_pruebas_irrelevantes.py'
"""

import os
import pandas as pd
import _1a_bis_pacientes_excluidos


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")


dataIN = pd.read_excel(os.path.join(datosDir, 'DatosPruebas0.xlsx'))

dataOUT = {'IDPaciente': [], 'NumSolicitud': [], 'Prueba': [], 'FRealizacion': [], 'Resultado': [], 'Unidades': []}

pacienteID, numSolicitud, tipoPrueba, fechaPrueba, resPrueba, udsPrueba \
    = dataIN['IDPaciente'], dataIN['NumSolicitud'], dataIN['Prueba'], \
    dataIN['FRealizacion'], dataIN['Resultado'], dataIN['Unidades']

for i in range(len(pacienteID)):
    if not int(pacienteID[i]) in _1a_bis_pacientes_excluidos.IDexcluidos:
        dataOUT['IDPaciente'].append(pacienteID[i])
        dataOUT['NumSolicitud'].append(numSolicitud[i])
        dataOUT['Prueba'].append(tipoPrueba[i])
        dataOUT['FRealizacion'].append(fechaPrueba[i])
        dataOUT['Resultado'].append(resPrueba[i])
        dataOUT['Unidades'].append(udsPrueba[i])

nuevoExcel = os.path.join(datosDir, 'DatosPruebas1a.xlsx')
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True) 
