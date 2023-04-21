#!/usr/bin/env bash

conda activate gis-env
module load launcher
export LAUNCHER_WORKDIR="$(pwd)"
export LAUNCHER_JOB_FILE="$(pwd)/full_mosaic_launcher.sh"
$LAUNCHER_DIR/paramrun

