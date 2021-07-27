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
    def image_read():
        image = gdal.Open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif", gdal.GA_Update)
        return image

    # Logarithmische Skalierung des Bildes
    def log_scale(image):
        # lesen das Bild als numpy Array
        image_array = image.GetRasterBand(1).ReadAsArray()
        # logarithmisch skalieren die Werte >0
        image_array[image_array != 0] = (np.log10(image_array[image_array > 0])) * 10
        # 0 Werte als nAn darstellen
        image_array[image_array == 0] = np.nan
        return image_array

    # Definierung einer Funktion zur weiteren Skalierung der Daten, bzw. Kontraststreckung
    def rescale_intensity(log_image):
        # berechnen min und max Werte im Array
        min = np.nanmin(log_image)
        max = np.nanmax(log_image)
        # Perzentile für Kontraststreckung definieren
        # und ignorieren nAn Werte
        percentiles = np.nanpercentile(log_image, (2, 98))
        # Strecken der Intensitätsstuffen, die innerhalb des 2. und 98. Perzentils liegen
        scaled = exposure.rescale_intensity(log_image,
                                            in_range=tuple(percentiles),
                                            out_range=(min, max))
        return scaled

    # Definierung einer Funktion zum Screiben des neu berechneten Array als raster Bild
    def image_save():
        # Erstellen der neuen Datei im tiff Format
        driver = gdal.GetDriverByName('Gtiff')
        # Kopieren der Geoinformation vom input Bild in die neue raster Datei
        output_image = driver.CreateCopy("logscaled.tif", image, 1)
        # Kopieren des numpy Arrays in die neue raster Datei
        output_image.GetRasterBand(1).WriteArray(image_int)
        #output_image.FlushCache()
        del output_image

    # Definierung einer Funktion zur Bildvisualisierung
    def image_visualize():
        # Öffnen des neu berechneten Bildes mit dem Packet rasterio
        new_image = rasterio.open("..\GEO_ex_folder\logscaled.tif")
        # Erstellen einer Figur und eines Subplots
        fig, ax = plt.subplots(figsize=(7, 4))
        # imshow verwenden um den Colorbar zuordnen zu können
        # das erste Band der Datei kann mit .read(1) gelesen werden
        image_hidden = ax.imshow(new_image.read(1),
                                 cmap='Greys_r')
        # Plotten auf der gleichen Achse mit rasterio.plot.show
        show(new_image.read(1),
                transform=new_image.transform,
                ax=ax,
                cmap='Greys_r')
        # Colorbar unter Verwendung des jetzt ausgeblendeten Bildes hinzufügen
        fig.colorbar(image_hidden, ax=ax)
        # Darstellung des Bildes mit Colorbar in einem Fenster
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
