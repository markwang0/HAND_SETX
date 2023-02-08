import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio
import sys

# pass HUC8 name (subdirectory name) as command line argument
huc8_path = sys.argv[1]
event = sys.argv[2]

df = pd.read_csv(f"/work2/08291/mwa/stampede2/HAND_SETX/done/{event}_stage.csv")

catch_df = gpd.read_file(
    f"{huc8_path}/gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg",
    layer="gw_catchments_reaches_filtered_addedAttributes_crosswalked",
)

# keep only those HydroIDs present in this HUC8 (HydroID == FATSGTID)
if ("FATSGTID" in df.columns) and ("HydroID" not in df.columns):
    df = df.rename(columns={"FATSGTID": "HydroID"})
df = df[df["HydroID"].isin(catch_df["HydroID"])]

for hydroid in df["HydroID"]:
    if len(df["stage_m"].loc[df["HydroID"] == hydroid]) != 0:
        stage = df["stage_m"].loc[df["HydroID"] == hydroid].item()
        with rio.open(f"{huc8_path}/cropped_hand/hand_{hydroid}.tif") as src:
            hand = src.read(1, masked=True)
            profile = src.profile
        # set inundation to 0 for nodata (-9999) and hand >= stage
        # otherwise inundation is stage minus hand
        inun = np.where((hand >= stage) | (hand < 0), 0, stage - hand)
        inun = np.ma.masked_where(inun == 0, inun)  # mask out 0 inundation
        # save mask with GDAL convention
        msk = (~inun.mask * 255).astype("uint8")
        with rio.Env(GDAL_TIFF_INTERNAL_MASK=True):
            with rio.open(
                f"{huc8_path}/inundation/{event}/inun_{hydroid}.tif",
                "w",
                **profile,
            ) as ds_out:
                ds_out.write(inun, 1)
                if isinstance(msk, np.uint8):
                    continue
                else:
                    ds_out.write_mask(msk)
