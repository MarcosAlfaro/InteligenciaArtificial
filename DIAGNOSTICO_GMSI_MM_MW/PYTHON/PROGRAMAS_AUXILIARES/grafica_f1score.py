import matplotlib.pyplot as plt

# Datos de F1-Score
classifiers = ['Decision Tree', 'Discriminant Analysis', 'Logistic Regression', 'Naïve-Bayes', 'SVM', 'KNN', 'Neural Net']
types = ['Coarse', 'Subspace', '', 'Gaussian', 'Coarse Gaussian', 'Coarse', 'Feedforward']
f1_scores = {
    'Decision Tree':         [68.7, 36.4, 66.5, 83.6],
    'Discriminant Analysis': [79.5, 82.5, 89.5, 89.9],
    'Logistic Regression':   [78.0, 55.9, 57.6, 71.9],
    'Naïve-Bayes':           [47.3, 69.7, 71.2, 80.3],
    'SVM':                   [84.2, 89.5, 94.3, 90.6],
    'KNN':                   [67.7, 71.2, 79.3, 79.9],
    'Neural Net':            [87.7, 89.4, 90.9, 86.2]
}
experiments = ['EXP1', 'EXP2', 'EXP3', 'EXP4']

# Creación del gráfico
fig, ax = plt.subplots()
plt.grid()
for classifier in classifiers:
    ax.plot(experiments, f1_scores[classifier], marker='o', label=classifier)

# Ajustes del gráfico
ax.set_xlabel('Experiment')
ax.set_ylabel('F1-Score (%)')
ax.set_title('Classifier F1-Score by Experiment')
ax.set_ylim(0, 100)  # Límite del eje Y de 0 a 100
ax.legend(title='Classifier')

# Mostrar gráfico
plt.savefig("graficaF1Score.png", dpi=400)
plt.show()
