import matplotlib.pyplot as plt

# Datos de precisión
classifiers = ['Decision Tree', 'Discriminant Analysis', 'Logistic Regression', 'Naïve-Bayes', 'SVM', 'KNN', 'Neural Net']
types = ['Coarse', 'Subspace', '', 'Gaussian', 'Coarse Gaussian', 'Coarse', 'Feedforward']
precision_data = {
    'Decision Tree':         [97.0, 86.8, 94.2, 93.9],
    'Discriminant Analysis': [96.2, 93.6, 98.1, 96.0],
    'Logistic Regression':   [96.6, 87.5, 93.6, 93.3],
    'Naïve-Bayes':           [50.8, 90.6, 92.0, 90.0],
    'SVM':                   [97.8, 94.8, 97.0, 94.6],
    'KNN':                   [94.1, 93.6, 96.4, 95.6],
    'Neural Net':            [92.6, 93.6, 92.7, 75.7]
}
experiments = ['EXP1', 'EXP2', 'EXP3', 'EXP4']

# Creación del gráfico
fig, ax = plt.subplots()
plt.grid()
for classifier in classifiers:
    ax.plot(experiments, precision_data[classifier], marker='o', label=classifier)

# Ajustes del gráfico
ax.set_xlabel('Experiment')
ax.set_ylabel('Precision (%)')
ax.set_title('Classifier Precision by Experiment')
ax.set_ylim(0, 100)  # Límite del eje Y de 0 a 100
ax.legend(title='Classifier')

# Mostrar gráfico
plt.savefig("graficaPrecision.png", dpi=400)
plt.show()
