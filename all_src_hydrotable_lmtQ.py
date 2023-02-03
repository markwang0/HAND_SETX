import pandas as pd
from glob import glob

ht_paths = glob("./3m/12*/hydroTable_rp_bf_lmtdischarge_cda.csv")
pd.concat(
    [
        pd.read_csv(p, usecols=["FATSGTID", "stage", "discharge_cms"])
        for p in ht_paths
    ]
).to_csv("./hydroTable_all_ID_stage_Q.csv", index=False)
