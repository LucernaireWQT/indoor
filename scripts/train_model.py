from time import time
import tensorflow as tf
import pandas as pd
from tensorflow import keras  

from utils import get_train_and_test_data

df = pd.read_csv("data/out.csv")

X_train, X_test, y_train, y_test = get_train_and_test_data(df, 0.2)

model = tf.keras.Sequential([
    keras.layers.Input(shape=(len(X_train.columns))),
    keras.layers.GaussianNoise(0.05),
    keras.layers.Dropout(0.05),
    keras.layers.Dense(200, activation="relu"),
    keras.layers.Dense(50, activation="relu"),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(7),
    keras.layers.Softmax()
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


callbacks = [keras.callbacks.TensorBoard(log_dir=f'./logs/{time()}')]
model.fit(X_train, y_train, validation_data = (X_test, y_test), epochs=1000, callbacks=callbacks, use_multiprocessing=True)

model.save("saved_model/my_model")
new_model = keras.models.load_model("saved_model/my_model")
new_model.evaluate(X_test, y_test)


