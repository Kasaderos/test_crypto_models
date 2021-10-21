from sklearn.linear_model import LinearRegression
from model import ModelInterface
import numpy as np


class CR(ModelInterface):
    def __init__(self) -> None:
        pass

    def predict(self, data):
        N = len(data)
        X = np.array(data[:N-1]).reshape(-1, 1)
        y = np.array(data[1:N])
        return 
