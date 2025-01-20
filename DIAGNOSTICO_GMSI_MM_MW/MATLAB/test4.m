T = readtable('VectoresPacientesTestExp4ID573.csv');
X = T(:,1:end-1);
Y = T(:,end);
y_actual = table2array(Y);
yActual = [yActual; y_actual];

yfit = tree.predictFcn(X);
tree = mean(yfit==y_actual)
yTree = [yTree; yfit];

yfit = disc.predictFcn(X);
discriminant = mean(yfit==y_actual)
yDisc = [yDisc; yfit];

yfit = regression.predictFcn(X);
logisticRegression = mean(yfit==y_actual)
yReg = [yReg; yfit];

yfit = bayes.predictFcn(X);
gaussianBayes = mean(yfit==y_actual)
yBayes = [yBayes; yfit];

yfit = SVM.predictFcn(X);
coarseGaussianSVM = mean(yfit==y_actual)
ySVM = [ySVM; yfit];

yfit = KNN.predictFcn(X);
coarseKNN = mean(yfit==y_actual)
yKNN = [yKNN; yfit];
