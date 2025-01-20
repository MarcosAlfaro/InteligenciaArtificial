import os
import numpy as np
import pandas as pd
from datetime import datetime

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

datosPacientes = pd.read_excel(os.path.join(datosDir, 'DatosPacientes.xlsx'))
datosPacientesFiltrados = pd.read_csv(os.path.join(datosDir, 'VectoresPacientes.csv'))
# fechaInicioPruebas = datetime(2010, 1, 1)
IDfiltrados = list(set(datosPacientesFiltrados["IDPaciente"]))

PA_IDPaciente, grupo, genero, fechaNacimiento, fechaDX1, fechaDX2, DX2, numAnaliticas = \
    datosPacientes['IDPaciente'], datosPacientes['Grupo'], datosPacientes['Genero'], \
    datosPacientes['Fecha Nacimiento'], datosPacientes['Fecha DX1'], datosPacientes['Fecha DX2'], \
    datosPacientes['DX2'], datosPacientes['N. Analiticas']

H, M, posH, posM, negH, negM = 0, 0, 0, 0, 0, 0
IgG_H, IgG_M, noIgG_H, noIgG_M, posIgG, negIgG, posNoIgG, negNoIgG = 0, 0, 0, 0, 0, 0, 0, 0
edadH, edadM = [], []
edadPos, edadNeg = [], []
tiempoProgresion, tiempoSeguimiento, intervaloPruebas, ritmoAnaliticas = [], [], [], []
for i in range(len(datosPacientes)):
    if PA_IDPaciente[i] in IDfiltrados:

        if genero[i] == "Masculino":
            H += 1
            edadH.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)

            if 'IgG' in grupo[i]:
                IgG_H += 1
                if DX2[i] == 1:
                    edadPos.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    posH += 1
                    posIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    edadNeg.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    negH += 1
                    negIgG += 1
            else:
                noIgG_H += 1
                if DX2[i] == 1:
                    edadPos.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    posH += 1
                    posNoIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    edadNeg.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    negH += 1
                    negNoIgG += 1
        else:
            M += 1
            edadM.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
            if 'IgG' in grupo[i]:
                IgG_M += 1
                if DX2[i] == 1:
                    edadPos.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    posM += 1
                    posIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    edadNeg.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    negM += 1
                    negIgG += 1
            else:
                noIgG_M += 1
                if DX2[i] == 1:
                    edadPos.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
                    posM += 1
                    posNoIgG += 1
                    tiempoProgresion.append((fechaDX2[i] - fechaDX1[i]).days / 365.25)
                else:
                    edadNeg.append((fechaDX1[i] - fechaNacimiento[i]).days / 365.25)
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
    if IDPaciente[i] == pacienteActual or IDPaciente[i] not in IDfiltrados:
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
        ritmoAnaliticas.append(numAnaliticasPaciente)
    pacienteActual = IDPaciente[i]

edadM.remove(edadM[-1])

edadPos.remove(edadPos[-1])


edadTodos = edadH + edadM
maxEdad, minEdad, maxEdadH, minEdadH, maxEdadM, minEdadM, avgEdad, avgEdadH, avgEdadM, desvEdad, desvEdadH, desvEdadM =\
    max(edadTodos), min(edadTodos), max(edadH), min(edadH), max(edadM), min(edadM), \
    np.average(edadTodos), np.average(edadH), np.average(edadM), np.std(edadTodos), np.std(edadH), np.std(edadM)

maxEdadPos, minEdadPos, avgEdadPos, desvEdadPos, maxEdadNeg, minEdadNeg, avgEdadNeg, desvEdadNeg =\
    max(edadPos), min(edadPos), np.average(edadPos), np.std(edadPos),\
    max(edadNeg), min(edadNeg), np.average(edadNeg), np.std(edadNeg)

avgTiempoProg, desvTiempoProg = np.average(tiempoProgresion), np.std(tiempoProgresion)
avgTiempoSeg, desvTiempoSeg = np.average(tiempoSeguimiento), np.std(tiempoSeguimiento)
avgIntervalo, desvIntervalo = np.average(intervaloPruebas), np.std(intervaloPruebas)
avgRitmo, desvRitmo = np.average(ritmoAnaliticas), np.std(ritmoAnaliticas)

print("PACIENTES ORIGINALES")

print(f"Total pacientes: {H+M}, hombres: {H}, mujeres: {M}")

