T = readtable('DATOS/VectoresPacientes.csv');
T = table2array(T);
T = T(1:292,:);
matrizCorr = corrcoef(T);
vectorCorr = matrizCorr(2:end-1,end);
vectorCorrAbsoluto = abs(vectorCorr);
[vectorCorrOrdenado, indices] = sort(vectorCorrAbsoluto);
vectorOrdenado = vectorCorr(indices)
indices