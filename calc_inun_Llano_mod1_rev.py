import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio


module1_df = pd.read_csv("mod1_rev.csv")  # missing stages filled in

mod_dfs_temp = [module1_df]

catch_df = gpd.read_file(
    "gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg",
    layer="gw_catchments_reaches_filtered_addedAttributes_crosswalked",
)

# keep only those FATSGTIDs present in this HUC8
mod_dfs = []
for mod_df in mod_dfs_temp:
    mod_df = mod_df[mod_df["FATSGTID"].isin(catch_df["HydroID"])]
    mod_dfs.append(mod_df)

for (mod_df, name) in zip(mod_dfs, ["mod1"]):
    for fatsgtid in mod_df["FATSGTID"]:
        if len(mod_df["stage_m"].loc[mod_df["FATSGTID"] == fatsgtid]) != 0:
            stage = mod_df["stage_m"].loc[mod_df["FATSGTID"] == fatsgtid].item()
            for (fpath, heal_status) in zip(
                ["hand_FATSGTID_", "hand_healed_FATSGTID_"],
                ["unhealed", "healed"],
            ):
                with rio.open(f"cropped_hand/{fpath}{fatsgtid}.tif") as src:
                    hand = src.read(1, masked=True)
                    profile = src.profile
                # set inundation to 0 for nodata (-9999) and hand >= stage
                # otherwise inundation is stage minus hand
                inun = np.where((hand >= stage) | (hand < 0), 0, stage - hand)
                inun = np.ma.masked_where(
                    inun == 0, inun
                )  # mask out 0 inundation
                # save mask with GDAL convention
                msk = (~inun.mask * 255).astype("uint8")
                with rio.Env(GDAL_TIFF_INTERNAL_MASK=True):
                    with rio.open(
                        f"inundation_rev/{name}/{heal_status}_inun_{fatsgtid}.tif",
                        "w",
                        **profile,
                    ) as ds_out:
                        ds_out.write(inun, 1)
                        if isinstance(msk, np.uint8):
                            continue
                        else:
                            ds_out.write_mask(msk)
