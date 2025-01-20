import yaml
import os

current_directory = os.path.dirname(os.path.realpath(__file__))


class Config():
    def __init__(self, yaml_file=os.path.join(current_directory, 'parameters.yaml')):
        with open(yaml_file) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            print(config)

            self.device = config.get('device')

            self.csvDir = config.get('csvDir')
            self.figuresDir = config.get('figuresDir')
            self.datasetDir = config.get('datasetDir')
            self.modelsDir = config.get('modelsDir')

            self.formatList = config.get('formatList')
            self.lenList = config.get('lenList')
            self.testEnv = config.get('testEnv')
            self.envs = config.get('envs')

            self.trainLength = config.get('trainLength')
            self.batchSize = config.get('batchSize')
            self.numModelsSaved = config.get('numModelsSaved')
            self.margin = config.get('margin')

            self.rPos = config.get('rPos')
            self.rNeg = config.get('rNeg')

            self.kMax = config.get('kMax')

            self.w = config.get('w')

            self.lf_methods = config.get('lf_methods')

            self.sizeRGB_MLP = config.get('sizeRGB_MLP')
            self.sizeDepth_MLP = config.get('sizeDepth_MLP')
            self.MLP_architecture = config.get('MLP_architecture')
            self.stopTrainingMLP = config.get('stopTrainingMLP')

            self.numComponents_PCA = config.get('numComponents_PCA')
            self.PCA_weighted = config.get('PCA_weighted')

            self.baseModel_MF = config.get('baseModel_MF')


PARAMS = Config()
