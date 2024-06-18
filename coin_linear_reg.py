#read a series of csv files containing cryptocurrency data, train a linear regression model, extrapolate 30 days into the future, and then show a visual representation of the results
#reference used: https://medium.com/hackerdawn/bitcoin-price-prediction-using-linear-regression-94e0e5a63c42

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

paths = ["btc_1year.csv", "eth_1year.csv", "sol_1year.csv"]

for path in paths:
    coin_name = path[0:3].upper()
    file_name = './data/' + path
    frame = pd.read_csv(file_name)

    #Price over time graph
    f1 = plt.figure(figsize = (12, 7))
    plt.plot(frame["time"], frame["close"], color='goldenrod', lw=2)
    plt.title("" + coin_name + " Price over time", size=25)
    plt.xlabel("Time", size=20)
    plt.ylabel("$ Price", size=20)
    f1.savefig("outputs\\" + coin_name + "_fig1")
    #f1.show()

    #convert timestamps to actual dates
    frame['Dates'] = pd.to_datetime(frame['time'], unit='s')

    #set features that will be used for training, and output label
    required_features = ['open', 'high', 'low', 'volumefrom', 'volumeto']
    output_label = 'close'

    #create test split
    x_train, x_test, y_train, y_test = train_test_split(
    frame[required_features],
    frame[output_label],
    test_size = 0.3
    )

    #create and train model
    model = LinearRegression()
    model.fit(x_train, y_train)

    print("" + coin_name + " Model score: "  + str(model.score(x_test, y_test)))

    #set up future forecasts
    future_set = frame.shift(periods=30).tail(30)
    prediction = model.predict(future_set[required_features])

    #future prediction graph
    f2 = plt.figure(figsize = (12, 7))
    plt.plot(frame["time"][-400:-60], frame["close"][-400:-60], color='goldenrod', lw=2)
    plt.plot(future_set["time"], prediction, color='deeppink', lw=2)
    plt.title("" + coin_name + " Price over time with Forecast", size=25)
    plt.xlabel("Time", size=20)
    plt.ylabel("$ Price", size=20)
    f2.savefig("outputs\\" + coin_name + "_fig2")
    #f2.show()