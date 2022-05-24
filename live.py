import tensorflow as tf
import pandas as pd
import json

from get_data import get_rssis

def live_predict():
    model = tf.keras.models.load_model("saved_model/my_model")
    with open("saved_model/my_model/macs.json") as fp:
        macs = json.load(fp)

    rssis = get_rssis()
    known_mac_rssis = {k: rssis[k] if k in rssis else -95 for k in macs}
    print(rssis)

    df = pd.DataFrame(columns = macs).astype("float64")
    df = df.append(known_mac_rssis, ignore_index=True).add(100).divide(100)

    print(model.predict(df))
    

live_predict()