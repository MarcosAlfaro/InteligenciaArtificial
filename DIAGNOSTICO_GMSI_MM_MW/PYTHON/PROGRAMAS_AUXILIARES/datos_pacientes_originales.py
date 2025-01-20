import os
import numpy as np
import pandas as pd
import _1a_bis_pacientes_excluidos
from datetime import datetime

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

dataIN = pd.read_excel(os.path.join(datosDir, 'DatosPacientes.xlsx'))
# fechaInicioPruebas = datetime(2010, 1, 1)
IDoriginales = list(set(range(575)) - set(_1a_bis_pacientes_excluidos.IDexcluidos))

PA_IDPaciente, grupo, genero, fechaNacimiento, fechaDX1, fechaDX2, DX2, numAnaliticas = \
    dataIN['IDPaciente'], dataIN['Grupo'], dataIN['Genero'], dataIN['Fecha Nacimiento'], \
    dataIN['Fecha DX1'], dataIN['Fecha DX2'], dataIN['DX2'], dataIN['N. Analiticas']

H, M, posH, posM, negH, negM = 0, 0, 0, 0, 0, 0
IgG_H, IgG_M, noIgG_H, noIgG_M, posIgG, negIgG, posNoIgG, negNoIgG = 0, 0, 0, 0, 0, 0, 0, 0
edadH, edadM = [], []
tiempoProgresion, tiempoSeguimiento, intervaloPruebas = [], [], []
for i in range(len(dataIN)):
    if PA_IDPaciente[i] in IDoriginales:

        if genero[i] == "Masculino":
            H += 1
            edadH.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)

            if 'IgG' in grupo[i]:
                IgG_H += 1
                if DX2[i] == 1:
                    posH += 1
                    posIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    negH += 1
                    negIgG += 1
            else:
                noIgG_H += 1
                if DX2[i] == 1:
                    posH += 1
                    posNoIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    negH += 1
                    negNoIgG += 1
        else:
            M += 1
            edadM.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
            if 'IgG' in grupo[i]:
                IgG_M += 1
                if DX2[i] == 1:
                    posM += 1
                    posIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    negM += 1
                    negIgG += 1
            else:
                noIgG_M += 1
                if DX2[i] == 1:
                    posM += 1
                    posNoIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    negM += 1
                    negNoIgG += 1

# FALTA OBTENER:
# TIEMPO DE SEGUIMIENTO: ÚLTIMA ANALÍTICA - PRIMERA ANALÍTICA
# INTERVALO DE VISITAS: TIEMPO DE SEGUIMIENTO / (NUM. VISITAS - 1)
# PENSAR CÓMO HACERLO

dataIN = pd.read_csv(os.path.join(datosDir, 'FechasGraficasCompleto.csv'))

IDPaciente = dataIN["IDPaciente"]
maxNumAnaliticas = max(numAnaliticas)

pacienteActual = 0
for i in range(len(IDPaciente)):
    if IDPaciente[i] == pacienteActual or IDPaciente[i] not in IDoriginales:
        pacienteActual = IDPaciente[i]
        continue
    for j in range(maxNumAnaliticas):
        fechasPaciente = dataIN[str(j)][i]
        if fechasPaciente == 0.0:
            break
    if j > 1:
        tiempoSeguimiento.append(dataIN[str(j-1)][i] - dataIN["0"][i])
        idxPaciente = list(PA_IDPaciente).index(IDPaciente[i])
        numAnaliticasPaciente = numAnaliticas[idxPaciente]
        intervaloPruebas.append(tiempoSeguimiento[-1]/(numAnaliticasPaciente-1))
    pacienteActual = IDPaciente[i]

edadM.remove(edadM[-3])
edadM.remove(edadM[-2])
edadM.remove(edadM[-1])

edadTodos = edadH + edadM
maxEdad, minEdad, maxEdadH, minEdadH, maxEdadM, minEdadM, avgEdad, avgEdadH, avgEdadM, desvEdad, desvEdadH, desvEdadM =\
    max(edadTodos), min(edadTodos), max(edadH), min(edadH), max(edadM), min(edadM), \
    np.average(edadTodos), np.average(edadH), np.average(edadM), np.std(edadTodos), np.std(edadH), np.std(edadM)
avgTiempoProg, desvTiempoProg = np.average(tiempoProgresion), np.std(tiempoProgresion)
avgTiempoSeg, desvTiempoSeg = np.average(tiempoSeguimiento), np.std(tiempoSeguimiento)
avgIntervalo, desvIntervalo = np.average(intervaloPruebas), np.std(intervaloPruebas)

print("PACIENTES ORIGINALES")

print(f"Total pacientes: {H+M}, hombres: {H}, mujeres: {M}")

print(f"Edad pacientes: {avgEdad} +- {desvEdad} años, rango:{minEdad}-{maxEdad} años")
print(f"Edad pacientes hombres: {avgEdadH} +- {desvEdadH} años, rango:{minEdadH}-{maxEdadH} años")
print(f"Edad pacientes mujeres: {avgEdadM} +- {desvEdadM} años, rango:{minEdadM}-{maxEdadM} años")

print(f"Total positivos: {posH+posM}, hombres: {posH}, mujeres:{posM}")
print(f"Total negativos: {negH+negM}, hombres: {negH}, mujeres:{negM}")

print(f"Pacientes grupo IgG: {IgG_H+IgG_M}, hombres: {IgG_H}, mujeres: {IgG_M}")
print(f"Pacientes grupo no-IgG: {noIgG_H+noIgG_M}, hombres: {noIgG_H}, mujeres: {noIgG_M}")

print(f"Pacientes grupo IgG positivos: {posIgG}, negativos: {negIgG}")
print(f"Pacientes grupo no-IgG positivos: {posNoIgG}, negativos: {negNoIgG}")

print(f"Tiempo progresión MGUS->MM: {avgTiempoProg} +- {desvTiempoProg} años")
print(f"Tiempo seguimiento pacientes: {avgTiempoSeg} +- {desvTiempoSeg} años")
print(f"Intervalo realización pruebas: {avgIntervalo} +- {desvIntervalo} años")
