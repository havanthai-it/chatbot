from keras.layers import Input, LSTM, Dense, Masking
from keras.models import Sequential
from keras.optimizers import Adam


def build_model(X, y):
    m, time_steps, max_len = X.shape

    model = Sequential()
    model.add(Masking(mask_value=0, input_shape=(time_steps, max_len)))
    model.add(LSTM(512, dropout=0.3, return_sequences=False))
    model.add(Dense(units=max_len, activation="softmax"))
    adam = Adam(lr=0.003, beta_1=0.9, beta_2=0.999, decay=0.0001)
    model.compile(loss="categorical_crossentropy",
                  optimizer=adam,
                  metrics=["accuracy"])
    model.summary()
    return model
