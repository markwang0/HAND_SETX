#!/bin/bash

# get event identifier of run with -e flag
# e.g. ./inun_launcher_prep.sh -e harvey
while getopts n: flag; do
    case "${flag}" in
        e) event=${OPTARG};;
    esac
done

echo "Event: $event"

# create file of launcher commands
# make subdirectories for inundation .tif files
if [ -f inun_launcher_${event}.sh ]; then
    rm inun_launcher_${event}.sh
fi

for D in 3m/12*; do
    if [ -d "${D}" ]; then
        mkdir -p ${D}/inundation/${event}
        echo "python calc_inun.py \"${D}\" \"${event}\"" >> inun_launcher_${event}.sh
    fi
done
