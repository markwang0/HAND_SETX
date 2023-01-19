#!/bin/bash

# get name identifier of run with -n flag
# e.g. ./inun_launcher_prep.sh -n harvey
# if none given use date and time
while getopts n: flag; do
    case "${flag}" in
        n) name=${OPTARG};;
    esac
done

if (( $OPTIND == 1 )); then
    name=$(date +%Y%m%d-%H%M%S)
fi

echo "Identifier: $name"

# create file of launcher commands
# make subdirectories for inundation .tif files
if [ -f inun_launcher.sh ]; then
    rm inun_launcher.sh
fi

for D in 12*; do
    if [ -d "${D}" ]; then
        mkdir -p ${D}/inundation/${name}
        echo "python calc_inun.py \"${D}\" \"${name}\"" >> inun_launcher.sh
    fi
done
