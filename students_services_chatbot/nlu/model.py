from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam


def build_model(X, y):
    """Build classification model"""
    model = Sequential()
    model.add(Dense(1024, input_dim=300, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(y.shape[1], activation="softmax"))
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
    model.compile(loss="categorical_crossentropy",
                  optimizer=adam,
                  metrics=["accuracy"])
    return model
