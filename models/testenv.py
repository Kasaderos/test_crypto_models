from testmodel import TestModel
from loader import Loader 
from lm import LM
from ma import MA 

# testenv tests the forecasts one step ahead

class TestEnv:
    def __init__(self, model, start_index=1):
        self.model = model
        self.start = start_index
        self.next = start_index
        self.price = 0
        self.eps = 0.001
        self.predicted = 0
        self.dir_predicted = 0
        self.commission = 0.002
        self.buy_price = None 
        self.cache = 0
        self.last_op = ""
        self.max_delta = 0
        self.min_delta = 100000000000
        self.data = None

    # loads time series of prices
    def load(self, data):
        self.ts = data['close'].to_numpy()
        self.data = data
        self.price = self.ts[self.next]

    # returns False if the ts row is over
    def update(self):

        self.price = self.ts[self.next]
        self.next += 1

        if self.next >= len(self.ts):
            return False

        self.next_price = self.ts[self.next]
        return True
    
    def calc_cache(self, op):
        if op == None:
            return

        assert op != self.last_op

        if op == "buy":
            self.buy_price = self.price

        if op == "sell":
            s = self.price - self.buy_price
            print(f"{self.price} {self.buy_price}")
            delta = s - s * self.commission

            self.min_delta = min(self.min_delta, delta)
            self.max_delta = max(self.max_delta, delta)

            print(f"cache = {self.cache} + delta {delta}")
            self.cache += delta 
            self.buy_price = None 

        self.last_op = op

    def predict(self):
        value, op, r2 = self.model.predict(self.data, self.next-1)

        self.calc_cache(op)

        next_price = self.next_price
        
        up = value > self.price and self.next_price > self.price
        down = value < self.price and self.next_price < self.price

        if up or down:
            self.dir_predicted += 1

        if up:
            print(f"up {self.next_price - self.price} {value - self.price}")

        if down:
            print(f"down {self.next_price - self.price} {value - self.price}")

        if value != 0 and abs(1 - next_price/value) < self.eps:
            self.predicted += 1
            return f"{next_price} + {value} params [ {r2} ]"
        return f"{next_price} - {value}  params [ {r2} ]"

    def print_result(self):
        print(f"\nvalue predicted    {self.predicted}/{len(self.ts)-self.start}")
        print(f"dir predicted     {self.dir_predicted}/{len(self.ts)-self.start}")
        print(f"cache     {self.cache}")
        print(f"min delta {self.min_delta}")
        print(f"max delta {self.max_delta}")


env = TestEnv(LM(), 1400)
loader = Loader('../data/btc_usdt_daily.csv')
env.load(loader.data)

while env.update():
    print(env.predict())
env.print_result()
