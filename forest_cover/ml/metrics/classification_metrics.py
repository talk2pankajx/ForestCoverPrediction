from forest_cover.entity.artifact_entity import ClassificationMetrics
from forest_cover.exception import ForestException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys

def classification_score(y_true,y_pred):
    try:
        model_f1_score = f1_score(y_true,y_pred,average='weighted')
        model_precision_score = precision_score(y_true,y_pred,average='weighted')
        model_recall_score = recall_score(y_true,y_pred,average='weighted')
        classification_metrics = ClassificationMetrics(f1_score=model_f1_score, precision_score=model_precision_score, recall_score=model_recall_score)
        return classification_metrics
    except Exception as e:
        raise ForestException(e, sys)