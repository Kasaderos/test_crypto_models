from sklearn.linear_model import LinearRegression
from model import ModelInterface
import numpy as np


class MA(ModelInterface):
    def __init__(self) -> None:
        self.last_op = None 
        self.last_diff7 = 0 
        pass

    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w

    def predict(self, data):
        ma7 = self.moving_average(data, 7)
        ma25 = self.moving_average(data, 25)
        ma50 = self.moving_average(data, 50)

        diff7 = ma7[len(ma7)-1] - ma7[len(ma7)-2]
        diff25 = ma7[len(ma25)-1] - ma7[len(ma25)-2]
        diff50 = ma7[len(ma50)-1] - ma7[len(ma50)-2]
        
        last_price = data[len(data)-1]
        diff = last_price - data[len(data)-2]
        eps = 20

        if self.last_op == "buy":
            if diff7 < 0 or diff25 < 0 or diff50 < 0:
                self.Reverse = True
                self.last_op = "sell"
                self.last_diff7 = diff7 
                return last_price - 200, self.last_op, f"{self.last_op} {diff7} {diff25}"
        elif self.last_op == "sell" or self.last_op == None:
            #if diff7 > 0 and self.Reverse:
            #    self.last_diff7 = diff7
            #    return last_price + diff7, None, f"- {diff7} {diff25}" 

            self.Reverse = False
            if diff7 > eps and diff25 > eps:
                self.last_op = "buy"
                return last_price + 200, self.last_op, f"{self.last_op} {diff7} {diff25}" 
        return last_price + diff7, None, f"- {diff7} {diff25}" 

