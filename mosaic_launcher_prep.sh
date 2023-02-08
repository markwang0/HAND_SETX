#!/usr/bin/env bash

# make subdirectories for inundation .tif files
# create file of launcher commands

if [ -f mosaic_launcher.sh ]; then
    rm mosaic_launcher.sh
fi

export mosaic_dir=/scratch/08291/mwa/doe_data/mosaic

events=("harvey ike imelda")

for D in 3m/12*; do
    if [ -d "${D}" ]; then
        for event in ${events[@]}; do
            echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
${D}/inundation/${event}/inun_*.tif \
$mosaic_dir/${event}_mosaic_${D:3:-1}.tif" >> mosaic_launcher.sh
        done
    fi
done

# wait to complete all above tasks before moving on
# echo wait >> mosaic_launcher.sh

if [ -f full_mosaic_launcher.sh ]; then
    rm full_mosaic_launcher.sh
fi

# mosaic together individual HUC8 maps
for event in ${events[@]}; do
    echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
$mosaic_dir/${event}_mosaic_*.tif \
$mosaic_dir/${event}_full_mosaic.tif" >> full_mosaic_launcher.sh
done

