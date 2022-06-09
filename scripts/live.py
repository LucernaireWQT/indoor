import tensorflow as tf
import pandas as pd
import json

from get_data import get_rssis
model = tf.keras.models.load_model("saved_model/my_model")
with open("saved_model/my_model/macs.json") as fp:
    macs = json.load(fp)

while True:
    rssis = get_rssis()
    known_mac_rssis = {k: rssis[k] if k in rssis else -95 for k in macs}
    print(known_mac_rssis)
    # print(rssis)

    df = pd.DataFrame(known_mac_rssis, index=[1]).astype("float64")
    df = df.reindex(sorted(df.columns), axis=1)
    # print(df)

    print(model.predict(df))
    
