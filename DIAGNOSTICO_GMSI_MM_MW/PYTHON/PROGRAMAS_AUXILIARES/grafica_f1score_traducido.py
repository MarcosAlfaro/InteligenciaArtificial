import matplotlib.pyplot as plt

# Datos de F1-Score
classifiers = ['Árbol de decisión', 'Análisis discriminante', 'Regresión logística', 'Naïve-Bayes', 'SVM', 'KNN', 'MLP']
types = ['Coarse', 'Subspace', '', 'Gaussian', 'Coarse Gaussian', 'Coarse', 'Feedforward']
f1_scores = {
    'Árbol de decisión':         [68.7, 36.4, 66.5, 83.6],
    'Análisis discriminante': [79.5, 82.5, 89.5, 89.9],
    'Regresión logística':   [78.0, 55.9, 57.6, 71.9],
    'Naïve-Bayes':           [47.3, 69.7, 71.2, 80.3],
    'SVM':                   [84.2, 89.5, 94.3, 90.6],
    'KNN':                   [67.7, 71.2, 79.3, 79.9],
    'MLP':            [87.7, 89.4, 90.9, 86.2]
}
experiments = ['C1', 'C2', 'C3', 'C4']

# Creación del gráfico
fig, ax = plt.subplots()
plt.grid()
for classifier in classifiers:
    ax.plot(experiments, f1_scores[classifier], marker='o', label=classifier)

# Ajustes del gráfico
ax.set_xlabel('Conjunto')
ax.set_ylabel('F1-Score (%)')
ax.set_title('Diagnóstico de progresión de GMSI a MM/MW')
ax.set_ylim(0, 100)  # Límite del eje Y de 0 a 100
ax.legend(title='Clasificadores')

# Mostrar gráfico
plt.savefig("graficaF1Score_traducido.png", dpi=400)
plt.show()
