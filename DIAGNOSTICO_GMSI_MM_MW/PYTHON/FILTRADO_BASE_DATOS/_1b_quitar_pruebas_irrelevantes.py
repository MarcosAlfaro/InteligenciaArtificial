"""
EN ESTE PROGRAMA SE ELIMINAN DEL EXCEL "DatosPruebas1a.xlsx"
LOS DATOS DE LAS PRUEBAS QUE NO SON DE INTERÉS O PRESENTAN RESULTADOS NO VÁLIDOS:

NOTA: antes de ejecutar este programa hay que abrir el Excel "DatosPruebas1a.xlsx"
y eliminar mediante Buscar y Reemplazar lo siguiente:
Puntos -> Comas
<= -> Nada
>= -> Nada
< -> Nada
> -> Nada


Tiempo ejecución: 3 min aprox.

Programa anterior a ejecutar: "_1a_quitar_pacientes.py"
Programa siguiente a ejecutar: "_2_ordenar_pruebas.py"
"""

import os
import pandas as pd

baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

dataIN = pd.read_excel(os.path.join(datosDir, 'DatosPruebas1a.xlsx'))

dataOUT = {'IDPaciente': [], 'NumSolicitud': [], 'Prueba': [], 'FRealizacion': [], 'Resultado': [], 'Unidades': []}

# CONJUNTO DE PRUEBAS REDUCIDO
# factores = ['Monoclonal', 'monoclonal', 'MONOCLONAL', 'Kappa', 'kappa', 'KAPPA', 'Lambda',
#             'lambda', 'LAMBDA', 'IgG', 'IgA', 'IgM', 'iga', 'igg', 'igm', 'IGA', 'IGG', 'IGM', 'Proteínas totales']

# CONJUNTO DE PRUEBAS COMPLETO
factores = ['Monoclonal', 'monoclonal', 'MONOCLONAL', 'Kappa', 'kappa', 'KAPPA', 'Lambda',
            'lambda', 'LAMBDA', 'IgG', 'IgA', 'IgM', 'Proteínas totales', 'Hemoglobina', 'Volumen corpuscular medio',
            'Plaquetas', 'Leucocitos', 'Neutrofilos (V. Absoluto)', 'Monocitos (V. Absoluto)',
            'Linfocitos (V. Absoluto)', 'Albúmina', 'Calcio', 'LDH', 'Creatinina']

factoresOut = ['Ac. anti Neisseria', 'Anti Polisacárido', 'Bordetella', 'Hepatitis',  'orina', 'ORINA', 'Herpes',
               'Haemophilus', 'Difteria',  'Paperas', 'Rubeola', 'Sarampión', 'Toxina tetánica', 'Varicela',
               'espícula', 'Cardiolipina', 'Toxoplasmosis', 'Citomegalovirus', 'Parvovirus', 'Epstein-Barr',
               'endomisio', 'Legionella', 'Rickettsia', 'Brucelosis', 'Chlamydia', 'Mycoplasma', 'Borrelia',
               'Helicobacter', 'Adenovirus', 'No se detectan', 'Anticuerpos', 'UNI', 'LCR',
               'antigangliosidos', 'Coxiella', 'Aspergillus', 'Leishmaniosis', 'Bartonella',
               'A1c', 'Hemoglobina corpuscular media', 'Hemoglobina, gasometría',
               'Albúmina, proteinograma', 'transglutaminasa', 'Transglutaminasa']

pacienteID, numSolicitud, tipoPrueba, fechaPrueba, resPrueba, udsPrueba \
    = dataIN['IDPaciente'], dataIN['NumSolicitud'], dataIN['Prueba'], \
    dataIN['FRealizacion'], dataIN['Resultado'], dataIN['Unidades']


for i in range(len(pacienteID)):

    if any(elemento in tipoPrueba[i] for elemento in factores):
        if not any(elemento in tipoPrueba[i] for elemento in factoresOut):
            if isinstance(resPrueba[i], (int, float)):
                dataOUT['IDPaciente'].append(pacienteID[i])
                dataOUT['NumSolicitud'].append(numSolicitud[i])
                dataOUT['Prueba'].append(tipoPrueba[i])
                dataOUT['FRealizacion'].append(fechaPrueba[i])
                dataOUT['Resultado'].append(resPrueba[i])
                dataOUT['Unidades'].append(udsPrueba[i])


nuevoExcel = os.path.join(datosDir, 'DatosPruebas1b.xlsx')
dout = pd.DataFrame(dataOUT)
dout.to_excel(nuevoExcel, index=True)
