# crop HAND HUC rasters into component FATSGTID (3m) / COMID (10m) watersheds

import geopandas as gpd
import numpy as np
import os
import pandas as pd
import rasterio as rio
import rasterio.mask as rmsk
import sys

from glob import glob
# from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from osgeo import gdal

# make dir to keep cropped hand .tifs
# note: make symlink to $SCRATCH before running script
if not os.path.isdir("cropped_hand_multi"):
    os.mkdir("cropped_hand_multi")

huc6_dir = "../10m_HAND_HUC6_ike/"
huc6_10m_list = os.listdir(huc6_dir)

def process_huc6_10m(huc6_10m):
    # 10m USGS dataset
    huc6_dir = "../10m_HAND_HUC6_ike/"
    my_crs = "EPSG:26915"  # UTM projection
    # change segment_feature_name if using 3m dataset
    segment_feature_name = "comid"

    print(f"processing {huc6_10m}")
    # project HAND raster
    hand_raster_fpath = f"{huc6_dir}/{huc6_10m}/{huc6_10m}dd.tif"
    hand_raster_proj_fpath = hand_raster_fpath[:-4] + "_proj.tif"
    hand_raster_proj = gdal.Warp(
        hand_raster_proj_fpath,
        hand_raster_fpath,
        # xRes=10,  # set resolution
        # yRes=10,
        # cutlineDSName="cutline.shp", # crop file
        # cropToCutline=True,
        dstNodata=-9999,
        dstSRS=my_crs,
        creationOptions=[
            "COMPRESS=LZW",
        ],
    )
    hand_raster_proj = None  # close GDAL dataset
    print("HAND raster projected")

    # project catchment
    catch_df_file = f"{huc6_dir}/{huc6_10m}/{huc6_10m}_catch.sqlite"
    catch_df = gpd.read_file(catch_df_file)
    catch_df = catch_df.to_crs(my_crs)
    print("catchment projected")

    # crop projected HAND to projected COMID catchments
    src_hand = rio.open(hand_raster_proj_fpath)
    in_meta = src_hand.meta
    for seg_feat in catch_df[segment_feature_name]:
        geo = (
            catch_df["geometry"].loc[catch_df[segment_feature_name] == seg_feat].item()
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

        with rio.open(
            f"cropped_hand_multi/HUC{huc6_10m}_seg{seg_feat}.tif", "w", **out_meta
        ) as dst:
            dst.write(out_image)
    print("cropped HAND raster to feature IDs")

if __name__ == '__main__':
    # pool = Pool(os.cpu_count() - 1)
    pool = ThreadPool()
    pool.map(process_huc6_10m, huc6_10m_list)
