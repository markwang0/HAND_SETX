import geopandas as gpd
import numpy as np
import os
import pandas as pd
import rasterio as rio
import sys

from multiprocessing.pool import ThreadPool
# from multiprocessing import Pool

# make dir to keep inundation .tifs
# note: make symlink to $SCRATCH before running script
if not os.path.isdir("inundation_multi"):
    os.mkdir("inundation_multi")

huc6_dir = "../10m_HAND_HUC6_ike/"
huc6_10m_list = os.listdir(huc6_dir)

event = "ike"


def inun_huc6_10m(huc6_10m):
    print(f"processing {huc6_10m}")
    my_crs = "EPSG:26915"  # UTM projection
    catch_df_file = f"{huc6_dir}/{huc6_10m}/{huc6_10m}_catch.sqlite"
    catch_df = gpd.read_file(catch_df_file)
    catch_df = catch_df.to_crs(my_crs)

    # seg_ID = "HydroID" # 3m dataset
    seg_ID = "feature_id"  # 10m dataset

    # subset df to segments in current HUC
    # df = df[df[seg_ID].isin(catch_df["HydroID"])] # 3m dataset
    df = pd.read_csv(f"ike_stage.csv")
    df = df[df[seg_ID].isin(catch_df["comid"])]  # 10m dataset

    for hydroid in df[seg_ID]:
        # skip making inundation maps that already exist
        if os.path.isfile(f"inundation_multi/HUC{huc6_10m}_seg{hydroid}_inun.tif"):
            continue
        else:
            if len(df["stage_m"].loc[df[seg_ID] == hydroid]) != 0:
                stage = df["stage_m"].loc[df[seg_ID] == hydroid].item()
                with rio.open(
                    f"cropped_hand_multi/HUC{huc6_10m}_seg{hydroid}.tif",
                ) as src:
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
                        f"inundation_multi/HUC{huc6_10m}_seg{hydroid}_inun.tif",
                        "w",
                        **profile,
                    ) as ds_out:
                        ds_out.write(inun, 1)
                        if isinstance(msk, np.uint8):
                            continue
                        else:
                            ds_out.write_mask(msk)

if __name__ == '__main__':
    # pool = Pool(os.cpu_count() - 1)
    pool = ThreadPool()
    pool.map(inun_huc6_10m, huc6_10m_list)
