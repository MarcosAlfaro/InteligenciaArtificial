function obtain_metrics(classifierName, model, X, y_actual)

    fprintf('Type: %s', classifierName); 
    y_pred = model.predictFcn(X);
    
    accuracy = mean(y_pred==y_actual);
    
    TP = sum((y_pred == 1) & (y_actual == 1));
    FP = sum((y_pred == 1) & (y_actual == 0));
    TN = sum((y_pred == 0) & (y_actual == 0));
    FN = sum((y_pred == 0) & (y_actual == 1));
    
    fprintf('TP:%d, FP:%d, TN:%d, FN:%d\n', TP, FP, TN, FN); 
    
    precision = TP / (TP + FP);
    recall = TP / (TP + FN);
return