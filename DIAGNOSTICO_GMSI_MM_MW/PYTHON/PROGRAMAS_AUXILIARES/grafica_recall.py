import matplotlib.pyplot as plt

# Datos de recall
classifiers = ['Decision Tree', 'Discriminant Analysis', 'Logistic Regression', 'Naïve-Bayes', 'SVM', 'KNN', 'Neural Net']
types = ['Coarse', 'Subspace', '', 'Gaussian', 'Coarse Gaussian', 'Coarse', 'Feedforward']
recall_data = {
    'Decision Tree':         [53.1, 23.0, 51.4, 75.4],
    'Discriminant Analysis': [67.7, 73.8, 82.2, 84.5],
    'Logistic Regression':   [65.3, 41.0, 41.6, 58.5],
    'Naïve-Bayes':           [44.2, 56.6, 58.1, 72.5],
    'SVM':                   [73.9, 84.8, 91.7, 87.0],
    'KNN':                   [52.8, 57.4, 67.3, 68.7],
    'Neural Net':            [83.2, 85.5, 89.2, 100]
}
experiments = ['EXP1', 'EXP2', 'EXP3', 'EXP4']

# Creación del gráfico
fig, ax = plt.subplots()
plt.grid()
for classifier in classifiers:
    ax.plot(experiments, recall_data[classifier], marker='o', label=classifier)

# Ajustes del gráfico
ax.set_xlabel('Experiment')
ax.set_ylabel('Recall (%)')
ax.set_title('Classifier Recall by Experiment')
ax.set_ylim(0, 100)  # Límite del eje Y de 0 a 100
ax.legend(title='Classifier')

# Mostrar gráfico
plt.savefig("graficaRecall.png", dpi=400)
plt.show()
