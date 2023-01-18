#!/usr/bin/env bash

# make subdirectories for inudnation .tif files
# create file of launcher commands

if [ -f mosaic_launcher.sh ]; then
    rm mosaic_launcher.sh
fi

# calculation identifier, change each run
# using flows sent from Tim on 2022-12-21
export calc_id=20221221
mkdir mosaic_${calc_id}
mods=("1 2a 2b 3a 3b")
for D in 12*; do
    if [ -d "${D}" ]; then
        for i in ${mods[@]}; do
            if [ -d "${D}"/inundation_${calc_id}/mod"${i}" ]; then
                echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
${D}/inundation_${calc_id}/mod${i}/healed_*.tif \
mosaic_${calc_id}/${D}_mod${i}_healed_mosaic.tif" >> mosaic_launcher.sh
            fi
        done
    fi
done

# wait to complete all above tasks before moving on
# echo wait >> mosaic_launcher.sh

if [ -f full_mosaic_launcher.sh ]; then
    rm full_mosaic_launcher.sh
fi

# mosaic together individual HUC8 maps
mkdir full_mosaic_${calc_id}
for i in ${mods[@]}; do
    echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
mosaic_${calc_id}/*_mod${i}_healed_mosaic.tif \
full_mosaic_${calc_id}/mod${i}_healed_full_mosaic.tif" >> full_mosaic_launcher.sh
done

