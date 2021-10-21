from binance import Client
import numpy as np
import time
from lm import LM


def get_price():
	return float(client.get_avg_price(symbol=symbol)["price"])


def ma(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def get_parsed_data():
	data = client.get_klines(symbol=symbol, interval=interval, limit=1000)
	data = np.array(data)
	w = 5
	open = ma(data[:, 1].astype(np.float64), w)
	high = ma(data[:, 2].astype(np.float64), w)
	low = ma(data[:, 3].astype(np.float64), w)
	close = ma(data[:, 4].astype(np.float64), w)
	volume = ma(data[:, 5].astype(np.float64), w)
	#trades = data[:, 8].astype(np.int32)[w-1:]

	return np.column_stack((open, high, low, volume, close))


def get_min_diff(price):
	return price * (1+alpha)/(1-alpha) - price


def get_price_diff(price, beta):
	return get_min_diff(price) * (1+beta)

client = Client('apikey', 'secret')

# global params
symbol = "BTCUSDT"
interval = "4h"
alpha = 0.001

# stats
dir_predicted = 0
value_predicted = 0 
value_precision = 10 # for BTC USDT
st_err = 0

sleep_duration = 60 * 60 * 4 # sec

model = LM()
iteration = 0
while True:
	last_price = get_price() 
	value = model.predict(get_parsed_data())
	time.sleep(sleep_duration)

	price = get_price()
	
	if value > last_price and price > last_price or \
		value < last_price and price < last_price: 
		dir_predicted += 1
	
	if abs(value - price) < value_precision:
		value_predicted += 1

	print(f"last_price {last_price} price {price} predicted {value} ")
	print(f"dir predicted {dir_predicted} value predicted {value_predicted}")
	iteration += 1
	

