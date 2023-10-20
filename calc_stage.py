import numpy as np
import os
import sys
import pandas as pd

# events = ["harvey", "ike", "imelda"]
events = ["ike"]


for event in events:
    # NWM flowrates for a given event
    df = pd.read_csv(
        f"./{event}_max_conus.csv",
        usecols=["feature_id", "streamflow"],
    )

    # read in master synthetic rating curves csv
    hydrotable = pd.read_csv(
        "./hydroTable_all_ID_stage_Q.csv",
        usecols=["CatchId", "Stage", "Discharge (m3s-1)"],
    )

    # keep only those HydroIDs present in hydrotable AOI (feature_id == CatchId)
    df = df[df["feature_id"].isin(hydrotable["CatchId"])]

    # reset indexing to simplify subsetting rating tables
    df.index = df["feature_id"]
    df.drop(columns="feature_id", inplace=True)
    hydrotable.index = hydrotable["CatchId"]
    hydrotable.drop(columns="CatchId", inplace=True)

    # interpolate stage from streamflows with synthetic rating table
    df["stage_m"] = np.nan

    for hydroid in df.index:
        # HydroID = CatchId or feature_id
        # for each HydroID, subset hydrotable to get the HydroID
        # specific rating table and interpolate stage from discharge
        stage = np.interp(
            df.loc[hydroid, "streamflow"],
            hydrotable.loc[hydroid, "Discharge (m3s-1)"],
            hydrotable.loc[hydroid, "Stage"],
        )
        df.loc[hydroid, "stage_m"] = stage

    df.to_csv(
        f"./{event}_stage.csv",
    )

    del df
