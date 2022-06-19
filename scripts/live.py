import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
import pandas as pd
import json
from get_data import get_rssis

model = tf.keras.models.load_model("saved_model/my_model")
with open("data/macs.json") as fp:
    macs = json.load(fp)

while True:
    rssis = get_rssis()
    known_mac_rssis = {k: rssis[k] if k in rssis else -95 for k in macs}

    df = pd.DataFrame(known_mac_rssis, index=[1]).astype("float64").add(95).divide(95)
    df = df[sorted(df.columns)]

    pred = model.predict(df, verbose=0)
    print(pred)

    y_pred = tf.argmax(pred, 1)
    print(y_pred.numpy()[0])
    
    
