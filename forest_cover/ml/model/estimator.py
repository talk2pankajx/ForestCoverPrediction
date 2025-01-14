from forest_cover.constants.training_pipe import MODEL_FILE_NAME,SAVED_MODELS_DIR
from forest_cover.exception import ForestException
from forest_cover.logging import logging

import os
import sys


class ForestPredictionModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise ForestException(e, sys)
        
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred
        except  Exception as e:
            raise ForestException(e, sys)
        
        