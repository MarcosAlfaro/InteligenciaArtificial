import numpy as np
import pandas as pd
from scipy import io
import csv

datosVectores = pd.read_csv("VectoresPacientes.csv")
# datosVectores = pd.read_csv("VectoresPacientesDA.csv")

"""
pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Ratio Neutrofilos/Linfocitos', 'Ratio Plaquetas/Linfocitos', 'Ratio Monocitos/Linfocitos',
           'Albumina', 'Calcio', 'Proteina C reactiva', 'VSG', 'LDH',
           'Creatinina', 'Ratio Creatinina/Hemoglobina', 'Beta-2 microglobulina']
"""

pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteinas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albumina', 'Calcio', 'Proteina C reactiva', 'VSG', 'LDH', 'Creatinina', 'Beta-2 microglobulina']


dimensiones = (len(datosVectores['IDPaciente']), 2*len(pruebas)+3)
matrizDatos = np.zeros(dimensiones)
cont = 0

vectoresPacientes = []
for i in range(len(datosVectores['IDPaciente'])):
    if i == 51:
        print(i)
    # vectorPaciente = [datosVectores["IDPaciente"][i]]
    for j in range(len(pruebas)):
        matrizDatos[i][2*j] = datosVectores[pruebas[j] + " Ultimo valor"][i]
        matrizDatos[i][2*j+1] = datosVectores[pruebas[j] + " Tendencia"][i]
    matrizDatos[i][-3] = datosVectores["Edad"][i]
    matrizDatos[i][-2] = datosVectores["IgG/No IgG"][i]
    matrizDatos[i][-1] = datosVectores["DX2"][i]
    # vectoresPacientes.append(vectorPaciente)

io.savemat('matrizDatosSR.mat', {'matriz': matrizDatos})

matrizCovarianza = np.cov(matrizDatos)
# matrizCovarianza = np.cov(matrizDatos, bias=True)  # muestral

io.savemat('matrizCovarianzaSR.mat', {'matriz': matrizCovarianza})

print(matrizCovarianza)

"""EN MATLAB"""
# datos = load('matrizDatos.mat');
# matrizDatos = datos.matriz;
# matrizDatos = datos.matrizDatos;
# matrizCovarianza = cov(matrizDatos)  # poblacional
# matrizCovarianza = cov(matrizDatos, 1)  # muestral



