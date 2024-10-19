import numpy as np
from joblib import load
import pandas as pd

class PreprocessingStep:
    def __init__(self,scalerPath=None):
        self.scaler = load(scalerPath)
        self.scaler = self.scaler["decision_tree_scaler"]
    
    def preprocess(self, X):
        if X is None:
            X = [[27.0]]
        t = pd.DataFrame({"temperature": X[0]})
        #print("s", self.scaler.transform(t))
        return self.scaler.transform(t)

class DTClassifier:
    def __init__(self, SaveModelPath=None):
        self.saved_model_data = load(SaveModelPath)

    def preprocess(self, X):
        preprocessing = PreprocessingStep(scalerPath="saveModels\decision_tree_scaler_11.pkl")
        return preprocessing.preprocess(X)

    def predict(self, X):
        X_scaled = self.preprocess(X)
        return self.saved_model_data.predict(X_scaled)

def mainQualityDetection(param, model="temperature"):
    prediction = None
    if param == "" :
        param = None
    if model == "temperature":
        dt_classifier = DTClassifier(SaveModelPath="saveModels\decision_tree_model11.pkl")
        prediction = dt_classifier.predict(np.array([param]).reshape(-1, 1))
    return False if prediction[0] == 0 else True
