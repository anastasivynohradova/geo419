# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
# import packages
import os
import requests
import zipfile36 as zipfile
import io
from osgeo import gdal
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
#from cv2 import cv2
from skimage import io, exposure, data

print("Willkommen!")


def script():

    def downtiff():
    #create folder
        if  os.path.exists('GEO_ex_folder'):
            print("Folder exists")
        else:
            os.makedirs('GEO_ex_folder')
            print('A new folder has been created')

        os.chdir('GEO_ex_folder')

        if os.path.isfile('GEO419_Testdatensatz'):
            print("Zip file File exists")
        elif not os.path.isfile('GEO419_Testdatensatz'):
            print('Download starts')
            zipurl = 'https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip'
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


    def imageread():
        ds = gdal.Open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif")
        #image = np.array(Image.open('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'))
        image = np.array(ds.GetRasterBand(1).ReadAsArray())
        # log skalierung
        image[image != 0] = (np.log10(image[image > 0])) * 10
        # 0 Werte als nAn darstellen
        image[image == 0] = np.nan
        return image


    def mask(image):
        # Use a mask to mark the NaNs
        image_masked = np.ma.masked_not_equal(image, np.nan)
        percentiles = np.percentile(image_masked, (2, 98))
        scaled = exposure.rescale_intensity(image_masked,
                                            in_range=tuple(percentiles))
        return scaled


    def imagevisualize(image_masked):
        np.savetxt('out', image_masked, delimiter=',')
        plt.imshow(image_masked, interpolation='nearest', cmap='gray')
        plt.show()

    if __name__ == "__main__":
        downloadunpack = downtiff()
        tifcheck = tifcheck()
        image = imageread()
        image_masked = mask(image)
        image_combined = imagevisualize(image_masked)

if __name__ == "__main__":
    script = script()

