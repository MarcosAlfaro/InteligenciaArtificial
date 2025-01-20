import pandas as pd
import os


def crear_fila_csv(vector, writer):
    fila = []
    for elemento in range(len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


datosDir = "DATOS"


datosVectores = pd.read_csv(os.path.join(datosDir, "VectoresPacientes.csv"))
datosPacientes = pd.read_excel(os.path.join(datosDir, "DatosPacientes.xlsx"))
pacientesAnonimo = pd.read_excel(os.path.join(datosDir, "PacientesAnonimo.xlsx"))

pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'LDH', 'Creatinina']

pruebasOUT = ['ComponenteMonoclonal', 'RatioKappaLambda', 'IgA', 'IgG', 'IgM', 'ProteinasTotales',
              'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
              'Albumina', 'Calcio', 'LDH', 'Creatinina']


# ESCRIBIR LOS VECTORES DE LOS PACIENTES
vectoresPacientes, vectoresPositivos = [], []

nivelBajo, nivelMedio, nivelAlto, nivelBajoPos, nivelMedioPos, nivelAltoPos, \
nivelBajoNeg, nivelMedioNeg, nivelAltoNeg = 0, 0, 0, 0, 0, 0, 0, 0, 0
lowAsp, medAsp, highAsp, lowNoAsp, medNoAsp, highNoAsp, lowNumAsp, medNumAsp, highNumAsp = 0, 0, 0, 0, 0, 0, 0, 0, 0
for i in range(len(datosVectores['IDPaciente'])):

    ID = datosVectores['IDPaciente'][i]

    idxPA = list(pacientesAnonimo["IDPaciente"]).index(ID)


    vectorPaciente = []
    vectorPaciente.append(str(datosVectores["IDPaciente"][i]))
    vectorPaciente.append(datosVectores["Componente Monoclonal Ultimo valor"][i])
    vectorPaciente.append(datosVectores["Ratio Kappa/Lambda Ultimo valor"][i])
    vectorPaciente.append(datosVectores["IgA Ultimo valor"][i])
    vectorPaciente.append(datosVectores["IgG Ultimo valor"][i])
    vectorPaciente.append(datosVectores["IgM Ultimo valor"][i])
    if "IgA" in datosPacientes["Grupo"][i]:
        vectorPaciente.append("IgA")
    elif "IgG" in datosPacientes["Grupo"][i]:
        vectorPaciente.append("IgG")
    else:
        vectorPaciente.append("IgM")
    vectorPaciente.append(datosVectores["IgG/No IgG"][i])
    vectorPaciente.append(int(datosVectores["DX2"][i]))

    nivelRiesgo = 0
    if vectorPaciente[1] > 1.5:
        nivelRiesgo += 1
    if vectorPaciente[2] < 0.1 or vectorPaciente[2] > 10:
        nivelRiesgo += 1
    if vectorPaciente[7] == 0:
        nivelRiesgo += 1
    if vectorPaciente[6] == "IgA":
        if vectorPaciente[4] < 650 or vectorPaciente[5] < 50:
            nivelRiesgo += 1
    elif vectorPaciente[6] == "IgG":
        if vectorPaciente[3] < 40 or vectorPaciente[5] < 50:
            nivelRiesgo += 1
    else:
        if vectorPaciente[3] < 40 or vectorPaciente[4] < 650:
            nivelRiesgo += 1
    vectorPaciente.append(nivelRiesgo)

    if vectorPaciente[-1] <= 1:
        nivelBajo += 1
        if vectorPaciente[-2] == 1:
            nivelBajoPos += 1
        else:
            nivelBajoNeg += 1
    elif vectorPaciente[-1] == 2:
        nivelMedio += 1
        if vectorPaciente[-2] == 1:
            nivelMedioPos += 1
        else:
            nivelMedioNeg += 1
    else:
        nivelAlto += 1
        if vectorPaciente[-2] == 1:
            nivelAltoPos += 1
        else:
            nivelAltoNeg += 1

    if pacientesAnonimo["Nº Aspirados"][idxPA] > 0:

        if nivelRiesgo <= 1:
            lowAsp += 1
            lowNumAsp += int(pacientesAnonimo["Nº Aspirados"][idxPA])
        elif nivelRiesgo == 2:
            medAsp += 1
            medNumAsp += int(pacientesAnonimo["Nº Aspirados"][idxPA])
        elif nivelRiesgo > 2:
            highNumAsp += int(pacientesAnonimo["Nº Aspirados"][idxPA])
            highAsp += 1
    else:
        if nivelRiesgo <= 1:
            lowNoAsp += 1
        elif nivelRiesgo == 2:
            medNoAsp += 1
        elif nivelRiesgo > 2:
            highNoAsp += 1

        # print(f'{vectorPaciente}')

print(f"Nivel bajo: {nivelBajo}, Positivos: {nivelBajoPos}, Negativos: {nivelBajoNeg}")
print(f"Nivel medio: {nivelMedio}, Positivos: {nivelMedioPos}, Negativos: {nivelMedioNeg}")
print(f"Nivel alto: {nivelAlto}, Positivos: {nivelAltoPos}, Negativos: {nivelAltoNeg}")

print(f"Media aspirados pacientes: Riesgo bajo: {lowNumAsp/(lowAsp + lowNoAsp)}, "
      f"Riesgo medio: {medNumAsp/(medAsp + medNoAsp)}, "
      f"Riesgo alto: {highNumAsp/(highAsp + highNoAsp)}")
print(f"Total pacientes con aspirados: Riesgo bajo: {lowAsp}, Riesgo medio: {medAsp}, Riesgo alto: {highAsp}")
print(f"Total pacientes sin aspirados: Riesgo bajo: {lowNoAsp}, Riesgo medio: {medNoAsp}, Riesgo alto: {highNoAsp}")