print(f"Edad pacientes: {avgEdad} +- {desvEdad} años, rango:{minEdad}-{maxEdad} años")
print(f"Edad pacientes hombres: {avgEdadH} +- {desvEdadH} años, rango:{minEdadH}-{maxEdadH} años")
print(f"Edad pacientes mujeres: {avgEdadM} +- {desvEdadM} años, rango:{minEdadM}-{maxEdadM} años")
print(f"Edad pacientes positivos: {avgEdadPos} +- {desvEdadPos} años, rango:{minEdadPos}-{maxEdadPos} años")
print(f"Edad pacientes negativos: {avgEdadNeg} +- {desvEdadNeg} años, rango:{minEdadNeg}-{maxEdadNeg} años")

print(f"Total positivos: {posH+posM}, hombres: {posH}, mujeres:{posM}")
print(f"Total negativos: {negH+negM}, hombres: {negH}, mujeres:{negM}")

print(f"Pacientes grupo IgG: {IgG_H+IgG_M}, hombres: {IgG_H}, mujeres: {IgG_M}")
print(f"Pacientes grupo no-IgG: {noIgG_H+noIgG_M}, hombres: {noIgG_H}, mujeres: {noIgG_M}")

print(f"Pacientes grupo IgG positivos: {posIgG}, negativos: {negIgG}")
print(f"Pacientes grupo no-IgG positivos: {posNoIgG}, negativos: {negNoIgG}")

print(f"Tiempo progresión MGUS->MM: {avgTiempoProg} +- {desvTiempoProg} años")
print(f"Tiempo seguimiento pacientes: {avgTiempoSeg} +- {desvTiempoSeg} años")
print(f"Intervalo realización pruebas: {avgIntervalo} +- {desvIntervalo} años")
print(f"Número de pruebas anuales: {avgRitmo} +- {desvRitmo} pruebas/año")


dataIN = pd.read_excel(os.path.join(datosDir, 'PacientesAnonimo.xlsx'))

IDPaciente, DX2, N_aspirados, grupo = dataIN['IDPaciente'], dataIN['DX2(MM=1;MW=2)'], dataIN['Nº Aspirados'], dataIN['Ifs']


posAsp, posNoAsp, negAsp, negNoAsp, asp, noAsp = 0, 0, 0, 0, 0, 0
posNumAsp, negNumAsp, numAsp = 0, 0, 0
IgAAsp, IgGAsp, IgMAsp, IgANoAsp, IgGNoAsp, IgMNoAsp, IgANumAsp, IgGNumAsp, IgMNumAsp = 0, 0, 0, 0, 0, 0, 0, 0, 0
for i in range(len(IDPaciente)):
    ID = int(IDPaciente[i])
    if ID in IDfiltrados:

        if N_aspirados[i] >= 1:
            numAsp += int(N_aspirados[i])
            asp += 1
            if DX2[i] == 1 or DX2[i] == 2:
                posAsp += 1
                posNumAsp += int(N_aspirados[i])
            else:
                negAsp += 1
                negNumAsp += int(N_aspirados[i])

            if 'IgA' in grupo[i]:
                IgAAsp += 1
                IgANumAsp += int(N_aspirados[i])
            elif 'IgG' in grupo[i]:
                IgGAsp += 1
                IgGNumAsp += int(N_aspirados[i])
            elif 'IgM' in grupo[i]:
                IgMNumAsp += int(N_aspirados[i])
                IgMAsp += 1
        else:
            noAsp += 1
            if DX2[i] == 1 or DX2[i] == 2:
                posNoAsp += 1
            else:
                negNoAsp += 1

            if 'IgA' in grupo[i]:
                IgANoAsp += 1
            elif 'IgG' in grupo[i]:
                IgGNoAsp += 1
            elif 'IgM' in grupo[i]:
                IgMNoAsp += 1

print(f"Media aspirados pacientes: {numAsp/292}, Positivos: {posNumAsp/7}, Negativos: {negNumAsp/285}")
print(f"Total pacientes con aspirados: {asp}, Positivos: {posAsp}, Negativos: {negAsp}")
print(f"Total pacientes sin aspirados: {noAsp}, Positivos: {posNoAsp}, Negativos: {negNoAsp}")

print(f"Media aspirados pacientes: {numAsp/292}, IgA: {IgANumAsp/41}, IgG: {IgGNumAsp/216}, IgM: {IgMNumAsp/35}")
print(f"Total pacientes con aspirados: {asp}, IgA: {IgAAsp}, IgG: {IgGAsp}, IgM: {IgMAsp}")
print(f"Total pacientes sin aspirados: {noAsp}, IgA: {IgANoAsp}, IgG: {IgGNoAsp}, IgM: {IgMNoAsp}")
