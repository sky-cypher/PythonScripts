#!/usr/bin/env python
import os
from io import StringIO
import requests
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


def getData(script_code, start, end):
    price_endpoint = "https://api.bseindia.com/BseIndiaAPI/api/StockPriceCSVDownload/w"
    info_endpoint = "https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w"
    price_params = {
        "pageType" : "0",
        "rbType" : "D",
        "Scode" : str(script_code),
        "FDates" : str(start),
        "TDates" : str(end),
            }
    info_params = { "Scripcode" : str(script_code) }
    headers = {
        "Host" : "api.bseindia.com",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv :94.0) Gecko/20100101 Firefox/94.0",
            }
    csv_data = requests.get(price_endpoint, params=price_params, headers=headers)
    info = requests.get(info_endpoint, params=info_params, headers=headers)
    name = info.json()[0]["Scrip_Name"][:-1]
    return name, StringIO(csv_data.text)

start = dt.datetime(2020,1,1)
end = dt.datetime.now()
if int(end.strftime("%H")) < 16:
    end -= dt.timedelta(days=1)
start = start.strftime("%d/%m/%Y")
end = end.strftime("%d/%m/%Y")

script_code = input("Enter script code : ")
if not script_code : script_code = '500209'

try:
    company, daily = getData(script_code,start,end)
    daily = pd.read_csv(daily)
except requests.exceptions.RequestException:
    if 'y' in input("Read from file :").lower():
        daily = pd.read_csv(script_code + '.csv')
        company = input("Enter company name : ")
    else:
        quit()

daily["Date"] = pd.to_datetime(daily["Date"], format="%d-%B-%Y")
daily.sort_values(by = ["Date"])
daily.set_index("Date", inplace = True)
data = daily.head(len(daily) - 100)
prediction_days = 60
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data['Close Price'].values.reshape(-1,1))

def train_model():
    x_train = []
    y_train = []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)
    model.save(f'{script_code}_model.hdf5')
    return model


try:
    model = load_model(f'{script_code}_model.hdf5')
except Exception as e:
    print(e)
    print("Training model :")
    model = train_model()


test_data = daily.tail(100)
actual_prices = test_data['Close Price'].values

total_dataset = pd.concat((data['Close Price'], test_data['Close Price']), axis=0)
model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

x_test = []
for x in range(prediction_days, len(model_inputs) + 1):
    x_test.append(model_inputs[x-prediction_days:x, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)
print(f"Next day's {company} price : {round(float(predicted_prices[-1]), 2)}")

fig = plt.figure()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(0.6)
ax = fig.add_subplot(111)
ax.patch.set_facecolor('#2d2d2d')
ax.patch.set_alpha(1.0)

plt.plot(actual_prices, color='#5567d5',
        label=f"Actual {company} Price")
plt.plot(predicted_prices, color='#55d567',
        label=f"Predicted {company} Price")
plt.title(f"{company} Share Price \u20b9")
plt.ylabel('Price')
plt.legend()
plt.show()
