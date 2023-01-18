# Data
[`/corral/utexas/NFIE-NWM-UT/nfiedata/pin2flood/2022-December`](https://web.corral.tacc.utexas.edu/nfiedata/pin2flood/2022-December/)

[`AustinExerciseModules.zip`](https://www.caee.utexas.edu/prof/maidment/Pin2Flood/AustinExerciseModules.zip)

# Workflow

Download data above by following the hyperlinks or copying from TACC. Clone and `cd` to this repository, download and unzip the archives linked above, and save them into the repository. For example, execute these commands:

```sh
# clone and cd to this repo
git clone https://github.com/markwang0/HAND_austin_exercises.git
cd HAND_austin_exercises
# download and unzip HUC8 datasets
wget -r --no-parent -A '12*.zip' https://web.corral.tacc.utexas.edu/nfiedata/pin2flood/2022-December/ 
unzip '12*.zip'
# download and unzip discharge scenarios
wget https://www.caee.utexas.edu/prof/maidment/Pin2Flood/AustinExerciseModules.zip
unzip 'AustinExerciseModules.zip'
```

After completing these steps your working directory should look something like this:
 
```sh
HAND_austin_exercises
├── 12070102
├── 12070203
├── 12070204
├── 12070205
├── 12090109
├── 12090201
├── 12090204
├── 12090205
├── 12090206
├── 12090301
├── 12100201
├── 12100202
├── 12100203
├── AustinExerciseModules
├── AustinExerciseModules.zip
├── calc_all_inun.sh
├── calc_inun.job
├── calc_inun.py
├── calc_profiles.ipynb
├── crop_all_hand.sh
├── crop_hand.py
├── hand_austin_exercises.yml
└── README.md
```

### Crop each healed and unhealed HAND raster to each FATSGTID

If you do not have a python environment with geopandas, numpy, pandas, rasterio & matplotlib, use the included conda environment:

```sh
conda create -f hand_austin_exercises.yml
conda activate hand-austin-exercises
```

Within the `HAND_austin_exercises` directory run:

```sh
sudo chmod +x crop_all_hand.sh
./crop_all_hand.sh
```

Or run `crop_hand.py` within each HUC8 subdirectory.

### Calculate inundation for each FATSGTID

Within the `HAND_austin_exercises` directory run:

```sh
sudo chmod +x calc_all_inun.sh
./calc_all_inun.sh
```

Or run `calc_inun.py` within each HUC8 subdirectory.

This saves inundation maps for each FATSGTID to the `inundation/mod{x}` directory within a HUC8 subdirectory. Inundation maps derived from healed HAND rasters are prefixed with `healed_`, otherwise they are prefixed with `unhealed_`.

### Create a composite inundation map for a HUC8 unit

For example, to composite the healed inundation maps for the LLano HUC8 (12090204) and module3b scenario into one inundation map, use GDAL:

```sh
cd 12090204/inundation/mod3b
gdalwarp -dstnodata -9999 \
         -srcnodata -9999 \
         -co "COMPRESS=LZW" \
          healed_*.tif mod3b_healed_mosaic.tif
```

### Generate discharge and WSE profiles

Follow the instructions in the `calc_profiles.ipynb` Jupyter notebook
