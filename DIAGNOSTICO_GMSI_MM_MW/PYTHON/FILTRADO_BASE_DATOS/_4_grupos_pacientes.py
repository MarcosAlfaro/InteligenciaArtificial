"""
EN ESTE PROGRAMA SE AÑADE INFORMACIÓN GENERAL DE CADA PACIENTE AL EXCEL "DatosPacientes.xlsx"

Tiempo ejecución: 0.

Programa anterior a ejecutar: "_3_contar_pruebas.py"
Programa siguiente a ejecutar: "_1c_quitar_pruebas_fuera_rango.py"
"""

import os
import pandas as pd
import _1a_bis_pacientes_excluidos

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

dataIN = pd.read_excel(os.path.join(datosDir, 'PacientesAnonimo.xlsx'))


grupos = ['DX2pos', ['IgG-Kappa', 'IgG-kappa'], ['IgG-Lambda', 'IgG-lambda'], ['IgG-kappa, lambda'],
          ['IgM-Lambda', 'IgM-lambda'], ['IgM-Kappa', 'IgM-kappa'],
          ['IgA-Lambda', 'IgA-lambda'], ['IgA-Kappa', 'IgA-kappa'],
          ['IgA-kappa/IgG-kappa']
          ]

DX2, IgG_K, IgG_L, IgG_KL, IgM, IgM_K, IgM_L, IgA_K, IgA_L, IgA_K_IgG_K, otros \
    = [], [], [], [], [], [], [], [], [], [], []
DX2_CSV, grupoCSV, generoCSV, nacimientoCSV = [], [], [], []

DX2_M, DX2_F, IgG_K_M, IgG_K_F, IgG_L_M, IgG_L_F, IgG_KL_M, IgG_KL_F = 0, 0, 0, 0, 0, 0, 0, 0
IgM_M, IgM_F, IgM_K_M, IgM_K_F, IgM_L_M, IgM_L_F = 0, 0, 0, 0, 0, 0
IgA_K_M, IgA_K_F, IgA_L_M, IgA_L_F, IgA_K_IgG_K_M, IgA_K_IgG_K_F = 0, 0, 0, 0, 0, 0
otros_M, otros_F = 0, 0

pacienteID = dataIN['IDPaciente']
Ifs = dataIN['Ifs']
genero = dataIN['Género']
tipoDX2 = dataIN['DX2(MM=1;MW=2)']
fechaNacimiento = dataIN['Fecha Nacimiento']


for i in range(len(pacienteID)):

    if not int(pacienteID[i]) in _1a_bis_pacientes_excluidos.IDexcluidos:

        nacimientoCSV.append(fechaNacimiento[i].to_pydatetime())

        if tipoDX2[i] == 1 or tipoDX2[i] == 2:
            DX2.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                DX2_M += 1
            else:
                DX2_F += 1

        if Ifs[i] in ['IgG-Kappa', 'IgG-kappa']:
            IgG_K.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgG_K_M += 1
                generoCSV.append('Masculino')
            else:
                IgG_K_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgG-K')

        elif Ifs[i] in ['IgG-Lambda', 'IgG-lambda']:
            IgG_L.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgG_L_M += 1
                generoCSV.append('Masculino')
            else:
                IgG_L_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgG-L')

        elif Ifs[i] in ['IgG-kappa, lambda']:
            IgG_KL.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgG_KL_M += 1
                generoCSV.append('Masculino')
            else:
                IgG_KL_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgG-KL')

        elif Ifs[i] in ['IgM']:
            IgM.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgM_M += 1
                generoCSV.append('Masculino')
            else:
                IgM_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgM-SC')

        elif Ifs[i] in ['IgM-Kappa', 'IgM-kappa']:
            IgM_K.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgM_K_M += 1
                generoCSV.append('Masculino')
            else:
                IgM_K_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgM-K')

        elif Ifs[i] in ['IgM-Lambda', 'IgM-lambda']:
            IgM_L.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgM_L_M += 1
                generoCSV.append('Masculino')
            else:
                IgM_L_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgM-L')

        elif Ifs[i] in ['IgA-Kappa', 'IgA-kappa']:
            IgA_K.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgA_K_M += 1
                generoCSV.append('Masculino')
            else:
                IgA_K_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgA-K')

        elif Ifs[i] in ['IgA-Lambda', 'IgA-lambda']:
            IgA_L.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgA_L_M += 1
                generoCSV.append('Masculino')
            else:
                IgA_L_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgA-L')

        elif Ifs[i] == 'IgA-kappa/IgG-kappa':
            IgA_K_IgG_K.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                IgA_K_IgG_K_M += 1
                generoCSV.append('Masculino')
            else:
                IgA_K_IgG_K_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('IgA-K,IgG-K')

        else:
            otros.append(int(pacienteID[i]))
            if genero[i] == 'Masculino':
                otros_M += 1
                generoCSV.append('Masculino')
            else:
                otros_F += 1
                generoCSV.append('Femenino')
            grupoCSV.append('Otros')

print(f"Pacientes DX2 positivo: {DX2} , Total={len(DX2)} , Hombres={DX2_M}, Mujeres={DX2_F}")
print(f"Pacientes IgG-Kappa: {IgG_K} , Total={len(IgG_K)} , Hombres={IgG_K_M}, Mujeres={IgG_K_F}")
print(f"Pacientes IgG-Lambda: {IgG_L} , Total={len(IgG_L)} , Hombres={IgG_L_M}, Mujeres={IgG_L_F}")
print(f"Pacientes IgG-Kappa/Lambda: {IgG_KL} , Total={len(IgG_KL)} , Hombres={IgG_KL_M}, Mujeres={IgG_KL_F}")
print(f"Pacientes IgM-sin clasificar: {IgM} , Total={len(IgM)} , Hombres={IgM_M}, Mujeres={IgM_F}")
print(f"Pacientes IgM-Kappa: {IgM_K} , Total={len(IgM_K)} , Hombres={IgM_K_M}, Mujeres={IgM_K_F}")
print(f"Pacientes IgM-Lambda: {IgM_L} , Total={len(IgM_L)} , Hombres={IgM_L_M}, Mujeres={IgM_L_F}")
print(f"Pacientes IgA-Kappa: {IgA_K} , Total={len(IgA_K)} , Hombres={IgA_K_M}, Mujeres={IgA_K_F}")
print(f"Pacientes IgA-Lambda: {IgA_L} , Total={len(IgA_L)} , Hombres={IgA_L_M}, Mujeres={IgA_L_F}")
print(f"Pacientes IgA-Kappa, IgG-Kappa: {IgA_K_IgG_K} , Total={len(IgA_K_IgG_K)} , "
      f"Hombres={IgA_K_IgG_K_M}, Mujeres={IgA_K_IgG_K_F}")
print(f"Otros: {otros} , Total={len(otros)}, Hombres={otros_M}, Mujeres={otros_F}")


rutaExcel = os.path.join(datosDir, "DatosPacientes.xlsx")
dIN = pd.read_excel(rutaExcel)
dIN['Grupo'] = grupoCSV
dIN['Genero'] = generoCSV
dIN['Fecha Nacimiento'] = nacimientoCSV

dIN.to_excel(rutaExcel, index=True)
