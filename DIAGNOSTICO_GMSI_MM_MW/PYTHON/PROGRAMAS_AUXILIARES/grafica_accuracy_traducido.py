import matplotlib.pyplot as plt

# Datos
classifiers = ['Decision Tree', 'Discriminant Analysis', 'Logistic Regression', 'Naïve-Bayes', 'SVM', 'KNN', 'MLP']
types = ['Coarse', 'Subspace', '', 'Gaussian', 'Coarse Gaussian', 'Coarse', 'Feedforward']
data = {
    'Decision Tree':         [75.3, 60.7, 73.5, 85.4],
    'Discriminant Analysis': [82.2, 84.7, 90.1, 90.6],
    'Logistic Regression':   [81.1, 68.3, 68.6, 77.5],
    'Naïve-Bayes':           [49.7, 76.0, 75.9, 82.5],
    'SVM':                   [85.9, 90.3, 94.3, 91.2],
    'KNN':                   [74.2, 77.3, 82.0, 83.0],
    'MLP':            [88.0, 90.1, 90.9, 84.2]
}
experiments = ['EXP1', 'EXP2', 'EXP3', 'EXP4']
colors = ["cyan", "blue", "green", "orange", "brown", "magenta", "red"]

# Creación del gráfico
fig, ax = plt.subplots()
plt.grid()
for classifier in classifiers:
    ax.plot(experiments, data[classifier], color=colors[classifiers.index(classifier)], marker='o', label=classifier)

# Ajustes del gráfico
ax.set_xlabel('Experiment')
ax.set_ylabel('Accuracy (%)')
ax.set_title('Classifier Accuracy')
ax.set_ylim(0, 100)  # Límite del eje Y de 0 a 100
ax.legend(title='Classifier')

# Mostrar gráfico
plt.savefig("graficaAccuracy.png", dpi=400)
plt.show()
