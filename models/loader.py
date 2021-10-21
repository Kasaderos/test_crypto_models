import pandas as pd
import numpy as np


class Loader:
    def __init__(self, csv, sep=','):
        df = pd.read_csv(csv, sep=sep)
        self.data = df 

