import geopandas as gpd
import pandas as pd

from glob import glob

catch_paths = glob(
    "./3m/12*/gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg"
)

# concatenate together HydroID and areasqkm lists for each HUC8
pd.concat(
    [
        gpd.read_file(
            p,
            ignore_geometry=True,
            ignore_fields=[
                # "HydroID",
                "S0",
                "LakeID",
                "LengthKm",
                "From_Node",
                "To_Node",
                "NextDownID",
                "min_thal_elev",
                "med_thal_elev",
                "max_thal_elev",
                # "areasqkm",
                "feature_id",
                "order_",
                # "geometry",
            ],
        )
        for p in catch_paths
    ]
).to_csv("./done/all_hydroid_areasqkm.csv", index=False)
