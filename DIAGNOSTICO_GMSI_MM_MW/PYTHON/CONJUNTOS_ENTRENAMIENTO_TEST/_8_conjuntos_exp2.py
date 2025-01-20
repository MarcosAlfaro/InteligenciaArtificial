import pandas as pd
import csv
import os


def crear_fila_csv(vector, writer):
    fila = []
    for elemento in range(len(vector)):
        fila.append(vector[elemento])
    # print(fila)
    writer.writerow(fila)
    return


datosDir = "DATOS"

IDPositivos = [73, 294, 330, 412, 468, 534, 573]

pruebas = ['ComponenteMonoclonal', 'RatioKappaLambda', 'IgA', 'IgG', 'IgM', 'ProteinasTotales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'LDH', 'Creatinina']

# esto es lo que cambia según el experimento
idxPruebas = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 15, 17, 21, 23, 27, 33, 35, 36]

for ID in IDPositivos:

    with open(os.path.join(datosDir, 'VectoresPacientesEntrenamientoExp2ID' + str(ID) + '.csv'), 'w',
              newline='') as file1:
        writer1 = csv.writer(file1)

        lineaTituloColumnas = []
        cont = 1
        for prueba in range(len(pruebas)):
            if cont in idxPruebas:
                lineaTituloColumnas.append(pruebas[prueba] + "UltimoValor")
            cont += 1
            if cont in idxPruebas:
                lineaTituloColumnas.append(pruebas[prueba] + "Tendencia")
            cont += 1
        if cont in idxPruebas:
            lineaTituloColumnas.append("Edad")
        cont += 1
        if cont in idxPruebas:
            lineaTituloColumnas.append("IgGNoIgG")
        lineaTituloColumnas.append("DX2")
        writer1.writerow(lineaTituloColumnas)

        with open(os.path.join(datosDir, 'VectoresPacientesTestExp2ID' + str(ID) + '.csv'), 'w', newline='') as file2:
            writer2 = csv.writer(file2)

            lineaTituloColumnas = []
            cont = 1
            for prueba in range(len(pruebas)):
                if cont in idxPruebas:
                    lineaTituloColumnas.append(pruebas[prueba] + "UltimoValor")
                cont += 1
                if cont in idxPruebas:
                    lineaTituloColumnas.append(pruebas[prueba] + "Tendencia")
                cont += 1
            if cont in idxPruebas:
                lineaTituloColumnas.append("Edad")
            cont += 1
            if cont in idxPruebas:
                lineaTituloColumnas.append("IgGNoIgG")
            lineaTituloColumnas.append("DX2")
            writer2.writerow(lineaTituloColumnas)

            for id in IDPositivos:
                datosVectores = pd.read_csv(os.path.join(datosDir, "GrupoID" + str(id) + ".csv"))
                vectoresPacientes = []
                for i in range(len(datosVectores['IDPaciente'])):
                    vectorPaciente = []
                    cont = 1
                    for j in range(len(pruebas)):
                        if cont in idxPruebas:
                            vectorPaciente.append(datosVectores[pruebas[j] + "UltimoValor"][i])
                        cont += 1
                        if cont in idxPruebas:
                            vectorPaciente.append(datosVectores[pruebas[j] + "Tendencia"][i])
                        cont += 1
                    if cont in idxPruebas:
                        vectorPaciente.append(datosVectores["Edad"][i])
                    cont += 1
                    if cont in idxPruebas:
                        vectorPaciente.append(datosVectores["IgGNoIgG"][i])
                    vectorPaciente.append(int(datosVectores["DX2"][i]))
                    vectoresPacientes.append(vectorPaciente)
                if id == ID:
                    for i in range(len(vectoresPacientes)):
                        crear_fila_csv(vectoresPacientes[i], writer2)
                else:
                    for i in range(len(vectoresPacientes)):
                        crear_fila_csv(vectoresPacientes[i], writer1)
