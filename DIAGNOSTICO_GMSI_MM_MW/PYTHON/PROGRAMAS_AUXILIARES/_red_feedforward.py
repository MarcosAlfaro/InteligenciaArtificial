import torch
import torch.nn as nn
import pandas as pd
import torch.optim as optim
from sklearn.model_selection import KFold
import os
from sklearn.metrics import confusion_matrix
import scipy.io as sio


def test(model, yMLP):
    # Evaluar el modelo en datos de prueba
    model.eval()  # Establecer la red en modo de evaluación (desactiva la regularización, dropout, etc.)

    with torch.no_grad():  # Indicar a PyTorch que no calcule gradientes
        outputs = model(x_test_tensor)  # Obtener las predicciones en datos de prueba

        # Convertir las salidas a predicciones binarias (por ejemplo, si la salida es mayor a 0.5,
        # clasificar como 1, de lo contrario como 0)
        y_pred = (outputs > 0.5).float()

        y_test = y_test_tensor.unsqueeze(1)

        yMLP.append(list(y_pred))

        # Calcular la precisión
        accuracy = (y_pred == y_test).float().mean().item() * 100.0

        # Calcula la matriz de confusión
        TN, FP, FN, TP = confusion_matrix(y_test, y_pred).ravel()

        # Calcula la precisión y el recall
        # precision = precision_score(y_test, y_pred)
        # recall = recall_score(y_test, y_pred)

        print(f'Epoch: {ep+1}')
        print(f'TP:{TP}, FP:{FP}, TN:{TN}, FN:{FN}')
        print(f'Precisión en datos de prueba: {accuracy:.2f}%\n')
    return


class RedNeuronal(nn.Module):
    def __init__(self):
        super(RedNeuronal, self).__init__()
        self.capas_ocultas = nn.Sequential(
            nn.Linear(7, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.capas_ocultas(x)
        return x


baseDir = os.getcwd()
datosDir = os.path.join(baseDir, "MATLAB")

positivesID = [73, 294, 330, 412, 468, 534, 573]
show_accuracy_epochs = [2, 4, 9, 14]
# show_accuracy_epochs = [9]
numEpochs = 3

yActual, yMLP = [], []
for ID in positivesID:
    print(f"TEST ID{ID}")
    datosEntrenamiento = pd.read_csv(os.path.join(datosDir, "VectoresPacientesEntrenamientoExp4ID" + str(ID) + ".csv"))
    datosTest = pd.read_csv(os.path.join(datosDir, "VectoresPacientesTestExp4ID" + str(ID) + ".csv"))

    # Crea una instancia de KFold para dividir los datos en 5 pliegues
    kf = KFold(n_splits=5, shuffle=True)

    # Crear una instancia de la red neuronal
    red_neuronal = RedNeuronal()

    # Definir la función de pérdida
    criterion = nn.BCELoss()  # Entropía cruzada binaria para problemas de clasificación binaria

    # Definir el optimizador (por ejemplo, Descenso del Gradiente Estocástico)
    optimizer = optim.SGD(red_neuronal.parameters(), lr=0.01)  # lr es la tasa de aprendizaje

    # Ejemplo de entrenamiento
    batch_size = 1

    X = datosEntrenamiento.iloc[:, 0:-1]
    y = datosEntrenamiento.iloc[:, -1]

    X = X.values
    y = y.values

    x_test = datosTest.iloc[:, 0:-1]
    y_test = datosTest.iloc[:, -1]

    # Convertir datos de prueba a tensores de PyTorch (si no lo están)
    x_test_tensor = torch.tensor(x_test.values, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

    # Lista para almacenar las precisiones de cada pliegue
    precisiones = []
    for ep in range(numEpochs):
        for train_index, test_index in kf.split(X):
            X_train, X_val = X[train_index], X[test_index]
            y_train, y_val = y[train_index], y[test_index]

            for i in range(0, len(X_train), batch_size):
                inputs = torch.Tensor(X_train[i:i+batch_size])  # Convertir a tensores de PyTorch
                labels = torch.Tensor(y_train[i:i+batch_size])
                labels = labels.unsqueeze(1)

                # Resetear los gradientes
                optimizer.zero_grad()

                # Forward pass (propagación hacia adelante)
                outputs = red_neuronal(inputs)

                # Calcular la pérdida
                loss = criterion(outputs, labels)

                # Backward pass (propagación hacia atrás) y actualización de pesos
                loss.backward()
                optimizer.step()

            # Calcular la precisión en este pliegue
            # (suponiendo que 'red_neuronal' es tu modelo entrenado y 'x_test_tensor',
            # 'y_test_tensor' son los datos de prueba)
            red_neuronal.eval()
            outputs = red_neuronal(torch.tensor(X_val, dtype=torch.float32))
            predicciones = (outputs > 0.5).float()
            accuracy = (predicciones == torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)).float().mean().item() * 100.0

            # Guardar la precisión del pliegue actual en la lista de precisiones
            precisiones.append(accuracy)

        if ep in show_accuracy_epochs:
            test(red_neuronal, yMLP)

        # Imprimir la precisión promedio de los 5 pliegues
        # print(f'Época {ep+1}/{numEpochs}: Precisión promedio en validación: {np.mean(precisiones):.2f}%')


data = sio.loadmat('MATLAB/datos.mat')

print(data.keys())

# Añadir las nuevas variables al diccionario
data['MLP'] = yMLP

# Guardar todas las variables de nuevo en el archivo .mat
sio.savemat('MATLAB/datos.mat', data)
