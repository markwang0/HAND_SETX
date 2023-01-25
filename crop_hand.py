# crop HAND HUC rasters into component FATSGTID (3m) / COMID (10m) watersheds
# healed and unhealed HAND

import geopandas as gpd
import numpy as np
import os
import pandas as pd
import rasterio as rio
import rasterio.mask as rmsk
import sys

from glob import glob

# different filenames for 3m Fathom DEM and 10m USGS DEM

# 10m USGS
if "10m" in os.getcwd():
    catch_df_file = glob("*_catch.sqlite")[0]
    catch_df = gpd.read_file(catch_df_file)
    # project from EPSG:4269 (NAD83) to EPSG:5070 (NAD83 / Conus Albers)
    catch_df = catch_df.to_crs("EPSG:5070")

    # before running script, project HAND raster to EPSG:5070
    # for example with nodata and compression options:
    # gdalwarp -dstnodata -9999 -co "COMPRESS=LZW" -t_srs EPSG:5070 \
    #           120402hand.tif 120402hand_proj.tif
    hand_raster_fpath = glob("*hand_proj.tif")[0]
    src_hand = rio.open(hand_raster_fpath)

    in_meta = src_hand.meta
    segment_feature_name = "comid"

elif "3m" in os.getcwd():
    catch_df_file = (
        "gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg"
    )
    catch_df = gpd.read_file(catch_df_file)

    hand_raster_fpath = "rem_zeroed_masked_healed.tif"
    src_hand = rio.open(hand_raster_fpath)

    in_meta = src_hand.meta
    segment_feature_name = "HydroID"

else:
    print("incorrect directory structure")
    sys.exit()

if not os.path.isdir("cropped_hand"):
    os.mkdir("cropped_hand")

for seg_feat in catch_df[segment_feature_name]:
    geo = (
        catch_df["geometry"]
        .loc[catch_df[segment_feature_name] == seg_feat]
        .item()
    )

    out_image, out_transform = rmsk.mask(src_hand, [geo], crop=True)
    out_meta = in_meta.copy()
    out_meta.update(
        {
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
        }
    )

    with rio.open(f"cropped_hand/hand_{seg_feat}.tif", "w", **out_meta) as dst:
        dst.write(out_image)
