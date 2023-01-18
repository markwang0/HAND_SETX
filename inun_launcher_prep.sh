#!/usr/bin/env bash

# make subdirectories for inudnation .tif files
# create file of launcher commands

if [ -f inun_launcher.sh ]; then
    rm inun_launcher.sh
fi

# calculation identifier, change each run
# using flows sent from Tim on 2022-12-21
export calc_id=20221221

for D in 12*; do
    if [ -d "${D}" ]; then
        mkdir -p ${D}/inundation_${calc_id}/mod{1,2a,2b,3a,3b}
        echo "python calc_inun.py \"${D}\" \"${calc_id}\"" >> inun_launcher.sh
    fi
done
