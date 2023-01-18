# crop HUC8 HAND rasters into component FATSGTID watersheds
# healed and unhealed HAND

import geopandas as gpd
import numpy as np
import os
import pandas as pd
import rasterio as rio
import rasterio.mask as rmsk

catch_df = gpd.read_file(
    "gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg",
    layer='gw_catchments_reaches_filtered_addedAttributes_crosswalked',
)

# Individual HUC8 Unit
hand_healed_raster_fpath = "rem_zeroed_masked_healed.tif"

src_hand_healed = rio.open(hand_healed_raster_fpath)
in_meta = src_hand_healed.meta

if not os.path.isdir("cropped_hand"):
    os.mkdir("cropped_hand")

for HydroID in catch_df["HydroID"]:
    geo = catch_df["geometry"].loc[catch_df["HydroID"] == HydroID].item()

    out_image, out_transform = rmsk.mask(src_hand_healed, [geo], crop=True)
    out_meta = in_meta.copy()
    out_meta.update(
        {
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
        }
    )

    with rio.open(
        f"cropped_hand/healed_FATSGTID_{HydroID}.tif", "w", **out_meta
    ) as dst:
        dst.write(out_image)




