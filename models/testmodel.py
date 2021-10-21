from model import ModelInterface

class TestModel(ModelInterface):
    def __init__(self):
        self.i = 4

    def predict(self, data):
        return data[len(data)-1] 
