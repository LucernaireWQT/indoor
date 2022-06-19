from time import time
from sklearn import metrics
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from clean_data import clean_data
from clean_data import NaNValueAction  

from utils import get_train_and_test_data


raw_df = pd.read_csv("data/raw_captures.csv", skipinitialspace=True)
df = clean_data(raw_df, -95)

X_train, X_test, y_train, y_test = get_train_and_test_data(df, 0.2)

model = tf.keras.Sequential([
    keras.layers.Input(shape=(len(X_train.columns))),
    keras.layers.Dropout(0.8),
    # keras.layers.GaussianNoise(0.05),
    keras.layers.Dense(200, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(7),
    keras.layers.Softmax()
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

callbacks = [keras.callbacks.TensorBoard(log_dir=f'./logs/{time()}')]
model.fit(X_train, y_train, validation_data = (X_test, y_test), epochs=300, callbacks=callbacks, use_multiprocessing=True)

y_pred = tf.argmax(model.predict(X_test), axis=1)

test_labels_list = list(y_test)
predicted_labels_list = list(y_pred.numpy())

model.save("models/high_dropout")

print(metrics.confusion_matrix(test_labels_list, predicted_labels_list))