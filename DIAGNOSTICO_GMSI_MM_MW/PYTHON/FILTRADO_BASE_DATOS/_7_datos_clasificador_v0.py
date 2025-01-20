import pandas as pd
import numpy as np
import _1a_quitar_pacientes
import _6_completar_datos
import csv


def crear_fila_csv(ID, vector):
    fila = [ID]
    for elemento in range(0, len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


datosPacientes = pd.read_excel('DatosPacientes.xlsx')

PA_IDPaciente = datosPacientes['IDPaciente']
PA_FechaDX1 = datosPacientes['Fecha DX1']
PA_FechaNacimiento = datosPacientes['Fecha Nacimiento']
PA_Grupo = datosPacientes['Grupo']
PA_DX2 = datosPacientes['DX2']

datosGraficas = pd.read_csv("DatosGraficasCompleto.csv", encoding='latin1')
fechasGraficas = pd.read_csv("FechasGraficasCompleto.csv", encoding='latin1')

numAnaliticas = 154
dimensiones = (numAnaliticas, 24, 575)
resultadosPruebas = np.zeros(dimensiones)
fechasPruebas = np.zeros(dimensiones)
pacientesValidos = 0

pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Ratio Neutrofilos/Linfocitos', 'Ratio Plaquetas/Linfocitos', 'Ratio Monocitos/Linfocitos',
           'Albumina', 'Calcio', 'Proteina C reactiva', 'VSG', 'LDH',
           'Creatinina', 'Ratio Creatinina/Hemoglobina', 'Beta-2 microglobulina']

for i in range(0, len(datosGraficas['IDPaciente'])):
    IDPaciente = int(datosGraficas['IDPaciente'][i])
    for j in range(0, numAnaliticas):
        resultadosPruebas[j][i % len(pruebas)][IDPaciente] = datosGraficas[str(j)][i]
        fechasPruebas[j][i % len(pruebas)][IDPaciente] = fechasGraficas[str(j)][i]

lenVector = 2 * len(pruebas) + 3

with open('DatosClasificador.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    lineaTituloColumnas = ["IDPaciente"]
    for prueba in range(0, len(pruebas)):
        lineaTituloColumnas.append(pruebas[prueba] + " Ultimo valor")
        lineaTituloColumnas.append(pruebas[prueba] + " Tendencia")
    lineaTituloColumnas.append("Edad")
    lineaTituloColumnas.append("IgG/No IgG")
    lineaTituloColumnas.append("DX2")

    writer.writerow(lineaTituloColumnas)
    vectoresPacientes = [np.zeros(lenVector)]

    for ID in range(1, 575):
        if ID in _1a_quitar_pacientes.IDexcluidos:
            vectoresPacientes.append(np.zeros(lenVector))
        else:
            existePrueba = 1
            for prueba in range(0, len(pruebas)):
                if resultadosPruebas[0][prueba][ID] == 0:
                    existePrueba = 0

            if existePrueba == 0:
                vectoresPacientes.append(np.zeros(lenVector))

            else:
                for sol in range(0, numAnaliticas):
                    if resultadosPruebas[sol][0][ID] == 0:
                        N = sol - 1
                        break
                if N < 3:
                    vectoresPacientes.append(np.zeros(lenVector))
                    print(ID)
                else:
                    pacientesValidos += 1
                    vectorPaciente = np.zeros(lenVector)
                    for prueba in range(0, len(pruebas)):
                        vectorPaciente[2 * prueba] = resultadosPruebas[N][prueba][ID]
                        vectorPaciente[2 * prueba + 1] = \
                            (resultadosPruebas[N][prueba][ID] - resultadosPruebas[N - 3][prueba][ID]) / \
                            (fechasPruebas[N][prueba][ID] - fechasPruebas[N - 3][prueba][ID])

                    for idx in range(0, len(PA_IDPaciente)):
                        if int(PA_IDPaciente[idx]) == ID:
                            break

                    vectorPaciente[-3] = (PA_FechaDX1[idx] - PA_FechaNacimiento[idx]).days / 365.25 + \
                                         fechasPruebas[N][0][ID]
                    if 'IgG' in PA_Grupo[idx]:
                        vectorPaciente[-2] = 0
                    else:
                        vectorPaciente[-2] = 1

                    vectorPaciente[-1] = PA_DX2[idx]

                    vectoresPacientes.append(vectorPaciente)

                    crear_fila_csv(ID, vectorPaciente)

print(f"Número de pacientes válidos: {pacientesValidos}")


