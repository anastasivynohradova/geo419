# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
# import packages
import os
import requests
import zipfile36 as zipfile
import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib import pyplot as plt
from skimage import exposure
from osgeo import gdal

print("Willkommen!")


def script():
    def tiff_download():
        # create folder
        if os.path.exists('GEO_ex_folder'):
            print("Folder exists")
        else:
            os.makedirs('GEO_ex_folder')
            print('A new folder has been created')

        os.chdir('GEO_ex_folder')

        if os.path.isfile('GEO419_Testdatensatz'):
            print("Zip file File exists")
        elif not os.path.isfile('GEO419_Testdatensatz'):
            print('Download starts')
            zipurl = 'https://upload.uni-jena.de/data/60faad3254c462.96067488/GEO419_Testdatensatz.zip'
            resp = requests.get(zipurl)

            zname = "GEO419_Testdatensatz"
            zfile = open(zname, 'wb')
            zfile.write(resp.content)
            zfile.close()

        if os.path.isfile('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'):
            print("Tif file exists")
        elif not os.path.isfile('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'):
            print('start unpacking')
            zfile = zipfile.ZipFile('GEO419_Testdatensatz')
            zfile.extractall()
            print('Zip unpacked')

    def tifcheck():
        for root, dirs, files in os.walk('GEO_ex_folder'):
            # select file name
            for file in files:
                # check the extension of files
                if file.endswith('.tif'):
                    # print whole path of files
                    print(os.path.join(root, file))
                else:
                    print('tif does not exist, please restart the programm')

    # Definierung einer Funktion zum Öffnen des Bildes
    # und logarithmische Skalierung des Bildes
    def image_read():
        # das Bild als read only-Bild öffnen
        # image = rasterio.open('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif')
        # with rasterio.open('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif') as src:
        #    image = src.read()
        image = gdal.Open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif", gdal.GA_Update)
        return image

    def log_scale(image):
        image_array = image.GetRasterBand(1).ReadAsArray()
        # logarithmisch skalieren
        image_array[image_array != 0] = (np.log10(image_array[image_array > 0])) * 10
        # 0 Werte als nAn darstellen
        image_array[image_array == 0] = np.nan
        # image = show(image_array, cmap='Greys_r')
        return image_array

    # Definierung einer Funktion zur weiteren Skalierung der Daten, bzw. Kontraststreckung
    def rescale_intensity(image):
        # Perzentile für Kontraststreckung definieren
        # und ignorieren nAn Werte
        min = np.nanmin(image)
        max = np.nanmax(image)
        percentiles = np.nanpercentile(image, (2, 98))
        # Strecken der Intensitätsstuffen, die innerhalb des 2. und 98. Perzentils liegen
        scaled = exposure.rescale_intensity(image,
                                            in_range=tuple(percentiles),
                                            out_range=(min, max))
        # image = show(scaled, cmap='Greys_r')
        return scaled

    def image_save():
        # Now to save your modifications into the same band you can do the following
        # This is writing the updated  array into the rasterband of the tif.
        #image.GetRasterBand(1).WriteArray(image_int)
        # You can create a copy of the existing image and save the  array into it like this
        driver = gdal.GetDriverByName('Gtiff')
        dst_ds = driver.CreateCopy("logscaled.tif", image, 1)
        dst_ds.GetRasterBand(1).WriteArray(image_int)
        dst_ds.FlushCache()
        del dst_ds

    # Definierung einer Funktion zur Bildvisualisierung
    def image_visualize():
        # Schreiben des neu berechneten Bildes in eine neue Datei
        src = rasterio.open("..\GEO_ex_folder\logscaled.tif")

        fig, ax = plt.subplots(figsize=(7, 4))

        # use imshow so that we have something to map the colorbar to
        image_hidden = ax.imshow(src.read(1),
                                 cmap='Greys_r')

        # plot on the same axis with rio.plot.show
        image = show(src.read(1),
                     transform=src.transform,
                     ax=ax,
                     cmap='Greys_r')

        # add colorbar using the now hidden image
        fig.colorbar(image_hidden, ax=ax)
        plt.show()

    if __name__ == "__main__":
        tiff_download()
        tifcheck()
        image = image_read()
        log_image = log_scale(image)
        image_int = rescale_intensity(log_image)
        image_save()
        image_visualize()


if __name__ == "__main__":
    script = script()
