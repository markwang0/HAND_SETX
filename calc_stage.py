import numpy as np
import os
import sys
import pandas as pd

events = ["harvey", "ike", "imelda"]
# event = "harvey"

for event in events:

    # flowrates for a storm in SETX. feature_id and FATSGTID
    df = pd.read_csv(
        f"./done/{event}_max_setx_FATSGTID.csv",
        usecols=["FATSGTID", "streamflow"],
    )

    df.index = df["FATSGTID"]
    df.drop(columns="FATSGTID", inplace=True)

    # read in master synthetic rating curves csv
    hydrotable = pd.read_csv(
        "./done/hydroTable_all_ID_stage_Q.csv",
        usecols=["FATSGTID", "feature_id", "stage", "discharge_cms"],
    )
    hydrotable.index = hydrotable["FATSGTID"]
    hydrotable.drop(columns="FATSGTID", inplace=True)

    # interpolate stage from streamflows with synthetic rating table
    event_df = pd.DataFrame()
    event_df.index = df.index
    event_df["Q_cms"] = df["streamflow"]
    event_df["stage_m"] = np.nan

    for hydroid in event_df.index:
        # HydroID = FATSGTID
        # for each HydroID, subset hydrotable.csv
        # to get the HydroID specific rating table
        # and interpolate stage from discharge
        stage = np.interp(
            event_df.loc[hydroid, "Q_cms"],
            hydrotable.loc[hydroid, "discharge_cms"],
            hydrotable.loc[hydroid, "stage"],
        )
        event_df.loc[hydroid, "stage_m"] = stage

    event_df.to_csv(
        f"./done/{event}_stage.csv",
    )

    del event_df
