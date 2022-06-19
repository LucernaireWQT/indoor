import enum
from random import sample
import sys
import pandas as pd

# Replace NaN: fixed value (-95), average of dataset, average of room
# Remove macs with poor detection rate
# Keep random subset of macs
# Normalize data

class NaNValueAction(enum.Enum):
    GLOBAL_AVERAGE = "GLOBAL_AVERAGE"
    ZONE_AVERAGE = "ROOM_AVERAGE"


def clean_data(dataframe: pd.DataFrame, nanValueAction: int | float | NaNValueAction = -95, detection_threshold: float = 0, random_sample_fraction: float = 1) -> pd.DataFrame:

    # Remove columns with a detection rate below given threshold
    nb_rows = len(dataframe.index)
    dataframe = dataframe.dropna(axis=1, thresh=int(nb_rows*detection_threshold))

    # Get list of macs
    macs = list(dataframe.columns.drop(["zone", "mesure"]))
    nb_macs = len(macs)

    # Drop a random sample of macs according to the given rate
    dropped_macs = sample(macs, int(nb_macs * (1 - random_sample_fraction)))
    dataframe = dataframe.drop(dropped_macs, axis=1)

    # If nan replace value is a number, replace all values with the given number
    if isinstance(nanValueAction, int | float):
        dataframe = dataframe.fillna(nanValueAction)

    # Replace NaN with average over all dataframe
    elif nanValueAction == NaNValueAction.GLOBAL_AVERAGE:
        global_mean = dataframe.drop(["zone", "mesure"], axis=1).mean()

        for mac, value in global_mean.items():
            mac = str(mac)
            dataframe[mac] = dataframe[mac].fillna(value)

    # Replace NaN with average of zone
    elif nanValueAction == NaNValueAction.ZONE_AVERAGE:
        zones = dataframe["zone"].unique()
        for zone in zones:
            zone_row_bools = dataframe["zone"] == zone
            zone_mean = dataframe[zone_row_bools].drop(["zone", "mesure"], axis=1).mean().fillna(-95)  # type: ignore

            for mac, value in zone_mean.items():  # type: ignore
                mac = str(mac)
                dataframe.loc[zone_row_bools, mac] = dataframe[mac][zone_row_bools].fillna(value)


    macs = dataframe.columns.drop(["zone", "mesure"])
    # 'normalize' the data
    dataframe[macs] = dataframe[macs].add(95).divide(95)
    
    return dataframe

if __name__ == "__main__":
    args = sys.argv
    _, file_in, file_out, *_ = args
    

    df = pd.read_csv(file_in, skipinitialspace=True)
    df = clean_data(df)
    df.to_csv(file_out, index=False)