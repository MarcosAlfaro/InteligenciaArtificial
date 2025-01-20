"""
EN ESTE PROGRAMA SE ELIMINAN DEL EXCEL "DatosPruebas0.xlsx" LOS DATOS DE LAS PRUEBAS
CORRESPONDIENTES A PACIENTES QUE:
- no son de interés (IDexcluidos1)
- pertenecen a un grupo incorrecto (IDexcluidos2 e IDexcluidos3)

Tiempo ejecución: 4 min aprox.

Programa anterior a ejecutar: '_0_juntar_datos.py'
Programa siguiente a ejecutar: '_1b_quitar_pruebas_irrelevantes.py'
"""

import pandas as pd
import os


def quitar_pacientes_grupo_otros():
    excluidos = []

    for i in range(0, len(pacienteID)):
        if not ('IgA' in grupo[i] or 'IgG' in grupo[i] or 'IgM' in grupo[i]):
            excluidos.append(int(pacienteID[i]))
    return excluidos


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "DATOS")

datosPacientes = pd.read_excel(os.path.join(datosDir, 'PacientesAnonimo.xlsx'))

pacienteID = datosPacientes['IDPaciente']
grupo = datosPacientes['Ifs']


# excluidos por no ser de interés
IDexcluidos1 = [1, 3, 13, 17, 24, 25, 26, 28,  30, 31, 35, 36, 40, 47, 56, 57, 58, 59, 60, 63, 64, 67,
                75, 77, 83, 86, 93, 101, 105, 106, 109, 111, 122, 126, 130, 134, 137, 147, 155,
                156, 160, 163, 167, 170, 172, 177, 181, 186, 189, 197, 200, 201, 208, 210, 211,
                212, 220, 224, 226, 229, 231, 234, 239, 241, 244, 245, 255, 257, 259, 262, 263,
                266, 273, 278, 287, 288, 289, 292, 301, 303, 304, 307, 309, 313, 316, 317, 321,
                322, 331, 332, 360, 361, 383, 390, 395, 403, 405, 407, 417, 421, 425, 426, 430,
                436, 442, 444, 451, 455, 456, 458, 459, 461, 462, 464, 475, 480, 481, 482, 484,
                485, 486, 487, 490, 494, 501, 503, 509, 510, 516, 518, 521, 526, 528, 529, 530,
                541, 545, 546, 558, 567, 570, 571, 574]

# excluidos por grupo incorrecto
IDexcluidos2 = [112, 386]
IDexcluidos3 = quitar_pacientes_grupo_otros()


IDexcluidos = IDexcluidos1 + IDexcluidos2 + IDexcluidos3

