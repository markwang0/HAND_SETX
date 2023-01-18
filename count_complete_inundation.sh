#!/usr/bin/env bash
find 12*/inundation_20221221 -maxdepth 1 -type d | while read -r dir; do printf "%s:\t" "$dir"; find "$dir" -type f | wc -l; done
