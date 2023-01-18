import numpy as np
import os
import sys
import pandas as pd

# read in corrected streamflows

df = pd.read_csv(
    "./AustinExerciseModules_rev/20221221_FATSGTID_flows_all_modules.csv",
)

df.index = df["FATSGTID"]
df.drop(columns="FATSGTID", inplace=True)

# read in master synthetic rating curves csv
hydrotable = pd.read_csv(
    "./AustinExerciseModules_rev/hydroTable_all_rp_bf_lmtdischarge_cda.csv",
    usecols=["FATSGTID", "stage", "discharge_cms"],
)
hydrotable.index = hydrotable["FATSGTID"]
hydrotable.drop(columns="FATSGTID", inplace=True)

# interpolate stage from streamflows with synthetic rating table
for name in ["1", "2a", "2b", "3a", "3b"]:

    mod_df = pd.DataFrame()
    mod_df.index = df.index
    mod_df["streamflow"] = df[f"module{name}_cms"]
    mod_df["stage_m"] = np.nan

    for hydroid in mod_df.index:
        # for each HydroID, subset hydrotable.csv
        # to get the HydroID specific rating table
        # and interpolate stage from discharge
        stage = np.interp(
            mod_df.loc[hydroid, "streamflow"],
            hydrotable.loc[hydroid, "discharge_cms"],
            hydrotable.loc[hydroid, "stage"],
        )
        mod_df.loc[hydroid, "stage_m"] = stage

    mod_df.to_csv(
        f"./AustinExerciseModules_rev/20221221_mod{name}_stage.csv",
    )

    del mod_df
