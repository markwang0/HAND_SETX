# Data
USGS 10m DEM derived HAND (CONUS): https://cfim.ornl.gov/data/

Fathom 3m DEM derived HAND (SETX): [`/corral/utexas/NFIE-NWM-UT/nfiedata/pin2flood/20230113_MarkWang`](https://web.corral.tacc.utexas.edu/nfiedata/pin2flood/20230113_MarkWang/)

# Workflow

### Prepare file structure

Clone this repo, obtain HUCs of interest, and save them into the repo. For example, execute these commands:

```sh
# clone and cd to this repo
git clone https://github.com/markwang0/HAND_SETX.git
cd HAND_SETX

# download and unzip HUC8 datasets
wget -r --no-parent -A '12*.zip' https://web.corral.tacc.utexas.edu/nfiedata/pin2flood/20230113_MarkWang/
unzip '12*.zip'
```
### Crop HAND

```sh
./crop_all_hand.sh
```

### Calculate inundation

For efficiency, inundation can be calculated for each HUC in parallel with TACC's [`launcher`](https://portal.tacc.utexas.edu/software/launcher). 

Create a list of python commands, `inun_launcher.sh`, to run with `launcher`:

```sh
./inun_launcher_prep.sh    # creates inun_launcher.sh
```

Then set `LAUNCHER_JOB_FILE` to point to `inun_launcher.sh`. Alternatively, run `inun_launcher.sh` line-by-line to calculate inundation as a serial job.

### Mosaic inundation maps together

For example, use GDAL to mosaic inundation maps for Hurricane Ike at the Sabine Lake HUC8 (12040201):

```sh
gdalwarp -dstnodata -9999 \
         -srcnodata -9999 \
         -co "COMPRESS=LZW" \
          12040201/inundation/ike/*.tif \
          12040201/inundation/ike_mosaic.tif
```

### Generate discharge and WSE profiles

See the `calc_profiles.ipynb` Jupyter notebook
