gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" -co "BIGTIFF=YES" /scratch/08291/mwa/doe_data/mosaic/harvey_mosaic_*.tif /scratch/08291/mwa/doe_data/mosaic/harvey_full_mosaic.tif
gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" -co "BIGTIFF=YES" /scratch/08291/mwa/doe_data/mosaic/ike_mosaic_*.tif /scratch/08291/mwa/doe_data/mosaic/ike_full_mosaic.tif
gdalwarp -dstnodata -9999 -srcnodata -9999 -co "COMPRESS=LZW" -co "BIGTIFF=YES" /scratch/08291/mwa/doe_data/mosaic/imelda_mosaic_*.tif /scratch/08291/mwa/doe_data/mosaic/imelda_full_mosaic.tif
