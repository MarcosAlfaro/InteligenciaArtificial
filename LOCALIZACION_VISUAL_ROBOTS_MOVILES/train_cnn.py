"""
TRAIN CODE: PLACE RECOGNITION TASK
3 CNNs trained with RGB images, depth maps and RGBd images (EARLY FUSION)

Train dataset: Freiburg Part A, cloudy sampled (556 images)
Validation dataset: Freiburg Part A, cloudy sampled (586 images)
Visual model dataset: the training set is employed as visual model

Training length: 500000 triplet samples

Training samples are chosen randomly, but following these restrictions:
- dist(Img Anchor, Img Positive) < 0.5m
- dist(Img Anchor, Img Negative) > 0.5m

CNN model: CosPlace
Transfer Learning in all the layers
Loss function: Batch Hard Loss (m=0.25)
"""


import torch
import os
import csv
import numpy as np
import torch.nn.functional as F
from torch.utils.data import DataLoader
from sklearn.neighbors import KDTree
import losses
import create_datasets
from models import CosPlace_RGB, CosPlace_d, CosPlace_RGBd
from config import PARAMS
from functions import create_path


device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

csvDir = create_path(os.path.join(PARAMS.csvDir, "TRAIN_DATA"))
formatList = PARAMS.formatList


"""NETWORK TRAINING"""

with open(csvDir + "/TrainData.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Img Format", "Desc Length", "Iteration", "Recall@k1", "Geometric Error"])

    lossFunction = "batch hard"
    margin = PARAMS.margin
    criterion = losses.BatchHardLoss()

    for imgFormat in formatList:

        if imgFormat in ["RGB", "d"]:

            trainDataset = create_datasets.Train(imgFormat=imgFormat)
            valDataset = create_datasets.Validation(imgFormat=imgFormat)
            vmDataset = create_datasets.VisualModel(imgFormat=imgFormat)

        elif imgFormat == "RGBd":

            trainDataset = create_datasets.Train_EF()
            valDataset = create_datasets.Validation_EF()
            vmDataset = create_datasets.VisualModel_EF()

        trainDataloader = DataLoader(trainDataset, shuffle=False, num_workers=0, batch_size=PARAMS.batchSize)
        valDataloader = DataLoader(valDataset, shuffle=False, num_workers=0, batch_size=1)
        vmDataloader = DataLoader(vmDataset, shuffle=False, num_workers=0, batch_size=1)

        coordsVM = []
        for i, vmData in enumerate(vmDataloader, 0):
            _, coords = vmData
            coordsVM.append(coords.detach().numpy()[0])
        treeCoordsVM = KDTree(coordsVM, leaf_size=2)

        baseModelDir = PARAMS.modelsDir
        formatDir = create_path(os.path.join(baseModelDir, imgFormat))

        for descLength in PARAMS.lenList:

            netDir = create_path(os.path.join(formatDir, str(descLength)))

            with torch.no_grad():

                cosplace_weights = torch.load(
                    os.path.join(baseModelDir, "CosPlace_pretrained", "vgg16_" + str(descLength) + ".pth"))
                if imgFormat == "RGB":
                    net = CosPlace_RGB(out_dim=descLength).to(device)
                else:
                    weights_conv1 = cosplace_weights['backbone.0.weight']  # Copiar los pesos originales de RGB
                    new_weights_conv1 = weights_conv1.mean(dim=1, keepdim=True)
                    if imgFormat == "d":
                        net = CosPlace_d(out_dim=descLength).to(device)
                        cosplace_weights['backbone.0.weight'] = new_weights_conv1
                    elif imgFormat == "RGBd":
                        net = CosPlace_RGBd(out_dim=descLength).to(device)
                        cosplace_weights['backbone.0.weight'] = torch.cat((weights_conv1, new_weights_conv1), dim=1)
                    else:
                        raise ValueError("Non-valid image format. Valid formats: RGB, d, RGBd")
                net.load_state_dict(cosplace_weights)


            optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

            print("\nNEW TRAINING: ")
            print(f"Image format: {imgFormat}, Desc. Length: {descLength}\n")

            bestError = 1000
            it = 0
            for i, data in enumerate(trainDataloader, 0):
                anc, pos, neg = data
                anc, pos, neg = anc.to(device), pos.to(device), neg.to(device)

                optimizer.zero_grad()

                output1, output2, output3 = net(anc), net(pos), net(neg)
                loss = criterion(output1, output2, output3, margin)
                loss.backward()

                optimizer.step()

                if i % (round(len(trainDataloader)/PARAMS.numModelsSaved)) == 0:
                    print(f"It {it}/{PARAMS.numModelsSaved}, Current loss: {loss}")

                    """VALIDATION"""

                    net.eval()
                    with torch.no_grad():
                        recall, geomError, minErrorPossible = 0, 0, 0

                        descriptorsVM = []
                        for j, vmData in enumerate(vmDataloader, 0):
                            imgVM = vmData[0].to(device)
                            output = net(imgVM)
                            descriptorsVM.append(output)
                        descriptorsVM = torch.squeeze(torch.stack(descriptorsVM)).to(device)

                        for j, valData in enumerate(valDataloader, 0):

                            imgVal, coordsImgVal = valData
                            imgVal = imgVal.to(device)

                            output = net(imgVal)
                            coordsImgVal = coordsImgVal.detach().numpy()[0]

                            distances = F.pairwise_distance(output, descriptorsVM).reshape(1, -1)
                            idxMinPred = torch.argmin(distances).cpu().detach().numpy()

                            geomDistances, idxGeom = treeCoordsVM.query(coordsImgVal.reshape(1, -1), k=1)
                            idxMinReal = idxGeom[0][0]

                            coordsPredictedImg, coordsClosestImg = coordsVM[idxMinPred], coordsVM[idxMinReal]

                            if idxMinPred in idxGeom[0]:
                                recall += 1

                            geomError += np.linalg.norm(coordsImgVal - coordsPredictedImg)
                            minErrorPossible += np.linalg.norm(coordsImgVal - coordsClosestImg)

                        recall *= 100 / len(valDataloader)
                        geomError /= len(valDataloader)
                        minErrorPossible /= len(valDataloader)

                        if geomError <= bestError:
                            bestError = geomError

                        if i > 0:
                            netName = os.path.join(netDir, "net_it" + str(it))
                            torch.save(net, netName)

                        print(f"Recall@1: {recall} %, Geometric error: {geomError} m, Best error: {bestError} m\n")

                        writer.writerow([imgFormat, descLength, it, recall, geomError])

                    net.train(True)
                    it += 1

            netName = os.path.join(netDir, "net_end")
            torch.save(net, netName)
