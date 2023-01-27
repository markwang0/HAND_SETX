#!/usr/bin/env bash

# run crop_hand.py in each HUC directory
# HUC directories of interest begin with 12*
# activate conda environment first

# 3m Fathom DEM
for D in 3m/12*; do
    if [ -d "${D}" ]; then
        cd "${D}"
        cp /work2/08291/mwa/stampede2/HAND_SETX/crop_hand.py .
        python crop_hand.py
        echo "${D} done"
        cd /work2/08291/mwa/stampede2/HAND_SETX/
    fi
done

# # 10m USGS DEM
# for D in 10m/12*; do
#     if [ -d "${D}" ]; then
#         cd "${D}"
#         cp /work2/08291/mwa/stampede2/HAND_SETX/crop_hand.py .
#         python crop_hand.py
#         echo "${D} done"
#         cd /work2/08291/mwa/stampede2/HAND_SETX/
#     fi
# done
