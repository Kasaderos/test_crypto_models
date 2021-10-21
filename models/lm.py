from sklearn.linear_model import LinearRegression
from model import ModelInterface
import numpy as np


class LM(ModelInterface):
    def __init__(self) -> None:
        self.state = "buy"
        pass

    def predict(self, data):
        N = data.shape[0]
        M = data.shape[1]
        N1 = N-1
        X = data[:N1,:M-1] 
        y = data[:N1, M-1] 
        reg = LinearRegression().fit(X, y)
        self.rsquared = reg.score(X, y)
        
        X = np.array([data[N1,:M-1]])
        return reg.predict(X)[0] 
