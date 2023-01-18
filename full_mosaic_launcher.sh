gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" mosaic_20221221/*_mod1_healed_mosaic.tif full_mosaic_20221221/mod1_healed_full_mosaic.tif
gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" mosaic_20221221/*_mod2a_healed_mosaic.tif full_mosaic_20221221/mod2a_healed_full_mosaic.tif
gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" mosaic_20221221/*_mod2b_healed_mosaic.tif full_mosaic_20221221/mod2b_healed_full_mosaic.tif
gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" mosaic_20221221/*_mod3a_healed_mosaic.tif full_mosaic_20221221/mod3a_healed_full_mosaic.tif
gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" mosaic_20221221/*_mod3b_healed_mosaic.tif full_mosaic_20221221/mod3b_healed_full_mosaic.tif
