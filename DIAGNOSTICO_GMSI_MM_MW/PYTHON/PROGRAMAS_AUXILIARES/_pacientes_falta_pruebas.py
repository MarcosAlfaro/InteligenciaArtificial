import pandas as pd
import _1a_quitar_pacientes

datosPruebas = pd.read_excel("DatosPruebas.xlsx")

DP_pacienteID = datosPruebas['IDPaciente']
DP_tipoPrueba = datosPruebas['Prueba']


pruebas = ['Componente Monoclonal', 'Ratio Kappa/Lambda', 'IgA', 'IgG', 'IgM', 'Proteínas totales',
           'Hemoglobina', 'VCM', 'Leucocitos', 'Plaquetas', 'Neutrofilos', 'Monocitos', 'Linfocitos',
           'Albúmina', 'Calcio', 'Proteína C reactiva', 'VSG', 'LDH',
           'Creatinina', 'Beta-2 microglobulina suero']


pruebasPacientes = []
for ID in range(0, 575):
    pruebasPacientes.append([])

for i in range(0, len(DP_pacienteID)):
    # DP_tipoPrueba[i] = str(DP_tipoPrueba[i])
    if "onoclo" in DP_tipoPrueba[i]:
        pruebaNueva = 'Componente Monoclonal'
    elif "appa" in DP_tipoPrueba[i] or 'lambda' in DP_tipoPrueba[i] or \
            "KAPPA" in DP_tipoPrueba[i] or "LAMBDA" in DP_tipoPrueba[i]:
        pruebaNueva = 'Ratio Kappa/Lambda'
    elif 'IgA' in DP_tipoPrueba[i]:
        pruebaNueva = 'IgA'
        if int(DP_pacienteID[i]) == 413:
            print(i)
    elif 'IgG' in DP_tipoPrueba[i]:
        pruebaNueva = 'IgG'
    elif 'IgM' in DP_tipoPrueba[i]:
        pruebaNueva = 'IgM'
    elif 'Proteínas totales' in DP_tipoPrueba[i]:
        pruebaNueva = 'Proteínas totales'
    elif 'Hemoglobina' in DP_tipoPrueba[i]:
        pruebaNueva = 'Hemoglobina'
    elif 'Plaquetas' in DP_tipoPrueba[i]:
        pruebaNueva = 'Plaquetas'
    elif 'Leucocitos' in DP_tipoPrueba[i]:
        pruebaNueva = 'Leucocitos'
    elif 'Monocitos' in DP_tipoPrueba[i]:
        pruebaNueva = 'Monocitos'
    elif 'Neutrofilos' in DP_tipoPrueba[i]:
        pruebaNueva = 'Neutrofilos'
    elif 'Linfocitos' in DP_tipoPrueba[i]:
        pruebaNueva = 'Linfocitos'
    elif 'Volumen corpuscular' in DP_tipoPrueba[i]:
        pruebaNueva = 'VCM'
    elif 'Velocidad' in DP_tipoPrueba[i]:
        pruebaNueva = 'VSG'
    elif 'Creatinina' in DP_tipoPrueba[i]:
        pruebaNueva = 'Creatinina'
    elif 'Albúmina' in DP_tipoPrueba[i]:
        pruebaNueva = 'Albúmina'
    elif 'Calcio' in DP_tipoPrueba[i]:
        pruebaNueva = 'Calcio'
    elif 'C reactiva' in DP_tipoPrueba[i]:
        pruebaNueva = 'Proteína C reactiva'
    elif 'LDH' in DP_tipoPrueba[i]:
        pruebaNueva = 'LDH'
    elif 'Beta-2' in DP_tipoPrueba[i]:
        pruebaNueva = 'Beta-2 microglobulina suero'
    else:
        continue

    if pruebaNueva not in pruebasPacientes[int(DP_pacienteID[i])]:
        pruebasPacientes[int(DP_pacienteID[i])].append(pruebaNueva)

for ID in range(0, 575):
    if not ID in _1a_quitar_pacientes.IDexcluidos:
        for p in pruebas:
            if p not in pruebasPacientes[ID]:
                print(f"ID{ID}: {p}")
