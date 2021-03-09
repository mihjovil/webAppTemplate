import numpy as np
import pandas as pd
import keras as k
from sklearn.preprocessing import MinMaxScaler

# region Constants
default_window_size = 14
prefix_weights = "model_weights/"
dictionary_of_weights = {
    1: prefix_weights+"checkpoints/one_day.ckpt",
    2: prefix_weights+"checkpoints/two_day_separation.ckpt",
    3: prefix_weights+"checkpoints/three_separation.ckpt",
    4: prefix_weights+"checkpoints/four_separation.ckpt",
    5: prefix_weights+"checkpoints/5_forecast_no_separation.ckpt",
    6: prefix_weights+"checkpoints/six_separation.ckpt",
    7: prefix_weights+"checkpoints/seven_separation.ckpt"
}
scale = MinMaxScaler()
# endregion


def create_trained_model():
    input_layer = k.layers.Input((default_window_size, 1))
    hidden_layer = k.layers.CuDNNGRU(64, return_sequences=True)(input_layer)
    hidden_layer = k.layers.CuDNNGRU(64)(hidden_layer)
    output_layer = k.layers.Dense(1)(hidden_layer)
    model = k.Model(inputs=input_layer, outputs=output_layer)
    return model


def load_weights(model, days):
    model.load_weights(dictionary_of_weights[days])
    return model


def load_file(path):
    df = pd.read_excel(path, names=['Date', 'Euro', 'Rate'])
    temp_col = np.array(df.Rate).reshape(-1, 1)
    temp_col = scale.fit_transform(temp_col)
    return temp_col


def weekly_forecast(path):
    model = create_trained_model()
    data = load_file(path)
    predictions = []
    # region forecasting
    # One day ahead
    model = load_weights(model, 1)
    temp_input = np.expand_dims(data[-14:], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # Two days ahead
    model = load_weights(model, 2)
    temp_input = np.expand_dims(data[-28::2], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # Three days ahead
    model = load_weights(model, 3)
    temp_input = np.expand_dims(data[-42::3], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # Four days ahead
    model = load_weights(model, 4)
    temp_input = np.expand_dims(data[-56::4], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # Five days ahead
    model = load_weights(model, 5)
    temp_input = np.expand_dims(data[-14:], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # Six days ahead
    model = load_weights(model, 6)
    temp_input = np.expand_dims(data[-84::6], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # Seven days ahead
    model = load_weights(model, 7)
    temp_input = np.expand_dims(data[-98::7], 0)
    temp_y = model.predict(temp_input)
    predictions.append(scale.inverse_transform(temp_y))
    # endregion
    return predictions


